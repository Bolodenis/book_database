from model import (Base, session, Book, engine)
import datetime
import csv

def menu():
    while True:
        print("""
        \nPROGRAMMING BOOKS
        \r1) Add book
        \r2) View all books
        \r3) Search for book
        \r4) Book analysis
        \r5) Exit
        """)
        
        choice = input("What would you like to do? ").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above.
            \rA number from 1-5.
            \rPress Enter to try again.
            ''')
            
def clean_date(date_str):
    months = [
    "January", "February", "March", "April", 
    "May", "June", "July", "August", 
    "September", "October", "November", "December"
]
    
    split_date = date_str.split(' ')
    print(split_date)
    month = int(months.index(split_date[0]) + 1)
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    
    return datetime.date(year, month, day)


def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float) * 100
    

def add_csv():
    try:
        with open('suggested_books.csv', newline='', encoding='utf-8') as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none
                if book_in_db == None
                    date = clean_date(row[2])
                    title = row[0]
                    author = row[1]
                    price = clean_price(row[3])
                    new_book = Book(title=title, author=author, published_date = date, price= price)
                    session.add(new_book)
            session.commit()
    except FileNotFoundError:
        print("The file 'suggested_books.csv' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            print("Add book functionality goes here.")  # Placeholder
        elif choice == '2':
            print("View all books functionality goes here.")  # Placeholder
        elif choice == '3':
            print("Search for book functionality goes here.")  # Placeholder
        elif choice == '4':
            print("Book analysis functionality goes here.")  # Placeholder
        elif choice == '5':
            print("GOODBYE")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()  # Run the main application
    add_csv()  # Uncomment to test CSV functionality separately
    for book in session.query(Book):
        print(book)
