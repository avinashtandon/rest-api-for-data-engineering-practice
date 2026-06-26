from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from typing import Optional
from datetime import datetime
import io
import pandas as pd
import json

from app.database.session import get_db
from app.api.dependencies import get_current_data_engineer, get_query_params
from app.utils.query_builder import QueryBuilder

# Import all models to allow generic export
from app.models.catalog import Product, Category
from app.models.people import Customer, Supplier, Employee
from app.models.transactions import Order, OrderItem, Payment, Invoice, Shipment
from app.models.location import Store, Department, Address, City, State, Country
from app.models.inventory import Warehouse, Inventory

router = APIRouter(prefix="/export", tags=["Data Extraction"])

# Map resource names to SQLAlchemy models
RESOURCE_MAP = {
    "products": Product,
    "categories": Category,
    "customers": Customer,
    "suppliers": Supplier,
    "employees": Employee,
    "orders": Order,
    "order_items": OrderItem,
    "payments": Payment,
    "invoices": Invoice,
    "shipments": Shipment,
    "stores": Store,
    "departments": Department,
    "warehouses": Warehouse,
    "inventory": Inventory
}

@router.get("/{resource}", summary="Bulk extract data for DE pipelines")
async def extract_data(
    resource: str,
    format: str = Query("csv", regex="^(csv|json)$"),
    query_params: dict = Depends(get_query_params),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_data_engineer)
):
    """
    Export data for a specific resource. 
    Supports incremental loading via updated_after and created_after query parameters.
    Returns streaming response to handle large datasets.
    """
    if resource not in RESOURCE_MAP:
        raise HTTPException(status_code=404, detail="Resource not found for extraction")
        
    model = RESOURCE_MAP[resource]
    builder = QueryBuilder(model)
    
    # We bypass the repository to do a raw query for DataFrame conversion
    from sqlalchemy.future import select
    stmt = select(model).where(model.deleted_at == None)
    
    if query_params.get("filters"):
        stmt = builder.apply_filters(stmt, query_params["filters"])
        
    stmt = builder.apply_sorting(stmt, query_params.get("sort_by"), query_params.get("order"))
    stmt = builder.apply_field_selection(stmt, query_params.get("fields"))
    
    # Do not apply pagination by default for bulk export unless specified
    if query_params.get("limit") != 100 or query_params.get("skip") != 0:
         stmt = builder.apply_pagination(stmt, query_params["skip"], query_params["limit"])
         
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    if not records:
        raise HTTPException(status_code=404, detail="No data found matching criteria")
        
    # Convert ORM objects to dicts using SQLAlchemy inspection
    data = []
    for record in records:
        record_dict = {c.key: getattr(record, c.key) for c in inspect(record).mapper.column_attrs}
        # Convert datetime objects to ISO format string for JSON/CSV safety
        for k, v in record_dict.items():
            if isinstance(v, datetime):
                record_dict[k] = v.isoformat()
            # Convert UUIDs to strings
            import uuid
            if isinstance(v, uuid.UUID):
                record_dict[k] = str(v)
        data.append(record_dict)
        
    df = pd.DataFrame(data)
    
    if format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={resource}_extract.csv"
        return response
        
    elif format == "json":
        stream = io.StringIO()
        # Use orient='records' for standard JSON array of objects
        df.to_json(stream, orient="records", date_format="iso")
        response = StreamingResponse(iter([stream.getvalue()]), media_type="application/json")
        response.headers["Content-Disposition"] = f"attachment; filename={resource}_extract.json"
        return response
