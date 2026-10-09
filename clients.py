from db_connection import get_connection


def generate_client_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ClientID) FROM Client")
    last_id = cursor.fetchone()[0]
    conn.close()
    if last_id is None:
        return 1
    else:
        return last_id + 1



#  INSERT - Add a new client
def add_client():
    conn = get_connection()
    cursor = conn.cursor()

    client_id = generate_client_id()

    print("\n--- Add New Client ---")
    name   = input("Enter Client Name: ")
    gender = input("Enter Gender (Male/Female): ")
    phone  = input("Enter Phone (11 digits): ")
    email  = input("Enter Email: ")
    date   = input("Enter Membership Date (YYYY-MM-DD): ")

    cursor.execute("""
        INSERT INTO Client (ClientID, ClientName, Gender, Phone, Email, MembershipDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_id, name, gender, phone, email, date))

    conn.commit()
    conn.close()
    print(f"\n Client '{name}' added successfully with ID {client_id}.")


#  SELECT - Show all clients
def show_clients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()

    print("\n--- All Clients ---")
    if not rows:
        print("No clients found.")
    else:
        print(f"{'ID':<5} {'Name':<20} {'Gender':<8} {'Phone':<13} {'Email':<25} {'Member Since'}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<8} {row[3]:<13} {row[4]:<25} {row[5]}")

    conn.close()


#  DELETE - Remove a client by ID-
def delete_client():
    conn = get_connection()
    cursor = conn.cursor()

    show_clients()

    print("\n--- Delete Client ---")
    try:
        client_id = int(input("Enter the Client ID to delete: "))
    except ValueError:
        print(" Invalid input. Please enter a number.")
        conn.close()
        return

    # CASE 1: Client doesn't exist
    cursor.execute("SELECT ClientName FROM Client WHERE ClientID = ?", (client_id,))
    result = cursor.fetchone()

    if result is None:
        print(f" No client found with ID {client_id}.")
        conn.close()
        return

    client_name = result[0]

    # Check completed or scheduled sessions
    cursor.execute("""
        SELECT COUNT(*) FROM Session 
        WHERE ClientID = ? AND Status IN ('Completed', 'Scheduled')
    """, (client_id,))
    active_count = cursor.fetchone()[0]

    # Check cancelled sessions
    cursor.execute("""
        SELECT COUNT(*) FROM Session 
        WHERE ClientID = ? AND Status = 'Cancelled'
    """, (client_id,))
    cancelled_count = cursor.fetchone()[0]

    # CASE 2A: Client has completed or scheduled sessions → block
    if active_count > 0:
        print(f"\n Cannot delete '{client_name}'.")
        print(f"  They have {active_count} Completed/Scheduled session(s) on record.")
        print("        Cannot delete a client with active history.")

    # CASE 2B: Client has ONLY cancelled sessions → allow with cleanup
    elif cancelled_count > 0:
        print(f"\n Client '{client_name}' has {cancelled_count} cancelled session(s).")
        print("  Deleting this client will also delete those cancelled sessions.")
        confirm = input("Are you sure you want to proceed? (yes/no): ")
        if confirm.lower() == 'yes':
            # Delete product usage of cancelled sessions first
            cursor.execute("""
                DELETE FROM Session_Product_Usage
                WHERE SessionID IN (
                    SELECT SessionID FROM Session 
                    WHERE ClientID = ? AND Status = 'Cancelled'
                )
            """, (client_id,))
            # Delete cancelled sessions
            cursor.execute("""
                DELETE FROM Session 
                WHERE ClientID = ? AND Status = 'Cancelled'
            """, (client_id,))
            # Delete client
            cursor.execute("DELETE FROM Client WHERE ClientID = ?", (client_id,))
            conn.commit()
            print(f" Client '{client_name}' and their cancelled sessions deleted successfully.")
        else:
            # CASE 4: User said no
            print("Deletion cancelled.")

    # CASE 3: Client has no sessions at all → delete directly
    else:
        confirm = input(f"Are you sure you want to delete '{client_name}'? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM Client WHERE ClientID = ?", (client_id,))
            conn.commit()
            print(f" Client '{client_name}' deleted successfully.")
        else:
            # CASE 4: User said no
            print("Deletion cancelled.")

    conn.close()