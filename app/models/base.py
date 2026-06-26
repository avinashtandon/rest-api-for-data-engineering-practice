import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean, Integer
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)  # Should ideally be a ForeignKey to User
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)

    # Note: For soft deletes, queries should typically filter by `deleted_at IS NULL` or `is_active = True`.
    # In a full SQLAlchemy implementation, we can use custom queries or base repository methods to automatically apply this.

Base = declarative_base(cls=CustomBase)
