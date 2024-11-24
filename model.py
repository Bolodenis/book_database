from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    published_date = Column('Published', Date)  # Corrected the typo in "published_date"
    price = Column('Price', Integer)
    
    def __repr__(self):
        return "<Book(title='%s', author='%s', published_date='%s', price='%s')>" % (
            self.title, self.author, self.published_date, self.price)  # Corrected `price='s'` to properly include `%s`
