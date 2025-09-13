import requestDatabase as rdb # requestDatabase modülünü rdb olarak içe aktarıyoruz
from datetime import date
from models import requestBooks # Sınıfımızı modeller dosyasından alıyoruz
import availableBooksManager as abm
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

    new_requestBook=requestBooks(
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
        name,
        pages,
        writer,
        adder,
        url,
        price,
        added_date
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
    all_books = rdb.get_all_available_books()
    
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