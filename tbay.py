
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# User model (table)
class User(Base):
    __tablename__ = "user"  # Table name
    
    # Table columns
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)    
    # Relationships
    auction_items = relationship("Item", backref="seller")
    bids = relationship("Bid", backref="user")

# Item model (table)
class Item(Base):
    __tablename__ = "item"  # Table name
    
    # Table columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    # Relationships
    seller_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    bids = relationship("Bid", backref="item")
    
# Bid model (table)
class Bid(Base):
    __tablename__ = "bid"  # Table name
    
    # Table columns
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)

# Delete all rows in all tables and create db model
def reset_db():
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)
  
def main():
  
  # Clear database tables
  reset_db()
  
  # Add three user to database
  john = User(username="John", password="john123")
  mickey = User(username="Mickey",password="mickey123")
  babe = User(username="Babe",password="babe123") 
  
  # Make one user auction a baseball
  baseball = Item(name="Baseball", description="Signed by like everyone", seller = babe)
  
  # Have each user place two bids on the baseball
  john_bid = Bid(price = 10000, user = john, item = baseball)
  mickey_bid = Bid(price = 20000, user = mickey, item = baseball)  
  session.add_all([john, mickey, babe, baseball, john_bid, mickey_bid])
  session.commit()
   
  # Perform a query to find out which user placed the highest bid
  row = session.query(User.username, Item.name).join(Bid, Item).filter(Item.name == "Baseball").order_by(Bid.price).all()
  highest_bidder = row[-1].username
  print "{} had the highest bid for the {}".format(highest_bidder, row[-1].name)

if __name__ == "__main__":
  main()