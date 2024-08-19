import mysql.connector


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elias928",
        database="library_management_system"
    )
    return connection




def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Create Authors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        biography TEXT
    )
    """)

    # Create Books Table with Genre
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author_id INT,
        genre VARCHAR(255),
        isbn VARCHAR(13) NOT NULL,
        publication_date DATE,
        availability BOOLEAN DEFAULT 1,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )
    """)

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        library_id VARCHAR(10) NOT NULL UNIQUE
    )
    """)

    # Create Borrowed Books Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowed_books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        book_id INT,
        borrow_date DATE NOT NULL,
        return_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()