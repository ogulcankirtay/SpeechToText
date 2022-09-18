from cgitb import text
import os
from re import M
from tkinter import Button, Menu, Tk, TkVersion, ttk
from tkinter import BOTH, END, RAISED, RIGHT, Entry, Label, Listbox, StringVar,filedialog, messagebox, simpledialog
import time
import tkinter as tk
from PIL import Image,ImageTk
from tkinter.tix import IMAGE
from asyncio.windows_events import NULL
from multiprocessing import connection
import threading
import speech_recognition as sr
import firebase_admin
from firebase_admin import credentials,firestore
import chunk
from email.mime import audio
from  pydub import AudioSegment
from pydub.utils import make_chunks
import soundfile as sf
import time
import datetime
from datetime import date

gui=Tk()
gui.title('Ses Dönüştürücü')
gui.geometry('400x500')
gui.resizable(False,False)
gui.configure(background="#4a4a4a")


cred = credentials.Certificate("Key.json")
app=firebase_admin.initialize_app(cred)
db=firestore.client()

bugun = datetime.date.today()

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    ##listbox.delete(0,END)
    i=0
    for doc in doc_snapshot:
        
       ## listbox.insert(i,doc.to_dict().get("metin"))
        print(f'Received document snapshot: {doc.to_dict()}')
        i+=1
    callback_done.set()

doc_ref = db.collection(u'Data')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

##initilaze 
r = sr.Recognizer()

def addData(data):
    doc=db.collection("Data").add(data)

def Cevir():        
    metin=""
    if(path==NULL):
           print("hata") 
           messagebox.showerror('Python Error', 'Lütfen dosya Seçiniz')
    
    else:
        myaudio=AudioSegment.from_wav(path)
        chunks_length= 8000
        f= sf.SoundFile(path)
        basename = os.path.basename(path)
        print(basename)
        ##print('seconds = {}'.format((f.frames / f.samplerate)*1000))
        zaman=int((f.frames / f.samplerate)/8)
        chunks=make_chunks(myaudio,chunks_length)
        for i,chunk in enumerate(chunks):
            chunkname=path+"_{0}.wav".format(i)
            print("exporting",chunkname)
            chunk.export(chunkname,format="wav")
            file=chunkname
            print(file)
            r=sr.Recognizer()
            
            gui.update_idletasks()
            time.sleep(1)
            bilgi="Ses Dosyanız Dönüştürülüyor Lütfen bekleyiniz.. "+str(zaman)
            text.set(bilgi)  
            zaman-=1
            with sr.AudioFile(file) as source:
                r.adjust_for_ambient_noise(source)
                print("Arka plan gürültüsü:" + str(r.energy_threshold))
                try:
                    ses = r.listen(source)
                  #  T.delete("1.0","end")
   
                    metin+="\n"+r.recognize_google(ses, language='tr-tr')
                   # T.insert(tk.INSERT,metin)
                
                    print("seeeee  "+metin)
                except sr.WaitTimeoutError:
                    print("Dinleme zaman aşımına uğradı")
                    messagebox.showinfo("showinfo", "Dinleme zaman aşımına uğradı") 
                    #T.delete("1.0","end")
                    #T.insert(tk.INSERT,"Dinleme zaman aşımına uğradı")
                except sr.UnknownValueError:
                    print("Ne dediğini anlayamadım")
                    #T.delete("1.0","end")
                    messagebox.showinfo("showinfo", "Ne dediğini anlayamadım") 
                    #T.insert(tk.INSERT,"Ne dediğini anlayamadım")
                except sr.RequestError:
                    print("İnternete bağlanamıyorum")
                    messagebox.showinfo("showinfo", "İnternete bağlanamıyorum") 
                    #T.delete("1.0","end")
                    #T.insert(tk.INSERT,"İnternete bağlanamıyorum")
    
    zaman=0
    dosya_Adı=basename+"-"+str(bugun)+".txt"
    bilgi="Ses Dosyanız Dönüştürülüyor Lütfen bekleyiniz.. "+str(zaman)
    text.set("")
    if(metin!=""):
            #dosya=open(dosya_Adı,"w",encoding='utf-8')
            #dosya.write(metin)
            kaydet(metin)
            data={'metin':metin}
            messagebox.showinfo("showinfo", "Dosyanız İndirilmiştir.")                    
            addData(data)
    ##    sender=popup()
    ##    if(sender!=NULL):
    ##        SendMessage(metin,sender)
           
   

def ac():
    global path
    gui.filename=filedialog.askopenfilename(title="Select File",filetypes=(("wav files","*.wav"),("all files","*.*")))
    path=gui.filename
    print(path)


def kaydet(metin):
    file=filedialog.asksaveasfile(defaultextension=".txt",
                                  filetypes=[
                                      ("Text file",".txt")
                                  ])
    file.write(metin)
    file.close()


# create an instance of progress bar
my_menu=Menu(gui)
gui.config(menu=my_menu)
#create menu item
file_menu=Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="Aç",command=ac)

#logo

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("Record.png"))


label = Label(gui, image = img,background="#4a4a4a")
label.pack(padx=5,pady=5)

start_btn=Button(gui,bg="black",text="Çevir",fg="white",command=Cevir,font="arial 20")

start_btn.pack(padx=2)
# string variable

text = tk.StringVar()
text.set("")
z=tk.Label(gui, textvariable=text,   bg = '#4a4a4a',
    fg = '#fff')

z.pack(padx=5,pady=5)





gui.mainloop()