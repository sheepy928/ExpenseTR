from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, create_engine, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dataclasses import dataclass
Base = declarative_base()

@dataclass
class USD(Float):
    dollars: int
    cents: int

    def __str__(self):
        return f"${self.dollars}.{self.cents:02d}"

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class TransactionList(Base):
    __tablename__ = 'transaction_list'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey('items.id', ondelete="CASCADE"))
    price = Column(Float)
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    item = relationship("Item")



class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey('merchants.id', ondelete="CASCADE"))
    amount = Column(Float)
    date = Column(Date)
    purchaser_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))

    merchant = relationship("Merchant")
    purchaser = relationship("Person", back_populates="transactions")
    items = relationship("TransactionList", back_populates="transaction",
                         cascade="all, delete, delete-orphan")
    splits = relationship("Split", back_populates="transaction",
                          cascade="all, delete, delete-orphan")
    def __str__(self):
        return f"{self.id}: {self.merchant.name} - {self.amount} - {self.date} - {self.purchaser.name}"
    
    Index('transaction_date_index', date)
    Index('transaction_merchant_id_index', merchant_id)


class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)



class Split(Base):
    __tablename__ = 'splits'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete="CASCADE"))
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))
    amount = Column(Float)

    transaction = relationship("Transaction", back_populates="splits")
    person = relationship("Person", back_populates="splits")

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    transactions = relationship("Transaction", order_by=Transaction.id,
                                back_populates="purchaser",
                                cascade="all, delete, delete-orphan")
    splits = relationship("Split", order_by=Split.id,
                          back_populates="person",
                          cascade="all, delete, delete-orphan")

    def __str__(self):
        return self.name

# Person.transactions = relationship("Transaction", order_by=Transaction.id, back_populates="purchaser")
# Person.splits = relationship("Split", order_by=Split.id, back_populates="person")


# Create an engine that stores data in the local directory's bill_tracking.db file.
engine = create_engine('sqlite:///bill_tracking.db?check_same_thread=False', echo=True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Create a sessionmaker bound to this engine
Session = sessionmaker(bind=engine)
