import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=LAPTOP-F1UC140D;'
        'DATABASE=SpaManagement;'
        'Trusted_Connection=yes;'
    )
    return conn

if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()

    print("Connected database:", cursor.execute("SELECT DB_NAME()").fetchone()[0])

    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)

    for row in cursor.fetchall():
        print(row)

    conn.close()