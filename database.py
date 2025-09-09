import sqlite3

# Bu dosyanın sorumluluğundaki sabitler
DB_FILE = "library.db"

def initialize_database():
    """Veritabanini ve tablolari (eğer yoksa) oluşturur."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # MEVCUT KİTAPLAR TABLOSU
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS available_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pages TEXT,
            writer TEXT,
            adder TEXT,
            added_date TEXT
        )
    ''')

    # İSTEK KİTAPLAR TABLOSU
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pages TEXT,
            writer TEXT,
            requester TEXT,
            url1 TEXT,
            price1 TEXT,
            url2 TEXT,
            price2 TEXT
        )
    ''')
    
    # KULLANICILAR TABLOSU
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()
    print("Veritabanı modülü başarıyla başlatıldı.")

# Database kısmı tamamlandı. Database e istek kısımlarının fonksiyon tanımlamaları kısmı başlatıldı.
# Burada sadece database ekle çıkar güncelle vs işlemleri var
# library_manager.py dosyasında kullanıcıdan bilgiler alınacak ve buraya atılacak.
# Yani aslında her ekleme fonksiyonuna karşılık db ye kayıt için de fonksiyon var.
def add_new_available_book(name, pages, writer, adder, added_date):
    """
    Parametre olarak verilen kitap bilgilerini veritabanına ekler.
    Bu fonksiyon KESİNLİKLE input() kullanmaz!
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        sql_command = "INSERT INTO available_books (name, pages, writer, adder, added_date) VALUES (?, ?, ?, ?, ?)"
        
        # Parametre olarak gelen verileri kullanıyoruz
        book_data = (name, pages, writer, adder, added_date)
        
        cursor.execute(sql_command, book_data)
        conn.commit()
        
        print(f"\n[✓] '{name}' adlı kitap veritabanına başarıyla eklendi.")

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    print(f"'{name}' adlı kitap veritabanına başarıyla eklendi!")

# Kitap silme fonksiyonu database için
def delete_book_by_id(book_id):
    """Verilen ID'ye sahip kitabı siler ve silinen kitabın adını mesajda gösterir."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 1. SİLMEDEN ÖNCE: Kitabın adını öğrenmek için bir sorgu yapalım.
        cursor.execute("SELECT name FROM available_books WHERE id = ?", (book_id,))
        book_to_delete = cursor.fetchone() # Sonucu al (None veya (isim,) şeklinde gelir)
        
        # 2. KONTROL: Eğer o ID'de bir kitap yoksa...
        if book_to_delete is None:
            print(f"\n[!] ID'si {book_id} olan bir kitap bulunamadı.")
            return # Fonksiyondan çık

        # Kitabın adını değişkene alalım. book_to_delete[0] -> ('Martin Eden',)[0] -> 'Martin Eden'
        book_name = book_to_delete[0]

        # 3. SİLME İŞLEMİ: Artık kitabı silebiliriz.
        cursor.execute("DELETE FROM available_books WHERE id = ?", (book_id,))
        conn.commit()
        
        # 4. BİLGİLENDİRME: Öğrendiğimiz ismi kullanarak mesajı yazdır.
        print(f"\n[✓] '{book_name}' adlı kitap başarıyla silindi.")

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()  
def get_all_available_books():
    """Veritabanındaki tüm mevcut kitapları bir liste olarak döndürür."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Tüm kitapları ID'ye göre sıralı bir şekilde seçiyoruz
        cursor.execute("SELECT id, name, writer, pages, adder, added_date FROM available_books ORDER BY id")
        
        all_books = cursor.fetchall()
        return all_books # Ham veriyi liste olarak döndür

    except sqlite3.Error as e:
        print(f"Veritabanı hatası oluştu: {e}")
        return [] # Hata durumunda boş bir liste döndür
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()