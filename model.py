from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///boks.db', echo = False)
Session = sessionmaker(bind=engine)
session = Session()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)  
    title = Column('Title', String)
    author = Column('Author', String)
    pulished_date = Column('Published', Date)
    price = Column('Price', Integer)
    
    
    def __repr__(self):
        return "<User(title='%s', author='%s', published_date='%s', price='s')>" % (
                self.title, self.author, self.published_date, self.price)