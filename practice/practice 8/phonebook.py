from connect import get_connection


# =========================
# CALL FUNCTION: search
# =========================
def search(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# =========================
# CALL PROCEDURE: upsert
# =========================
def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


# =========================
# CALL PROCEDURE: delete
# =========================
def delete(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()


# =========================
# CALL FUNCTION: pagination
# =========================
def get_page(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# =========================
# CALL PROCEDURE: bulk insert
# =========================
def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))

    conn.commit()
    cur.close()
    conn.close()


# =========================
# SIMPLE TEST MENU
# =========================
def menu():
    while True:
        print("\n--- PHONEBOOK (DB FUNCTIONS) ---")
        print("1. Search")
        print("2. Upsert")
        print("3. Delete")
        print("4. Pagination")
        print("5. Bulk insert test")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            p = input("Pattern: ")
            print(search(p))

        elif choice == "2":
            n = input("Name: ")
            ph = input("Phone: ")
            upsert(n, ph)

        elif choice == "3":
            v = input("Name or phone: ")
            delete(v)

        elif choice == "4":
            l = int(input("Limit: "))
            o = int(input("Offset: "))
            print(get_page(l, o))

        elif choice == "5":
            names = ["Ali", "Bob", "John"]
            phones = ["12345", "000", "999999"]
            bulk_insert(names, phones)

        elif choice == "6":
            break


if __name__ == "__main__":
    menu()