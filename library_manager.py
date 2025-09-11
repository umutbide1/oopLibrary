from datetime import date
import availableDatabase as adb
import screenCleaner as sc
import availableBooksManager as abm 
import requestBookManager as rbm 
# availableBooksManager modülünü abm olarak içe aktarıyoruz ve o şekilde kullanıcaz.
# Artık şu şekilde kullabiliyoruz: abm.add_available_book() gibisinden.

    
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
        sc.clear_screen()
        if choice == '1':
            abm.add_available_book()
        elif choice == '2':
            abm.delete_available_book()
        elif choice == '3':
            abm.display_books_table()
        elif choice == '4':
            abm.update_available_book()
            pass
        elif choice == '5':
            print("Ana menüye dönülüyor...")
            break
        else:
            print("Geçersiz seçim!")
            
def handle_request_books():
    while True:
        choice = show_request_books_menu()
        sc.clear_screen()
        if choice == '1':
            rbm.add_request_book()
            pass
        elif choice == '2':
            rbm.delete_request_book()
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
        sc.clear_screen()
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
    adb.initialize_database()
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

