# uvicorn main:app --host 127.0.0.1 --port 8080




import mysql.connector

global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newpassword",
    database="pandeyji_eatery"
)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="newpassword",
            database="pandeyji_eatery"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def test_db_connection():
    connection = get_db_connection()
    if connection:
        print("Database connected successfully")
    else:
        print("Database connection failed")

def get_order_status(order_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed"
    cursor = connection.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    try:
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
    except Exception as e:
        print(f"SQL Error: {e}")
        result = None
    cursor.close()
    connection.close()
    return result[0] if result else None

def get_next_order_id():
    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return 1 if result is None else result + 1

def get_menu_item_id(food_item):
    connection = get_db_connection()
    if connection is None:
        return -1
    cursor = connection.cursor()
    query = "SELECT item_id FROM food_items WHERE name = %s"
    try:
        cursor.execute(query, (food_item,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"SQL Error: {e}")
        return -1
    finally:
        cursor.close()
        connection.close()

def insert_order_item(food_item, quantity, order_id):
    item_id = get_menu_item_id(food_item)
    if item_id is None:
        print(f"Error: Food item '{food_item}' not found in food_items table.")
        return -1
    if item_id == -1:
        return -1

    connection = get_db_connection()
    if connection is None:
        return -1
    cursor = connection.cursor()
    query = "INSERT INTO orders (item_id, quantity, order_id) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (item_id, quantity, order_id))
        connection.commit()
        cursor.close()
        connection.close()
        return 0
    except Exception as e:
        print(f"SQL Error: {e}")
        cursor.close()
        connection.close()
        return -1

def insert_order_tracking(order_id, status):
    connection = get_db_connection()
    if connection is None:
        return -1
    cursor = connection.cursor()
    query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    try:
        cursor.execute(query, (order_id, status))
        connection.commit()
        cursor.close()
        connection.close()
        return 0
    except Exception as e:
        print(f"SQL Error: {e}")
        cursor.close()
        connection.close()
        return -1

def get_total_order_price(order_id):
    connection = get_db_connection()
    if connection is None:
        return -1
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT SUM(fi.price * o.quantity) AS total_price
    FROM orders o
    JOIN food_items fi ON o.item_id = fi.item_id
    WHERE o.order_id = %s
    """
    try:
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['total_price'] if result and result['total_price'] is not None else 0
    except Exception as e:
        print(f"SQL Error: {e}")
        cursor.close()
        connection.close()
        return -1

if __name__ == "__main__":
    test_db_connection()
    print(f"Next Order ID: {get_next_order_id()}")
    print(f"Status of Order ID 1: {get_order_status(1)}")
    print(f"Status of Order ID 999: {get_order_status(999)}")
    # Example of inserting data (uncomment to run)
    # print(f"Insert Order Item Result: {insert_order_item('Pizza', 2, get_next_order_id())}")
    # next_id = get_next_order_id()
    # print(f"Insert Tracking Result: {insert_order_tracking(next_id, 'pending')}")
    # print(f"Total price of order 1: {get_total_order_price(1)}")