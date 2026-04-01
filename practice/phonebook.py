import psycopg2
import csv
from config import DB_CONFIG

# -----------------------------
# Helper functions
# -----------------------------
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    phone VARCHAR(20) NOT NULL UNIQUE
                )
            """)
        conn.commit()
    print("Table ready.")

# -----------------------------
# Insert functions
# -----------------------------
def insert_from_csv(file_path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) != 2:
                        continue
                    first_name, phone = row
                    try:
                        cur.execute("INSERT INTO contacts (first_name, phone) VALUES (%s, %s)", (first_name, phone))
                    except psycopg2.errors.UniqueViolation:
                        conn.rollback()
                        print(f"Skipping duplicate phone: {phone}")
                    else:
                        conn.commit()
    print("CSV import done.")

def insert_from_console():
    first_name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO contacts (first_name, phone) VALUES (%s, %s)", (first_name, phone))
        conn.commit()
    print("Contact added.")

# -----------------------------
# Update functions
# -----------------------------
def update_contact():
    phone = input("Enter phone of contact to update: ").strip()
    new_name = input("New first name (leave blank to skip): ").strip()
    new_phone = input("New phone (leave blank to skip): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute("UPDATE contacts SET first_name=%s WHERE phone=%s", (new_name, phone))
            if new_phone:
                cur.execute("UPDATE contacts SET phone=%s WHERE phone=%s", (new_phone, phone))
        conn.commit()
    print("Contact updated.")

# -----------------------------
# Query functions
# -----------------------------
def query_contacts():
    print("1. By name")
    print("2. By phone prefix")
    choice = input("Choose filter: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == '1':
                name = input("Enter name to search: ").strip()
                cur.execute("SELECT first_name, phone FROM contacts WHERE first_name ILIKE %s", (f"%{name}%",))
            elif choice == '2':
                prefix = input("Enter phone prefix: ").strip()
                cur.execute("SELECT first_name, phone FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
            else:
                print("Invalid choice.")
                return
            rows = cur.fetchall()
            for r in rows:
                print(f"{r[0]} | {r[1]}")
            if not rows:
                print("No contacts found.")

# -----------------------------
# Delete function
# -----------------------------
def delete_contact():
    print("Delete by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Choose option: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == '1':
                name = input("Enter name: ").strip()
                cur.execute("DELETE FROM contacts WHERE first_name=%s", (name,))
            elif choice == '2':
                phone = input("Enter phone: ").strip()
                cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
            else:
                print("Invalid choice.")
                return
        conn.commit()
    print("Contact deleted.")

# -----------------------------
# Main menu
# -----------------------------
def main():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Choose option: ").strip()
        if choice == '1':
            path = input("Enter CSV file path: ").strip()
            insert_from_csv(path)
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()