from model import (Base, session, Book, engine)
import datetime
import csv
import time

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
            input("\nPlease choose a number between 1 and 5. Press Enter to try again.")

def clean_date(date_str):
    months = [
        "January", "February", "March", "April", 
        "May", "June", "July", "August", 
        "September", "October", "November", "December"
    ]
    while True:
        try:
            split_date = date_str.split(' ')
            month = int(months.index(split_date[0]) + 1)
            day = int(split_date[1].strip(','))
            year = int(split_date[2])
            return datetime.date(year, month, day)
        except (ValueError, IndexError):
            date_str = input("Invalid date. Please try again (e.g., October 25, 2017): ")

def clean_price(price_str):
    while True:
        try:
            price_float = float(price_str)
            return int(price_float * 100)
        except ValueError:
            price_str = input("Invalid price. Please enter a number without symbols (e.g., 25.99): ")

def add_csv():
    try:
        with open('suggested_books.csv', newline='', encoding='utf-8') as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
                if book_in_db is None:
                    date = clean_date(row[2])
                    title = row[0]
                    author = row[1]
                    price = clean_price(row[3])
                    new_book = Book(title=title, author=author, published_date=date, price=price)
                    session.add(new_book)
                    print(f"Added book: {title} by {author}")
            session.commit()
    except FileNotFoundError:
        print("The file 'suggested_books.csv' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

def app():
    while True:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date = clean_date(input('Published Date (e.g., October 25, 2017): '))
            price = clean_price(input('Price (e.g., 25.64): '))
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added successfully!')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book).all():
                print(book)
        elif choice == '3':
            search_term = input("Enter title or author to search: ").strip()
            results = session.query(Book).filter((Book.title.ilike(f"%{search_term}%")) | (Book.author.ilike(f"%{search_term}%"))).all()
            for book in results:
                print(book)
        elif choice == '4':
            print("Book analysis functionality is under development.")
        elif choice == '5':
            print("Goodbye!")
            break

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
