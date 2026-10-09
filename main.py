from clients import *
from bookings import *
from operations import *
from inquiries import *

while True:
    print("\n==================================")
    print("      BEAUTY & WELLNESS SYSTEM    ")
    print("==================================")
    print("--- Client Management ---")
    print("1 - Add New Client")
    print("2 - Show All Clients")
    print("3 - Delete Client")
    print("4 - Update Client Contact Info")
    print("")
    print("--- Session / Booking Management ---")
    print("5 - Book New Session")
    print("6 - Show All Sessions")
    print("7 - Delete Cancelled Session")
    print("8 - Update Session Status")
    print("")
    print("--- Inquiries ---")
    print("9  - View All Services")
    print("10 - View All Wellness Products")
    print("11 - Session Details")
    print("12 - Therapist Skills & Spa")
    print("")
    print("0 - Exit")
    print("==================================")

    choice = input("Enter choice: ")

    if choice == "1":
        add_client()

    elif choice == "2":
        show_clients()

    elif choice == "3":
        delete_client()

    elif choice == "4":
        update_client()

    elif choice == "5":
        add_session()

    elif choice == "6":
        show_sessions()

    elif choice == "7":
        delete_session()

    elif choice == "8":
        update_session_status()

    elif choice == "9":
        show_services()

    elif choice == "10":
        show_products()

    elif choice == "11":
        show_session_details()

    elif choice == "12":
        show_therapist_skills()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
