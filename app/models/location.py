from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class Country(Base):
    __tablename__ = "countries"
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    
    states = relationship("State", back_populates="country")

class State(Base):
    name = Column(String(100), index=True, nullable=False)
    code = Column(String(10), nullable=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False)
    
    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")

class City(Base):
    __tablename__ = "cities"
    name = Column(String(100), index=True, nullable=False)
    state_id = Column(UUID(as_uuid=True), ForeignKey("states.id"), nullable=False)
    
    state = relationship("State", back_populates="cities")
    addresses = relationship("Address", back_populates="city")

class Address(Base):
    __tablename__ = "addresses"
    line1 = Column(String(255), nullable=False)
    line2 = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=False)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)
    
    city = relationship("City", back_populates="addresses")

class Store(Base):
    name = Column(String(100), index=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    phone = Column(String(50), nullable=True)
    
    address = relationship("Address")

class Department(Base):
    name = Column(String(100), unique=True, index=True, nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=True)
    
    store = relationship("Store")
    employees = relationship("Employee", back_populates="department")
