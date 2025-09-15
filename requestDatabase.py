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


def delete_book_by_id(book_id_to_delete):
        """Verilen ID'ye sahip kitabi siler ve silinen kitabin adini mesajda gösterir."""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # SİLMEDEN ÖNCE: Kitabın adını öğrenmek için bir sorgu yapalım.
            cursor.execute("SELECT name FROM request_books WHERE id = ?", (book_id_to_delete,))
            book_to_delete = cursor.fetchone() # Sonucu al (None veya (isim,) şeklinde gelir)
            
            # 2. KONTROL: Eğer o ID'de bir kitap yoksa...
            if book_to_delete is None:
                print(f"\n[!] ID'si {book_id_to_delete} olan bir kitap bulunamadı.")
                return # Fonksiyondan çık

            book_name = book_to_delete[0]
            cursor.execute("DELETE FROM request_books WHERE id = ?", (book_id_to_delete,))
            conn.commit()
            print(f"\n[✓] '{book_name}' adlı kitap başarıyla silindi.")

        except sqlite3.Error as e:
            print(f"Veritabanı hatası oluştu: {e}")
            
        finally:
            if 'conn' in locals() and conn:
                conn.close()  

def get_all_request_books():
    """Veritabanındaki tüm mevcut kitapları bir liste olarak döndürür."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Tüm kitapları ID'ye göre sıralı bir şekilde seçiyoruz
        cursor.execute("SELECT id, name, writer, pages, adder, added_date FROM request_books ORDER BY id")
        
        all_books = cursor.fetchall()
        return all_books # Ham veriyi liste olarak döndür

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        return [] # Hata durumunda boş bir liste döndür
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def get_book_by_id(book_id):
    """Verilen ID'ye sahip tek bir kitabin tüm bilgilerini döndürür."""
    try:
        conn = sqlite3.connect(DB_FILE)
        # Veriyi sözlük gibi (sütun adlarıyla) almak için row_factory kullanıyoruz.
        # Bu sayede current_book['name'] gibi kullanımlar yapabiliyoruz.
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM request_books WHERE id = ?", (book_id,))
        book_data = cursor.fetchone() # Tek bir sonuç alıyoruz
        
        conn.close()
        return book_data # None (bulamazsa) veya bir satır nesnesi (bulursa) döndürür

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        return None
    


def update_book_by_id(book_id, name, pages, writer, adder, url, price, added_date):
    """Verilen ID'ye sahip kitabın bilgilerini günceller."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        sql_command = """
            UPDATE request_books
            SET name = ?,
                pages = ?,
                writer = ?,
                adder = ?,
                url = ?,
                price = ?,
                added_date = ?
            WHERE id = ?
        """
        
        cursor.execute(sql_command, (name, pages, writer, adder, url, price, added_date, book_id))
        conn.commit()
        
        print(f"\n[✓] '{name}' adlı kitap başarıyla güncellendi.")

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()