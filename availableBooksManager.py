import availableDatabase as adb # availableDatabase modülünü adb olarak içe aktarıyoruz
from datetime import date
from models import avaliableBooks # Sınıfımızı modeller dosyasından alıyoruz

# Kullanıcı Arayüzünden gelen bilgiler doğrultusunda database'e Mevcut kitap ekleyen kod bloğu
def add_available_book():
    """Kullanicidan kitap bilgilerini alir availableBook sinifindan bir nesne oluşturur bilgi aktarimini sağlar ve database'e ekler."""
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
    
    # Kullanıcıdan alınan bilgilerle bir 'avaliableBooks' nesnesi oluştur.
    new_book = avaliableBooks(
        name=name, 
        pages=pages, 
        writer=writer, 
        adder=adder, 
        added_date=added_date
    )
    # Oluşturulan nesnenin niteliklerini veritabanı fonksiyonuna gönder.
    adb.add_new_available_book(
        new_book.name, 
        new_book.pages, 
        new_book.writer, 
        new_book.adder, 
        new_book.added_date
    )


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
        adb.delete_book_by_id(book_id_to_delete)
        
    except ValueError:
        # Eğer kullanıcı sayı dışında bir şey girerse bu hata bloğu çalışır
        print("\n[!] Hata: Lütfen geçerli bir ID (sayı) girin.")
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")


def display_books_table():
    """Veritabanindan kitaplari alir ve tablo formatında ekrana yazdirir."""
    all_books = adb.get_all_available_books()
    
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

def update_available_book():
    """Kullanıcıdan ID alarak bir kitabı güncelleme işlemini yönetir."""
    print("\n--- Mevcut Kitap Bilgilerini Güncelle ---")
    display_books_table()
    
    try:
        # 1. Güncellenecek kitabın ID'sini al
        id_input = input("\nGüncellemek istediğiniz kitabın ID'sini girin (İptal için Enter'a basın): ")
        if not id_input:
            print("İşlem iptal edildi.")
            return
        
        book_id = int(id_input)
        
        # 2. O kitaba ait mevcut bilgileri veritabanından çek
        current_book = adb.get_book_by_id(book_id)
        
        if not current_book:
            print(f"\n[!] ID'si {book_id} olan bir kitap bulunamadı.")
            return

        print("\n--- Mevcut Bilgiler ---")
        print(f"Kitap Adı: {current_book['name']}")
        print(f"Yazar: {current_book['writer']}")
        print(f"Sayfa Sayısı: {current_book['pages']}")
        print("\nYeni bilgileri girin. Değiştirmek istemiyorsanız doğrudan Enter'a basın.")
        
        # 3. Kullanıcıdan yeni bilgileri al (Enter'a basarsa eskisi kalır)
        new_name = input(f"Yeni Kitap Adı [{current_book['name']}]: ") or current_book['name']
        new_writer = input(f"Yeni Yazar [{current_book['writer']}]: ") or current_book['writer']
        
        while True:
            new_pages_input = input(f"Yeni Sayfa Sayısı [{current_book['pages']}]: ")
            if not new_pages_input: # Enter'a basıldıysa
                new_pages = current_book['pages']
                break
            elif new_pages_input.isdigit(): # Sayı girildiyse
                new_pages = int(new_pages_input)
                break
            else:
                print("Hata: Lütfen geçerli bir sayfa sayısı girin.")

        # 4. Veritabanını yeni bilgilerle güncelle
        adb.update_book_by_id(book_id, new_name, new_writer, new_pages)

    except ValueError:
        print("\n[!] Hata: Lütfen geçerli bir ID (sayı) girin.")
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")
        
