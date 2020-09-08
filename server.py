from socket import socket, AF_INET, SOCK_STREAM
from _thread import start_new_thread


s = socket(AF_INET, SOCK_STREAM) # Socket oluşturur

host = '127.0.0.1' # Sunucu ip tanımlar

port = 7010 # Bağlantı noktası tanımlar

s.bind((host, port)) # Ip ve portu birbirine bağlar

s.listen(5) # İstemcinin bağlanması için bekler
print("Sunucu Bekliyor")

clients = [] # İstemciler
clientisim = [] # İstemci isimleri
isim = ""

def Yeni_Kullanici(c):  # İstemci başlangıç mesajlarını gönderir ve mesaj gelmesi için bekler
    global isim
    for client in clients:
        if Client_No_Bul(client) < Client_No_Bul(c):
            ilkmesaj = ">> "+clientisim[Client_No_Bul(c)] + " Aramıza Katıldı"
            client.send(ilkmesaj.encode('UTF-8'))
    while True:
        mesaj = c.recv(2048).decode('UTF-8') # Gelen mesajı alıp Hepsine_Yolla fonksiyonu ile diğer istemcilere gönderir
        Hepsine_Yolla(mesaj, c)

clientNo = 0
def Client_No_Bul(conn): # İstenilen istemcinin numarasını bulup return eder.
    global clientNo
    clientNo = 0
    for client in clients:
        if client == conn:
            return clientNo
        clientNo = clientNo + 1
    return clientNo

def Hepsine_Yolla(mesaj, con): # Gelen mesajı diğer tüm istemcilere gönderir
    for client in clients:
        if client != con:   # Mesajı gönderen istemcinin numarasını kontrol eder
            toplumesaj = clientisim[Client_No_Bul(con)] + ": " + mesaj
            client.send(toplumesaj.encode('UTF-8')) #

while True:
    connect, addrss = s.accept() # Bağlantı gelene kadar bekler. Gelen bağlantıyı kabul eder

    isim = connect.recv(2048).decode('UTF-8')   # İstemci isimlerini alır
    clientisim.append(isim) # İstemci isimlerini diziye atar
    clients.append(connect)  # Yeni istemciyi diziye atar
    Client_No_Bul(connect)  # istemci numarısını bulur
    print(str(isim)+" : "+str(addrss)+" Bağlandı")

    start_new_thread(Yeni_Kullanici, (connect,))  # Gelen her bağlantı için yeni thread oluşturur