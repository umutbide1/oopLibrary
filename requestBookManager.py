import requestDatabase as rdb # requestDatabase modülünü rdb olarak içe aktarıyoruz
from datetime import date
from models import requestBook # Sınıfımızı modeller dosyasından alıyoruz
# Kullanıcı Arayüzünden gelen bilgiler doğrultusunda database'e Mevcut kitap ekleyen kod bloğu


def add_request_book():
    """Kullanicidan istek kitap bilgilerini alir, request tablosuna eklemek üzere database fonksiyonunu cagirir."""
    print("\n-- Yeni İstek Kitap Ekle --")
    name = input("Kitap Adi: ")
    
    while True:
        try:
            pages = int(input("Sayfa Sayisi: "))
            break
        except ValueError:
            print("Hata: Sayfa sayisi bir tam sayi olmalidir. Lütfen tekrar deneyin.")

    # Geçerli kullanıcı adlarını (küçük harfle) bir listede tanımladık.
    writer = input("Yazar: ")
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
            print("Hata: Geçersiz kullanici. Lütfen 'Umut' veya 'Beyza' isimlerinden birini girin.")
    while True:
        url = input("Kitabin alinabileceği URL: ")
        if url.startswith("http://") or url.startswith("https://"):
            break
        else:
            print("Lütfen geçerli bir URL girin (https:// ile başlamali).")
    while True:
        try:
            price = float(input("Kitabin fiyatı (örn. 29.99): "))
            if price < 0:
                print("Fiyat negatif olamaz. Lütfen tekrar deneyin.")
                continue
            break
        except ValueError:
            print("Hata: Fiyat sayisal bir değer olmalidir. Lütfen tekrar deneyin.")

    # Tarihi otomatik alıyoruz
    added_date = date.today().strftime("%Y-%m-%d")

    new_request_book=requestBook(
        name=name, 
        pages=pages, 
        writer=writer, 
        adder=adder, 
        url=url,
        price=price,
        added_date=added_date
    )
    # Tüm doğrulanmış bilgileri toplayıp, database modülündeki fonksiyona yolluyoruz.
    rdb.add_new_request_book(
        new_request_book.name,
        new_request_book.pages,
        new_request_book.writer,
        new_request_book.adder,
        new_request_book.url,
        new_request_book.price,
        new_request_book.added_date
    )


def delete_request_book():
    """Kullanicidan silinecek istek kitap ID'sini alir, request tablosundan silmek üzere database fonksiyonunu cagirir."""
    print("\n-- İstek Kitap Sil --")
    display_books_table() # Önce mevcut kitapları ve ID'lerini göster
    try:
        id_input = input("\nSilmek istediğiniz kitabin ID'sini girin (İptal için Enter'a basin): ")

        # Eğer kullanıcı bir şey girmeden Enter'a basarsa işlemi iptal et
        if not id_input:
            print("İşlem iptal edildi.")
            return

        # Girilen değerin bir sayı olduğundan emin ol, değilse hata verecek
        book_id_to_delete = int(id_input)
        
        # Yeni database fonksiyonumuzu çağırıyoruz
        rdb.delete_book_by_id(book_id_to_delete)
        
    except ValueError:
        # Eğer kullanıcı sayı dışında bir şey girerse bu hata bloğu çalışır
        print("\n[!] Hata: Lütfen geçerli bir ID (sayı) girin.")
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")

def display_books_table():
    """Veritabanindan kitaplari alir ve tablo formatında ekrana yazdirir."""
    all_books = rdb.get_all_request_books()
    
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


def update_request_book():
    """Kullanicidan ID alarak istek bir kitabi güncelleme işlemini yönetir."""
    print("\n--- İstek Kitap Bilgilerini Güncelle ---")
    display_books_table()
    
    try:
        # 1. Güncellenecek kitabın ID'sini al
        id_input = input("\nGüncellemek istediğiniz kitabın ID'sini girin (İptal için Enter'a basın): ")
        if not id_input:
            print("İşlem iptal edildi.")
            return
        
        book_id = int(id_input)
        
        # 2. O kitaba ait mevcut bilgileri veritabanından çek
        current_book = rdb.get_book_by_id(book_id)
        
        if not current_book:
            print(f"\n[!] ID'si {book_id} olan bir kitap bulunamadı.")
            return

        print("\n--- Mevcut Bilgiler ---")
        print(f"Kitap Adı: {current_book['name']}")
        print(f"Kitap Sayfasi: {current_book['pages']}")
        print(f"Yazar: {current_book['writer']}")
        print(f"Ekleyen Kisi: {current_book['adder']}")
        print(f"Kitap Url: {current_book['url']}")
        print(f"Kitap Fiyati: {current_book['price']}")
        print("\nYeni bilgileri girin. Değiştirmek istemiyorsanız doğrudan Enter'a basın.")
        
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

        # Diğer alanlar için de benzer şekilde
        new_adder = input(f"Yeni Ekleyen Kişi [{current_book['adder']}]: ") or current_book['adder']

        while True:
            new_url_input = input(f"Yeni URL [{current_book['url']}]: ")
            if not new_url_input: # Enter'a basıldıysa
                new_url = current_book['url']
                break
            elif new_url_input.startswith("http://") or new_url_input.startswith("https://"):
                new_url = new_url_input
                break
            else:
                print("Lütfen geçerli bir URL girin (https:// ile başlamalı).")

        while True:
            new_price_input = input(f"Yeni Fiyat [{current_book['price']}]: ")
            if not new_price_input: # Enter'a basıldıysa
                new_price = current_book['price']
                break
            try:
                new_price = float(new_price_input)
                if new_price < 0:
                    print("Fiyat negatif olamaz. Lütfen tekrar deneyin.")
                    continue
                break
            except ValueError:
                print("Hata: Fiyat sayısal bir değer olmalıdır. Lütfen tekrar deneyin.")
        # 4. Veritabanını yeni bilgilerle güncelle
        rdb.update_book_by_id(book_id,new_name,new_pages,new_writer,new_adder,new_url,new_price,current_book['added_date']  # Ekleme tarihini değiştirmiyoruz
)

    except ValueError:
        print("\n[!] Hata: Lütfen geçerli bir ID (sayı) girin.")
    except KeyboardInterrupt:
        print("\nİşlem iptal edildi.")