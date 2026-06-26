from sqlalchemy import Select, asc, desc, or_, and_, cast, String
from sqlalchemy.orm import load_only
from typing import Any, Dict, List, Optional
from datetime import datetime

class QueryBuilder:
    def __init__(self, model):
        self.model = model

    def apply_filters(self, stmt: Select, filters: Dict[str, Any]) -> Select:
        for key, value in filters.items():
            if value is None:
                continue
                
            # Handle standard incremental loading / DE fields
            if key == "updated_after" and hasattr(self.model, "updated_at"):
                stmt = stmt.where(self.model.updated_at >= value)
            elif key == "updated_before" and hasattr(self.model, "updated_at"):
                stmt = stmt.where(self.model.updated_at <= value)
            elif key == "created_after" and hasattr(self.model, "created_at"):
                stmt = stmt.where(self.model.created_at >= value)
            elif key == "created_before" and hasattr(self.model, "created_at"):
                stmt = stmt.where(self.model.created_at <= value)
            elif key == "deleted_after" and hasattr(self.model, "deleted_at"):
                stmt = stmt.where(self.model.deleted_at >= value)
            
            # Handle specific operators
            elif key.endswith("_gt") and hasattr(self.model, key[:-3]):
                stmt = stmt.where(getattr(self.model, key[:-3]) > value)
            elif key.endswith("_gte") and hasattr(self.model, key[:-4]):
                stmt = stmt.where(getattr(self.model, key[:-4]) >= value)
            elif key.endswith("_lt") and hasattr(self.model, key[:-3]):
                stmt = stmt.where(getattr(self.model, key[:-3]) < value)
            elif key.endswith("_lte") and hasattr(self.model, key[:-4]):
                stmt = stmt.where(getattr(self.model, key[:-4]) <= value)
            elif key.endswith("_like") and hasattr(self.model, key[:-5]):
                stmt = stmt.where(getattr(self.model, key[:-5]).ilike(f"%{value}%"))
            elif key == "q":
                # Full text search (very basic implementation scanning all string columns)
                search_conditions = []
                for c in self.model.__table__.columns:
                    if isinstance(c.type, String):
                        search_conditions.append(cast(getattr(self.model, c.name), String).ilike(f"%{value}%"))
                if search_conditions:
                    stmt = stmt.where(or_(*search_conditions))
            
            # Handle exact matches
            elif hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
                
        return stmt

    def apply_sorting(self, stmt: Select, sort_by: str, order: str = "asc") -> Select:
        if sort_by and hasattr(self.model, sort_by):
            column = getattr(self.model, sort_by)
            if order.lower() == "desc":
                stmt = stmt.order_by(desc(column))
            else:
                stmt = stmt.order_by(asc(column))
        else:
            # Default sorting by created_at desc
            if hasattr(self.model, "created_at"):
                stmt = stmt.order_by(desc(self.model.created_at))
        return stmt

    def apply_field_selection(self, stmt: Select, fields: str) -> Select:
        if fields:
            field_list = [f.strip() for f in fields.split(",")]
            columns = [getattr(self.model, f) for f in field_list if hasattr(self.model, f)]
            if columns:
                stmt = stmt.options(load_only(*columns))
        return stmt

    def apply_pagination(self, stmt: Select, skip: int, limit: int) -> Select:
        return stmt.offset(skip).limit(limit)

    def apply_cursor_pagination(self, stmt: Select, cursor: str, limit: int) -> Select:
        # Simplified cursor implementation assuming cursor is an ID encoded in base64
        # In a real enterprise system, cursor pagination is usually complex (e.g. keyset pagination)
        import base64
        import json
        if cursor:
            try:
                decoded = base64.b64decode(cursor).decode('utf-8')
                cursor_data = json.loads(decoded)
                if 'id' in cursor_data and hasattr(self.model, 'id'):
                    # Using > for keyset pagination assuming ordered by ID
                    stmt = stmt.where(self.model.id > cursor_data['id'])
            except Exception:
                pass
        return stmt.limit(limit)
