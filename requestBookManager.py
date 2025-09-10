import requestDatabase as qdb # requestDatabase modülünü qdb olarak içe aktarıyoruz
from datetime import date
from models import requestBooks # Sınıfımızı modeller dosyasından alıyoruz

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
    qdb.add_new_request_book(
        name,
        pages,
        writer,
        adder,
        url,
        price,
        added_date
    )


#   BURADA KALINDI 