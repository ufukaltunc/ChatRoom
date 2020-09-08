# For GUI.
from tkinter import *
# For Communication.
from socket import socket, AF_INET, SOCK_STREAM
# For Multi-threading.
from threading import Thread

soket = socket(AF_INET, SOCK_STREAM)
soket.connect(('127.0.0.1', 7010))

def Mesaj_al(s): # Serverdan gelen mesajı alıp yazdırır
    while True:
        mesaj = s.recv(2048).decode('UTF-8')
        sohbet.insert(END, mesaj)

def Mesaj_yolla(*args): # Girilen mesajı servera gönderir
    mesaj = entry.get()
    sohbet.insert(END,"Ben: " + mesaj)
    soket.send(mesaj.encode('UTF-8'))
    entry.delete(0, END)

isim = ""
def isimbul(*args): # Girilen isime göre başlığı düzenler ve girilen isimi servera yollar
    global isim
    isim = entryisim.get()
    window.title(isim)
    soket.send(isim.encode('UTF-8'))
    login.destroy()
    window.deiconify()


window = Tk()
window.withdraw()
window.resizable(width=False, height=False)
window.geometry('600x400')
window.config(background="#222222")

############################################ Kayıt Menüsü
login = Toplevel()
login.title("Kayıt Ol")
login.resizable(width = False, height = False)
login.geometry('300x200')
login.config(background="#222222")

labelgiris = Label(login, text="Lütfen İsminizi Girin", bg="#222222", fg="white", font=('Times', '15'))
labelgiris.pack(side = TOP, pady=5)

entryisim = Entry(login, width=20, bg="#222222", fg="white", font=('Times', '15'))
entryisim.pack(side = TOP)
entryisim.bind("<Return>", isimbul)
entryisim.focus()

buton_isim = Button(login, text="Devam", width=10, height=1, bg="#222222", fg="white", font=('Times', '13'),
             command = isimbul)
buton_isim.pack(side = TOP, padx=10, pady=10)

############################################## ChatRoom
frame = Frame(window)
frame.config(background="#222222")
frame.pack()

entry = Entry(frame, width=48, bg="#222222", fg="white", font=('Times', '15'))
entry.pack(side=TOP, pady=5)
entry.bind("<Return>", Mesaj_yolla)
entry.focus()

buton = Button(frame, text="Yolla", width=10, bg="#222222", fg="white", font=('Times', '13'),
             command=Mesaj_yolla)
buton.pack(side=TOP, pady=8)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT,fill=Y)

sohbet = Listbox(frame, bg="#222222", fg="white", height=15, width=100, font=('Times', '15'),
              yscrollcommand=scrollbar.set)
sohbet.pack(side=LEFT, fill=BOTH)

receive = Thread(target=Mesaj_al, args=(soket,))
receive.start()

window.mainloop()