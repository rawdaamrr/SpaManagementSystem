from db_connection import get_connection

#  SELECT - View all services with their prices
def show_services():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ServiceID, ServiceName, Category, Duration, ServicePrice FROM Service")
    rows = cursor.fetchall()

    print("\n--- All Services ---")
    if not rows:
        print("No services found.")
    else:
        print(f"{'ID':<5} {'Service Name':<22} {'Category':<12} {'Duration':<12} {'Price (EGP)'}")
        print("-" * 65)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<22} {row[2]:<12} {str(row[3]):<12} {row[4]}")

    conn.close()

# SELECT - View all wellness products & stock
def show_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ProductID, ProductName, Price, StockQuantity FROM WellnessProduct")
    rows = cursor.fetchall()

    print("\n--- Wellness Products ---")
    if not rows:
        print("No products found.")
    else:
        print(f"{'ID':<5} {'Product Name':<28} {'Price (EGP)':<14} {'Stock'}")
        print("-" * 55)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<28} {row[2]:<14} {row[3]}")

    conn.close()

#  JOIN - Sessions with full client & service details
def show_session_details():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.SessionID,
            c.ClientName,
            c.Phone          AS ClientPhone,
            t.TherapistName,
            sv.ServiceName,
            sv.Category,
            sv.ServicePrice,
            sp.SpaName,
            sp.SpaLocation,
            s.Date,
            s.Status
        FROM Session s
        JOIN Client    c  ON s.ClientID    = c.ClientID
        JOIN Therapist t  ON s.TherapistID = t.TherapistID
        JOIN Service   sv ON s.ServiceID   = sv.ServiceID
        JOIN Spa       sp ON s.SpaID       = sp.SpaID
        ORDER BY s.Date DESC
    """)
    rows = cursor.fetchall()

    print("\n--- Session Details (with Client, Therapist, Service & Spa) ---")
    if not rows:
        print("No sessions found.")
    else:
        print(f"{'ID':<5} {'Client':<18} {'Phone':<13} {'Therapist':<15} {'Service':<22}"
              f" {'Category':<10} {'Price':<7} {'Spa':<18} {'Location':<22} {'Date':<22} {'Status'}")
        print("-" * 165)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<18} {row[2]:<13} {row[3]:<15} {row[4]:<22}"
                  f" {row[5]:<10} {row[6]:<7} {row[7]:<18} {row[8]:<22} {str(row[9]):<22} {row[10]}")

    conn.close()

#  JOIN - Therapists with their skills & spa name

def show_therapist_skills():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.TherapistID,
            t.TherapistName,
            t.Phone,
            ts.Skill,
            sp.SpaName,
            sp.SpaLocation
        FROM Therapist t
        JOIN Therapist_Skill ts ON t.TherapistID = ts.TherapistID
        JOIN Spa             sp ON t.SpaID        = sp.SpaID
        ORDER BY t.TherapistName
    """)
    rows = cursor.fetchall()

    print("\n--- Therapists with Skills & Spa ---")
    if not rows:
        print("No data found.")
    else:
        print(f"{'ID':<5} {'Therapist':<18} {'Phone':<13} {'Skill':<25} {'Spa':<18} {'Location'}")
        print("-" * 95)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<18} {row[2]:<13} {row[3]:<25} {row[4]:<18} {row[5]}")

    conn.close()
