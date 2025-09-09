from datetime import date
import database
import os
import platform

# Mevcut Kitaplar için nesne üretilecek sınıf tanımlaması
class avaliableBooks():
    def __init__(self,name,pages,writer,adder,added_date):
        self.name = name
        self.pages = pages
        self.writer = writer
        self.adder = adder
        self.added_date = added_date
    
    def __repr__(self):
        return f"{self.name} - {self.writer} ({self.pages} sayfa, Ekleyen: {self.adder}, Tarih: {self.added_date})"
        
# İstek Kitaplar için nesne üretilecek sınıf tanımlaması    
class requestBook():
    def __init__(self,name,pages,writer,requester,url1,price1,url2,price2):
        self.name = name
        self.pages = pages
        self.writer = writer
        self.requester = requester
        self.url1 = url1
        self.price1 = price1
        self.url2 = url2
        self.price2 = price2
        
# Kullanıcı işlemleri için nesne üretilecek sınıf tanımlaması    
class user():
    def __init__(self,name):
        self.name = name
        

# Kullanıcı Arayüzünden gelen bilgiler doğrultusunda database'e Mevcut kitap ekleyen kod bloğu
def add_available_book():
    """Kullanicidan kitap bilgilerini alir, doğrular ve database fonksiyonunu cagirir."""
    print("\n-- Yeni Kitap Ekle --")
    name = input("Kitap Adi: ")
    writer = input("Yazar: ")
    
    while True:
        try:
            pages = int(input("Sayfa Sayisi: "))
            break
        except ValueError:
            print("Hata: Sayfa sayisi bir tam sayı olmalidir. Lütfen tekrar deneyin.")

    # Geçerli kullanıcı adlarını (küçük harfle) bir listede tanımladık.
    valid_users = ["umut", "beyza"]
    
    # Doğru kullanıcı adı girilene kadar dönecek bir döngü başlattık
    while True:
        adder_input = input("Ekleyen Kişi (Umut veya Beyza): ")
        
        # Girilen ismin küçük harfe çevrilmiş halini listede kontrol et
        if adder_input.lower() in valid_users:
            # Veritabanına daha düzgün görünsün diye ilk harfi büyük kaydededilir.
            adder = adder_input.capitalize() 
            break
        else:
            # 6. Eğer isim geçersizse, hata mesajı göster ve döngü devam etsin.
            print("Hata: Geçersiz kullanıcı. Lütfen 'Umut' veya 'Beyza' isimlerinden birini girin.")
    
    # --- KONTROL BLOĞU BİTTİ ---

    # Tarihi otomatik alıyoruz
    added_date = date.today().strftime("%Y-%m-%d")

    # Tüm doğrulanmış bilgileri toplayıp, database modülündeki fonksiyona yolluyoruz.
    database.add_new_available_book(name, pages, writer, adder, added_date)


def delete_available_book():
    """Kullanıcıdan ID alarak silme işlemini yönetir."""
    print("\n--- Mevcut Listeden Kitap Sil ---")
    display_books_table() # Önce mevcut kitapları ve ID'lerini göster
    
    try:
        id_input = input("\nSilmek istediğiniz kitabın ID'sini girin (İptal için Enter'a basın): ")
        
        # Eğer kullanıcı bir şey girmeden Enter'a basarsa işlemi iptal et
        if not id_input:
            print("İşlem iptal edildi.")
            return

        # Girilen değerin bir sayı olduğundan emin ol, değilse hata verecek
        book_id_to_delete = int(id_input)
        
        # Yeni database fonksiyonumuzu çağırıyoruz
        database.delete_book_by_id(book_id_to_delete)
        
    except ValueError:
        # Eğer kullanıcı sayı dışında bir şey girerse bu hata bloğu çalışır
        print("\n[!] Hata: Lütfen geçerli bir ID (sayı) girin.")
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")


def display_books_table():
    """Veritabanından kitapları alır ve tablo formatında ekrana yazdırır."""
    all_books = database.get_all_available_books()
    
    print("\n--- Kütüphanedeki Mevcut Kitaplar ---")
    if not all_books:
        print("Kütüphanede hiç mevcut kitap bulunmuyor.")
        return

    print(f"{'ID':<4} | {'Kitap Adı':<30} | {'Yazar':<25} | {'Sayfa':>5} | {'Ekleyen':<10}")
    print("-" * 85)
    for book in all_books:
        # book[0]=id, book[1]=name, book[2]=writer, book[3]=pages, book[4]=adder
        print(f"{book[0]:<4} | {book[1]:<30} | {book[2]:<25} | {str(book[3]):>5} | {book[4]:<10}")
    print("-" * 85)

def show_available_books_menu():
    print("\n -- Mevcut Kitaplar --")
    print("1-) Mevcut Listeye Kitap Ekle ")
    print("2-) Mevcut Listeden Kitap Sil ")
    print("3-) Mevcut Kitaplari Listele ")
    print("4-) Mevcut kitap bilgilerini güncelle ")
    print("5-) Ana Menüye Dön ")
    choice = input("Seçiminiz: ")
    return choice
    
def show_request_books_menu():
    print("\n -- İstek Kitaplar --")
    print("1-) İstek Listesine Kitap Ekle ")
    print("2-) İstek Listesinden Kitap Sil ")
    print("3-) İstek Kitaplari Listele ")
    print("4-) İstek kitap bilgilerini güncelle ")
    print("5-) Ana Menüye Dön ")
    choice = input("Seçiminiz: ")
    return choice
    
def show_users_menu():
    print("\n -- Kullanıcılar --")
    print("1-) Kullanici Ekle ")
    print("2-) Kullanici Sil ")
    print("3-) Kullanicileri Listele ")
    print("4-) Ana Menüye Dön ")
    choice = input("Seçiminiz: ")
    return choice

def show_main_menu():
    print("\n========= ANA MENÜ =========")
    print("1. Mevcut Kitap İşlemleri")
    print("2. İstek Kitap İşlemleri")
    print("3. Yönetici İşlemleri")
    print("4. Programı Kapat")
    choice = input("Seçiminiz: ")
    return choice
  
def handle_available_books():
    while True:
        choice = show_available_books_menu()
        clear_screen()
        if choice == '1':
            add_available_book()
        elif choice == '2':
            delete_available_book()
        elif choice == '3':
            display_books_table()
        elif choice == '4':
            print("[!] Mevcut kitap güncelleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '5':
            print("Ana menüye dönülüyor...")
            break
        else:
            print("Geçersiz seçim!")
            
def handle_request_books():
    while True:
        choice = show_request_books_menu()
        clear_screen()
        if choice == '1':
            print("[!] İstek kitap ekleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '2':
            print("[!] İstek kitap silme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '3':
            print("[!] İstek kitap listeleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '4':
            print("[!] İstek kitap güncelleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '5':
            print("Ana menüye dönülüyor...")
            break
        else:
            print("Geçersiz seçim!")

def handle_admins():
    while True:
        choice = show_users_menu()
        clear_screen()
        if choice == '1':
            print("[!] Yönetici ekleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '2':
            print("[!] Yöneticileri listeleme fonksiyonu yakında eklenecek.")
            pass
        elif choice == '3':
            print("Ana menüye dönülüyor...")
            break
        else:
            print("Geçersiz seçim!")
            
def main():
    database.initialize_database()
    while True:
        choice = show_main_menu()
        if choice == '1':
            handle_available_books() # Mevcut kitaplar menüsüne git
        elif choice == '2':
            handle_request_books() # İstek kitaplar menüsüne git
        elif choice == '3':
            handle_admins() # Yönetici menüsüne git
        elif choice == '4':
            print("Program kapatıldı.")
            break # Ana döngüyü kır ve programı sonlandır.
        else:
            print("Geçersiz seçim! Lütfen 1-4 arasında bir sayı girin.")

def clear_screen():
    """İşletim sistemine göre terminal ekranını temizler."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')