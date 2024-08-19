# This is the main course of the program; Library Management System

import re
from book import Book
from user import User
from author import Author
import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elias928",
        database="library_management_system"
    )
    return connection



class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.authors = []

    def main_menu(self):
        while True:
            print("\nWelcome to the Library Management System!")
            print("Main Menu:")
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.book_operations()
            elif choice == '2':
                self.user_operations()
            elif choice == '3':
                self.author_operations()
            elif choice == '4':
                print("Thank you for using the Library Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_operations(self):
        while True:
            print("\nBook Operations:")
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Search for a book")
            print("5. Display all books")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.borrow_book()
            elif choice == '3':
                self.return_book()
            elif choice == '4':
                self.search_book()
            elif choice == '5':
                self.display_books()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def user_operations(self):
        while True:
            print("\nUser Operations:")
            print("1. Add a new user")
            print("2. View user details")
            print("3. Display all users")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_user()
            elif choice == '3':
                self.display_users()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def author_operations(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add a new author")
            print("2. View author details")
            print("3. Display all authors")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_author()
            elif choice == '2':
                self.view_author()
            elif choice == '3':
                self.display_authors()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    # Define methods for book operations
    def add_book(self):
        try:
            title = input("Enter book title: ")
            author_name = input("Enter book author: ")
            genre = input("Enter book genre: ")
            publication_date = input("Enter publication date (YYYY-MM-DD): ")

            # Validate publication date format
            if not re.match(r"\d{4}-\d{2}-\d{2}", publication_date):
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

            # Check if the author already exists
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
            author_id = cursor.fetchone()

            if not author_id:
                biography = input("Enter author biography: ")
                cursor.execute("INSERT INTO authors (name, biography) VALUES (%s, %s)", (author_name, biography))
                connection.commit()
                author_id = cursor.lastrowid
                print(f"Author '{author_name}' added successfully.")
            else:
                author_id = author_id[0]

            cursor.execute("INSERT INTO books (title, author_id, genre, isbn, publication_date, availability) VALUES (%s, %s, %s, %s, %s, %s)",
                           (title, author_id, genre, "1234567890123", publication_date, True))
            connection.commit()
            print(f"Book '{title}' by {author_name} added successfully.")
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def borrow_book(self):
        try:
            library_id = input("Enter your library ID: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE library_id = %s", (library_id,))
            user_id = cursor.fetchone()

            if not user_id:
                print(f"User with Library ID '{library_id}' not found.")
                return

            title = input("Enter book title to borrow: ")
            cursor.execute("SELECT id, availability FROM books WHERE title = %s", (title,))
            book = cursor.fetchone()

            if book and book[1]:
                cursor.execute("UPDATE books SET availability = 0 WHERE id = %s", (book[0],))
                cursor.execute("INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, CURDATE())", (user_id[0], book[0]))
                connection.commit()
                print(f"Book '{title}' borrowed successfully.")
            else:
                print(f"Book '{title}' not found or already borrowed.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def return_book(self):
        try:
            library_id = input("Enter your library ID: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE library_id = %s", (library_id,))
            user_id = cursor.fetchone()

            if not user_id:
                print(f"User with Library ID '{library_id}' not found.")
                return

            title = input("Enter book title to return: ")
            cursor.execute("SELECT id FROM books WHERE title = %s", (title,))
            book_id = cursor.fetchone()

            if book_id:
                cursor.execute("UPDATE books SET availability = 1 WHERE id = %s", (book_id[0],))
                cursor.execute("UPDATE borrowed_books SET return_date = CURDATE() WHERE user_id = %s AND book_id = %s AND return_date IS NULL", (user_id[0], book_id[0]))
                connection.commit()
                print(f"Book '{title}' returned successfully.")
            else:
                print(f"Book '{title}' not found or already available.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def search_book(self):
        try:
            title = input("Enter book title to search: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT title, author_id, genre, publication_date, availability FROM books WHERE title = %s", (title,))
            book = cursor.fetchone()

            if book:
                cursor.execute("SELECT name FROM authors WHERE id = %s", (book[1],))
                author_name = cursor.fetchone()[0]
                print(f"Book found: '{book[0]}' by {author_name}, Genre: {book[2]}, Published on: {book[3]}, Available: {bool(book[4])}")
            else:
                print(f"Book '{title}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def display_books(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT title, author_id, genre FROM books")
            books = cursor.fetchall()

            if not books:
                print("No books available.")
            else:
                print("Books available:")
                for book in books:
                    cursor.execute("SELECT name FROM authors WHERE id = %s", (book[1],))
                    author_name = cursor.fetchone()[0]
                    print(f"'{book[0]}' by {author_name}, Genre: {book[2]}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    # Define methods for user operations
    def add_user(self):
        try:
            name = input("Enter user name: ")
            library_id = input("Enter library ID: ")

            # Validate library ID format (must be alphanumeric)
            if not re.match(r"^[a-zA-Z0-9]+$", library_id):
                raise ValueError("Invalid library ID format. Please use alphanumeric characters.")

            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, library_id) VALUES (%s, %s)", (name, library_id))
            connection.commit()
            print(f"User '{name}' added successfully.")
        except ValueError as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def view_user(self):
        try:
            library_id = input("Enter library ID to view details: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, library_id FROM users WHERE library_id = %s", (library_id,))
            user = cursor.fetchone()
            if user:
                cursor.execute("SELECT title FROM books JOIN borrowed_books ON books.id = borrowed_books.book_id WHERE borrowed_books.user_id = %s", (user[0],))
                borrowed_books = cursor.fetchall()
                borrowed_books_list = [book[0] for book in borrowed_books]
                print(f"User found: {user[1]}, Library ID: {user[2]}, Borrowed Books: {borrowed_books_list}")
            else:
                print(f"User with Library ID '{library_id}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def display_users(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name, library_id FROM users")
            users = cursor.fetchall()
            if not users:
                print("No users available.")
            else:
                print("Users available:")
                for user in users:
                    print(f"User: {user[0]}, Library ID: {user[1]}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    # Define methods for author operations
    def add_author(self):
        try:
            name = input("Enter author name: ")
            biography = input("Enter author biography: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO authors (name, biography) VALUES (%s, %s)", (name, biography))
            connection.commit()
            print(f"Author '{name}' added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def view_author(self):
        try:
            name = input("Enter author name to view details: ")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name, biography FROM authors WHERE name = %s", (name,))
            author = cursor.fetchone()
            if author:
                print(f"Author found: {author[0]}, Biography: {author[1]}")
            else:
                print(f"Author '{name}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    def display_authors(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM authors")
            authors = cursor.fetchall()
            if not authors:
                print("No authors available.")
            else:
                print("Authors available:")
                for author in authors:
                    print(f"Author: {author[0]}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

# Create an instance of the LibraryManagementSystem and run the main menu
if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    library_system.main_menu()