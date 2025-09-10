# Bu dosya, projenin veri modellerini (sınıflarını) barındırır.

class avaliableBooks():
    def __init__(self,name,pages,writer,adder,added_date):
        self.name = name
        self.pages = pages
        self.writer = writer
        self.adder = adder
        self.added_date = added_date
    
    def __repr__(self):
        return f"{self.name} - {self.writer} ({self.pages} sayfa, Ekleyen: {self.adder}, Tarih: {self.added_date})"
        
class requestBooks():
    def __init__(self,name,pages,writer,adder,url,price,added_date):
        self.name = name
        self.pages = pages
        self.writer = writer
        self.adder = adder
        self.url = url
        self.price = price
        self.added_date = added_date
        
class user():
    def __init__(self,name):
        self.name = name
