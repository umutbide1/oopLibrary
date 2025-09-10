import sqlite3

# Veritabanı dosyasının yolu, oluşan db ile aynı olmalı.
DB_FILE = "library.db"

def add_new_request_book(name, pages, writer, adder, url, price, added_date):
    """
    Parametre olarak verilen istek kitap bilgilerini veritabanina ekler.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Sütun adlarının request_books tablosuyla eşleştiğinden emin olun.
        sql_command = "INSERT INTO request_books (name, pages, writer, adder, url, price, added_date) VALUES (?, ?, ?, ?, ?, ?, ?)"

        book_data = (name, pages, writer, adder, url, price, added_date)

        cursor.execute(sql_command, book_data)
        conn.commit()
        
        print(f"\n[✓] '{name}' adli istek kitap veritabanina başariyla eklendi.")

    except sqlite3.Error as e:
        print(f"Veritabani hatasi oluştu: {e}")
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()