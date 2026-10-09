from db_connection import get_connection

#  UPDATE - Update client contact info
def update_client():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ClientID, ClientName, Phone, Email FROM Client")
    rows = cursor.fetchall()

    print("\n--- All Clients ---")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<13} {'Email'}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<13} {row[3]}")

    print("\n--- Update Client Contact Info ---")
    try:
        client_id = int(input("Enter the Client ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        conn.close()
        return

    cursor.execute("SELECT ClientName FROM Client WHERE ClientID = ?", (client_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"No client found with ID {client_id}.")
        conn.close()
        return

    print(f"\nUpdating contact info for: {result[0]}")
    new_phone = input("Enter new Phone (leave blank to keep current): ").strip()
    new_email = input("Enter new Email (leave blank to keep current): ").strip()

    if not new_phone and not new_email:
        print("No changes made.")
        conn.close()
        return

    if new_phone and new_email:
        cursor.execute(
            "UPDATE Client SET Phone = ?, Email = ? WHERE ClientID = ?",
            (new_phone, new_email, client_id)
        )
    elif new_phone:
        cursor.execute(
            "UPDATE Client SET Phone = ? WHERE ClientID = ?",
            (new_phone, client_id)
        )
    else:
        cursor.execute(
            "UPDATE Client SET Email = ? WHERE ClientID = ?",
            (new_email, client_id)
        )

    conn.commit()
    conn.close()
    print(f"Client ID {client_id} updated successfully.")

#  UPDATE - Update session status 
def update_session_status():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.SessionID, c.ClientName, sv.ServiceName, s.Date, s.Status
        FROM Session s
        JOIN Client  c  ON s.ClientID  = c.ClientID
        JOIN Service sv ON s.ServiceID = sv.ServiceID
        ORDER BY s.SessionID
    """)
    rows = cursor.fetchall()

    print("\n--- All Sessions ---")
    print(f"{'ID':<5} {'Client':<18} {'Service':<22} {'Date':<22} {'Status'}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<18} {row[2]:<22} {str(row[3]):<22} {row[4]}")

    print("\n--- Update Session Status ---")
    try:
        session_id = int(input("Enter the Session ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        conn.close()
        return

    cursor.execute("SELECT Status FROM Session WHERE SessionID = ?", (session_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"No session found with ID {session_id}.")
        conn.close()
        return

    print(f"Current status: {result[0]}")
    print("Available statuses: Scheduled / Completed / Cancelled")
    new_status = input("Enter new Status: ").strip()

    if new_status not in ("Scheduled", "Completed", "Cancelled"):
        print("Invalid status. Must be Scheduled, Completed, or Cancelled.")
        conn.close()
        return

    cursor.execute(
        "UPDATE Session SET Status = ? WHERE SessionID = ?",
        (new_status, session_id)
    )
    conn.commit()
    conn.close()
    print(f"Session ID {session_id} status updated to '{new_status}'.")