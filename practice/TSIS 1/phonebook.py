import psycopg2
import csv
import json
import os
from datetime import date
from config import params

# Helper to handle date serialization for JSON
class DateEncoder(json.JSONEncoder):#subclass of JSONEncoder
    def default(self, obj):#called when unknown data appeared
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def get_connection():
    return psycopg2.connect(**params)

# --- 1. DATA ENTRY (CSV & CONSOLE) ---

def import_from_csv(filename):
    try:
        conn = get_connection()
        cur = conn.cursor()
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Add/Get Group
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id", (row['group'],))
                group_id = cur.fetchone()[0]
                # Add/Update Contact
                cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET email = EXCLUDED.email RETURNING id",
                            (row['name'], row['email'], row['birthday'], group_id))
                contact_id = cur.fetchone()[0]
                # Add Phone
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (contact_id, row['phone'], row['type']))
        conn.commit()
        print(f"Successfully imported {filename}")
    except Exception as e:
        print(f"CSV Error: {e}")
    finally:
        if conn: conn.close()

# --- 2. STORED PROCEDURE WRAPPERS ---

def add_new_phone(name, phone, p_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))
    conn.commit()
    print(f"Phone added for {name}")
    conn.close()

def move_contact_group(name, group):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    print(f"{name} moved to {group}")
    conn.close()

# --- 3. ADVANCED SEARCH & PAGINATION ---

def search_all(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    results = cur.fetchall()
    for row in results:
        print(f"Name: {row[0]} | Email: {row[1]} | Phones: {row[2]} | Group: {row[3]}")
    conn.close()

def view_paginated():
    page = 0
    limit = 5
    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, email FROM contacts ORDER BY name LIMIT %s OFFSET %s", (limit, page * limit))
        rows = cur.fetchall()
        print(f"\n--- Page {page + 1} ---")
        for r in rows: print(f"{r[0]} ({r[1]})")
        
        move = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if move == 'n' and len(rows) == limit: page += 1
        elif move == 'p' and page > 0: page -= 1
        elif move == 'q': break
        conn.close()

# --- 4. JSON IMPORT / EXPORT ---

def export_json(filename="phonebook.json"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name as group_name, 
        ARRAY_AGG(p.phone || ':' || p.type) as phone_data 
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """)#collects multiple rows into an array
    rows = cur.fetchall()
    data = []
    for r in rows:
        data.append({"name": r[0], "email": r[1], "birthday": r[2], "group": r[3], "phones": r[4]})
    
    with open(filename, 'w') as f:
        json.dump(data, f, cls=DateEncoder, indent=4)
    print(f"Data exported to {filename}")
    conn.close()
    
def import_json(filename="phonebook.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        conn = get_connection()
        cur = conn.cursor()
        for entry in data:
            # Check if contact exists
            cur.execute("SELECT id FROM contacts WHERE name = %s", (entry['name'],))
            exists = cur.fetchone()
            
            if exists:
                choice = input(f"\nContact '{entry['name']}' already exists. Overwrite? (y/n): ")
                if choice.lower() != 'y':
                    continue
                cur.execute("DELETE FROM contacts WHERE name = %s", (entry['name'],))

            # Use your existing procedure to handle group and contact creation
            cur.execute("CALL move_to_group(%s, %s)", (entry['name'], entry['group']))
            cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE name=%s", 
                        (entry.get('email'), entry.get('birthday'), entry['name']))
            
            # Re-insert phones
            for p_str in entry.get('phones', []):
                if p_str:
                    phone, p_type = p_str.split(':')
                    cur.execute("CALL add_phone(%s, %s, %s)", (entry['name'], phone, p_type))
        
        conn.commit()
        print("JSON Import complete.")
    except Exception as e:
        print(f"JSON Import Error: {e}")
    finally:
        if conn: conn.close()

# --- 5. MAIN CONSOLE INTERFACE ---

def main_menu():
    while True:
        print("\n--- PhoneBook TSIS 1 ---")
        print("1. Import CSV")
        print("2. Search Contacts")
        print("3. View All (Paginated)")
        print("4. Add Phone to existing contact")
        print("5. Move contact to group")
        print("6. Export to JSON")
        print("0. Exit")
        
        choice = input("Select: ")
        if choice == '1':
            path = input("CSV Filename: ")
            import_from_csv(path)
        elif choice == '2':
            q = input("Search query: ")
            search_all(q)
        elif choice == '3':
            view_paginated()
        elif choice == '4':
            n = input("Name: "); p = input("Phone: "); t = input("Type (home/work/mobile): ")
            add_new_phone(n, p, t)
        elif choice == '5':
            n = input("Name: "); g = input("New Group Name: ")
            move_contact_group(n, g)
        elif choice == '6':
            export_json()
        elif choice == '0':
            break

if __name__ == "__main__":
    main_menu()