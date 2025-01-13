import mysql.connector

# Establishing the connection b/w to MySQL
try:
    connection = mysql.connector.connect(
        host="localhost",      # Replace with your MySQL server address
        user="root",           # Replace with your MySQL username
        password="dbPassword",  # Replace with your MySQL password
        database="test_db"     # Replace with your database name or create one using SQL
    )
    
    if connection.is_connected():
        print("Connected to MySQL!")
        cursor = connection.cursor()
        
        # Step 1: Create a table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT
        )
        """)
        print("Table 'users' created or already exists.")

        # Step 2: Inserting data into the table
        insert_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
        values = [
            ("Alice", 25),
            ("Bob", 30),
            ("Charlie", 22)
        ]
        cursor.executemany(insert_query, values)
        connection.commit()  # Commit changes to the database
        print("Inserted sample data into 'users' table.")

        # Step 3: Query the data
        cursor.execute("SELECT * FROM users")
        print("\nData in 'users' table:")
        for row in cursor.fetchall():
            print(row)

        # Keep connection open for additional queries
        while True:
            query = input("\nEnter an SQL query (or type 'exit' to quit): ")
            if query.lower() == 'exit':
                break
            
            try:
                cursor.execute(query)
                if query.strip().lower().startswith("select"):
                    for row in cursor.fetchall():
                        print(row)
                else:
                    connection.commit()  # Commit if it's an insert/update/delete query
                    print("Query executed successfully.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the connection when done
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("\nConnection closed.")
