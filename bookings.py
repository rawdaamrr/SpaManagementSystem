from db_connection import get_connection


def generate_session_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(SessionID) FROM Session")
    last_id = cursor.fetchone()[0]
    conn.close()
    if last_id is None:
        return 1
    else:
        return last_id + 1


def show_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.SessionID, c.ClientName, t.TherapistName, sv.ServiceName,
               sp.SpaName, s.Date, s.Status
        FROM Session s
        JOIN Client    c  ON s.ClientID    = c.ClientID
        JOIN Therapist t  ON s.TherapistID = t.TherapistID
        JOIN Service   sv ON s.ServiceID   = sv.ServiceID
        JOIN Spa       sp ON s.SpaID       = sp.SpaID
        ORDER BY s.SessionID
    """)
    rows = cursor.fetchall()

    print("\n--- All Sessions ---")
    if not rows:
        print("No sessions found.")
    else:
        print(f"{'ID':<5} {'Client':<18} {'Therapist':<15} {'Service':<22} {'Spa':<18} {'Date':<22} {'Status'}")
        print("-" * 110)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<18} {row[2]:<15} {row[3]:<22} {row[4]:<18} {str(row[5]):<22} {row[6]}")

    conn.close()


def show_available_options():
    """Helper to display clients, therapists, services and spas before booking."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n-- Clients --")
    cursor.execute("SELECT ClientID, ClientName FROM Client")
    for r in cursor.fetchall():
        print(f"  {r[0]} - {r[1]}")

    print("\n-- Therapists --")
    cursor.execute("SELECT TherapistID, TherapistName FROM Therapist")
    for r in cursor.fetchall():
        print(f"  {r[0]} - {r[1]}")

    print("\n-- Services --")
    cursor.execute("SELECT ServiceID, ServiceName, ServicePrice FROM Service")
    for r in cursor.fetchall():
        print(f"  {r[0]} - {r[1]} ({r[2]} EGP)")

    print("\n-- Spas --")
    cursor.execute("SELECT SpaID, SpaName FROM Spa")
    for r in cursor.fetchall():
        print(f"  {r[0]} - {r[1]}")

    conn.close()

# INSERT - Book a new session
def add_session():
    show_available_options()

    print("\n--- Book New Session ---")
    try:
        session_id   = generate_session_id()
        client_id    = int(input("Enter Client ID: "))
        therapist_id = int(input("Enter Therapist ID: "))
        service_id   = int(input("Enter Service ID: "))
        spa_id       = int(input("Enter Spa ID: "))
        date         = input("Enter Date and Time (YYYY-MM-DD HH:MM:SS): ")
        status       = input("Enter Status (Scheduled / Completed / Cancelled): ")
    except ValueError:
        print("[Invalid input. IDs must be numbers.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Session (SessionID, ClientID, TherapistID, ServiceID, SpaID, Date, Status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, client_id, therapist_id, service_id, spa_id, date, status))

    conn.commit()
    conn.close()
    print(f"\nSession booked successfully with ID {session_id}.")

# DELETE - Delete a cancelled session by ID

def delete_session():
    conn = get_connection() #to show only cancelled ones
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.SessionID, c.ClientName, t.TherapistName, sv.ServiceName, s.Date
        FROM Session s
        JOIN Client    c  ON s.ClientID    = c.ClientID
        JOIN Therapist t  ON s.TherapistID = t.TherapistID
        JOIN Service   sv ON s.ServiceID   = sv.ServiceID
        WHERE s.Status = 'Cancelled'
    """)
    rows = cursor.fetchall()

    print("\n--- Cancelled Sessions ---")
    if not rows:
        print("No cancelled sessions found.")
        conn.close()
        return

    print(f"{'ID':<5} {'Client':<18} {'Therapist':<15} {'Service':<22} {'Date'}")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<18} {row[2]:<15} {row[3]:<22} {row[4]}")

    print("\n--- Delete Cancelled Session ---")
    try:
        session_id = int(input("Enter the Session ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        conn.close()
        return

    cursor.execute("SELECT SessionID FROM Session WHERE SessionID = ? AND Status = 'Cancelled'", (session_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"No cancelled session found with ID {session_id}.")
    else:
        cursor.execute("DELETE FROM Session_Product_Usage WHERE SessionID = ?", (session_id,))
        cursor.execute("DELETE FROM Session WHERE SessionID = ? AND Status = 'Cancelled'", (session_id,))
        conn.commit()
        print(f"Cancelled session ID {session_id} deleted successfully.")

    conn.close()
