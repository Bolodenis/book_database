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
    while True:
        try:
            split_date = date_str.split(' ')
            month = int(months.index(split_date[0]) + 1)
            day = int(split_date[1].strip(','))
            year = int(split_date[2])
            return datetime.date(year, month, day)
        except (ValueError, IndexError):
            date_str = input("Invalid date format. Please try again (e.g., October 25, 2017): ")


def clean_price(price_str):
    while True:
        try:
            price_float = float(price_str)
            return int(price_float * 100)
        except ValueError:
            price_str = input("Invalid price. Please enter a numeric value (e.g., 25.99): ")


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
            title = input('Title: ')
            author = input('Author: ')

            # Loop for validating date
            while True:
                date_input = input('Published Date (e.g., October 25, 2017): ')
                date = clean_date(date_input)
                if date:  # Valid date breaks the loop
                    break

            # Loop for validating price
            while True:
                price_input = input('Price (e.g., 25.64): ')
                price = clean_price(price_input)
                if price:  # Valid price breaks the loop
                    break

            # Add the new book
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added successfully!')
            time.sleep(1.5)

        elif choice == '2':
            books = session.query(Book).all()
            if books:
                for book in books:
                    print(f"{book.id} | {book.title} | {book.author} | {book.price} | {book.price}")
            else:
                print("No books found in the database.")

        elif choice == '3':
            search_term = input("Enter title or author to search: ").strip()
            results = session.query(Book).filter(
                (Book.title.ilike(f"%{search_term}%")) |
                (Book.author.ilike(f"%{search_term}%"))
            ).all()
            if results:
                for book in results:
                    print(book)
            else:
                print("No matching books found.")

        elif choice == '4':
            books = session.query(Book).all()
            if books:
                total_books = len(books)
                total_price = sum(book.price for book in books) / 100
                avg_price = total_price / total_books
                print(f"\nBook Analysis:")
                print(f"Total Books: {total_books}")
                print(f"Total Price: ${total_price:.2f}")
                print(f"Average Price: ${avg_price:.2f}")
            else:
                print("No books available for analysis.")

        elif choice == '5':
            print("GOODBYE")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Uncomment to load data from CSV
    add_csv()
    app()
