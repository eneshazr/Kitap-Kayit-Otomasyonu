from tkinter import * 
from tkinter import ttk, messagebox
import sqlite3
import webbrowser

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        F1 = Frame(self.master)
        F1.pack(pady=15, padx=25)

        self.F_listele = Frame(self.master)
        self.F_ekle = Frame(self.master)

        B1 = Button(F1,text="Kitap Ekle",command=self.ekle, font="bold", cursor="hand2", fg="red", width = 13, height=3)
        B1.grid(row=0, column=0, padx=20)
        B2 = Button(F1,text="Kitap Listele",command=self.listele, font="bold", cursor="hand2", fg="green", width = 13, height=3)
        B2.grid(row=0, column=1)
        self.baglanti = sqlite3.connect("baglan.sql", check_same_thread=True)
        self.im = self.baglanti.cursor()

    def ekle(self):
        if self.F_listele:
            self.F_listele.destroy()
        if self.F_ekle:
            self.F_ekle.destroy()
        self.F_ekle = Frame(self.master)
        self.F_ekle.place(x=250,y=150)
        Label(self.F_ekle,text="Kitap Adı: ").grid(row=0,column=0,pady=5,sticky=W)
        self.E1 = Entry(self.F_ekle, width=35)
        self.E1.grid(row=0,column=1,pady=5)

        Label(self.F_ekle,text="Yazar: ").grid(row=1,column=0,pady=5,sticky=W)
        self.E2 = Entry(self.F_ekle, width=35)
        self.E2.grid(row=1,column=1,pady=5)

        Label(self.F_ekle,text="Yayın Evi: ").grid(row=2,column=0,pady=5,sticky=W)
        self.E3 = Entry(self.F_ekle, width=35)
        self.E3.grid(row=2,column=1,pady=5)

        Label(self.F_ekle,text="Sayfa Sayısı: ").grid(row=3,column=0,pady=5,sticky=W)
        self.SS = Spinbox(self.F_ekle, from_=1, to = 999, width=5)
        self.SS.grid(row=3,column=1,pady=5,sticky=W)

        Label(self.F_ekle,text="Kaçıncı Baskı: ").grid(row=4,column=0,pady=5,sticky=W)
        self.BasimSay = Spinbox(self.F_ekle, from_=1, to = 999, width=5)
        self.BasimSay.grid(row=4,column=1,pady=5,sticky=W)

        Label(self.F_ekle,text="Yayın Yılı: ").grid(row=5,column=0,pady=5,sticky=W)
        self.BasimYil = Spinbox(self.F_ekle, from_=0, to = 2021, width=5)
        self.BasimYil.grid(row=5,column=1,sticky=W)

        B3 = Button(self.F_ekle, text="KAYIT ET",command=self.kayit_et,fg="red", cursor="hand2", width=15)
        B3.grid(row=5,column=1,pady=8,sticky=NE)


    def kayit_et(self):
        try:
            self.im.execute("CREATE TABLE IF NOT EXISTS kitaplar (id INTEGER PRIMARY KEY, Kitap_Adi VARCHAR(45), Yazar VARCHAR(45), Yayin_Evi VARCHAR(45), Sayfa_Sayisi INT, Baski INT, Yayin_Yili)") # Tablo oluşturma
            self.im.execute("INSERT INTO kitaplar VALUES (null,'"+self.E1.get()+"','"+self.E2.get()+"','"+self.E3.get()+"','"+self.SS.get()+"','"+self.BasimSay.get()+"','"+self.BasimYil.get()+"')")  # Veri ekleme
            self.baglanti.commit()
            say = Label(self.F_ekle, text="Kayıt Başarılı.", font="bold", fg="green")
            say.grid(row=6,column=1,pady=8,sticky=W)
            say.after(2000, say.destroy)
        except:
            messagebox.showerror("Hata","Galiba Kayıt Edilemedi.")

    def listele(self):
        try:
            if self.F_ekle:
                self.F_ekle.destroy()
            if self.F_listele:
                self.F_listele.destroy()
            self.F_listele = Frame(self.master)
            self.F_listele.place(x=0,y=120)
            self.im.execute("SELECT * FROM kitaplar")
            data = self.im.fetchall()
            def search():
                deget = self.ara.get()
                query = "SELECT id, Kitap_Adi, Yazar, Yayin_Evi, Sayfa_Sayisi, Baski, Yayin_Yili FROM kitaplar WHERE Kitap_Adi LIKE '%"+deget+"%' OR Yazar LIKE '%"+deget+"%' OR Yayin_Evi LIKE '%"+deget+"%'"
                self.im.execute(query)
                rows = self.im.fetchall()
                update(rows)
                bulunanVeri = len(rows)
                toplamverilbl["text"] = ""
                AraLBL["text"] = "Bulunan Veri: "+str(bulunanVeri)
                AraLBL.grid(row=3,column=0,sticky=W)

            self.ara = Entry(self.F_listele,width=35)
            self.ara.grid(row=0,column=0,sticky=W,pady=20,padx=10)
            self.araBTN = Button(self.F_listele, text="Ara",fg="blue",command=search,width=5)
            self.araBTN.grid(row=0,column=0,sticky=W,pady=20,padx=230)

            self.tv = ttk.Treeview(self.F_listele, columns=(1,2,3,4,5,6,7), show='headings', height=10)
            self.tv.grid()
            self.tv.bind("<Button-3>", self.popup)
            self.tv.heading(1, text='ID')
            self.tv.heading(2, text='Kitap Adı')
            self.tv.heading(3, text='Yazar')
            self.tv.heading(4, text='Yayın Evi')
            self.tv.heading(5, text='Sayfa Sayısı')
            self.tv.heading(6, text='Baskı')
            self.tv.heading(7, text='Yayın Yılı')

            self.tv.column("1",minwidth=10,width=27)
            self.tv.column("2",minwidth=50,width=250)
            self.tv.column("3",minwidth=50,width=198)
            self.tv.column("4",minwidth=50,width=100)
            self.tv.column("5",minwidth=10,width=60)
            self.tv.column("6",minwidth=10,width=40)
            self.tv.column("7",minwidth=10,width=60)

            sb = Scrollbar(self.F_listele, orient=VERTICAL,command=self.tv.yview)
            sb.grid(row=1,column=1,sticky=NS)
            sb2 = Scrollbar(self.F_listele, orient=HORIZONTAL, command=self.tv.xview)
            sb2.grid(row=2,column=0,sticky=EW)
            
            toplamVeri = f"{len(data)} Veri Bulundu."
            toplamverilbl = Label(self.F_listele,text=toplamVeri)
            toplamverilbl.grid(row=3,column=0,sticky=W) #.place(x=0, y=380)
            Button(self.F_listele, text="Tabloyu Yenile",fg="red", command=self.Yenile).grid(row=3,column=0,sticky=S)
            AraLBL = Label(self.F_listele)

            self.tv.config(yscrollcommand=sb2.set)
            self.tv.configure(yscrollcommand=sb.set, xscrollcommand=sb2.set)
            s = 1
            for i in data:
                self.tv.insert(parent='', index=s, iid=s, values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                s += 1

            def update(rows):
                self.tv.delete(*self.tv.get_children())
                for i in rows:
                    self.tv.insert("","end",values=i)
        except:
            messagebox.showwarning("Hata", "Veri Tabanı Bulunamadı")
    def Yenile(self):
        self.F_listele.destroy()
        self.listele()

    def popup(self, event):
        iid = self.tv.identify_row(event.y)
        if iid:
            m = Menu(root, tearoff=0)
            m.add_command(label="Düzenle", command=self.Duzenle)
            m.add_command(label="Satırı Kopyala", command=self.Kopyala)

            self.tv.selection_set(iid)
            self.at = self.tv.selection_set(iid)
            m.post(event.x_root, event.y_root)
        else:
            pass

    def Duzenle(self):
        focus = self.tv.focus()
        numara = self.tv.item(focus)["values"][0]
        yeniWin = Toplevel()
        yeniWin.wm_title("Düzenle")
        windowWidth = yeniWin.winfo_reqwidth()
        windowHeight = yeniWin.winfo_reqheight()
        positionRight = int(yeniWin.winfo_screenwidth()/2 - windowWidth/1)
        positionDown = int(yeniWin.winfo_screenheight()/3 - windowHeight/3)
        yeniWin.geometry(f"300x320+{positionRight}+{positionDown}")
        yeniWin.resizable(width=False, height=False)

        def veriKayit():
            # Veri Tabanını oluştur
            self.im.execute("CREATE TABLE IF NOT EXISTS kitaplar (Kitap Adı VARCHAR(45), Yazar VARCHAR(45), Yayin Evi VARCHAR(45), Sayfa Sayısı INT, Baskı INT, Yayın Yılı)") # Tablo oluşturma

            self.im.execute("UPDATE kitaplar SET Kitap_Adi = ?, yazar = ?, Yayin_Evi = ?, Sayfa_Sayisi = ?, Baski = ?, Yayin_Yili = ? WHERE id = ?", (self.E1.get(),self.E2.get(),self.E3.get(),self.SS.get(),self.BasimSay.get(),self.BasimYil.get(),numara))
            self.baglanti.commit()
            say = Label(yeniWin,text="Kayıt Edildi.", font="bold", fg="green")
            say.pack(side=BOTTOM)
            say.after(2000, say.destroy)
        def veriDuzenle():
            self.E1.config(state="normal")
            self.E2.config(state="normal")
            self.E3.config(state="normal")
            self.SS.config(state="normal")
            self.BasimSay.config(state="normal")
            self.BasimYil.config(state="normal")
            B3.config(state="normal",cursor="hand2")
        def veriSil():
            evet = messagebox.askyesno("Sil","Veri Tabanından silmek istiyormusunuz?")
            if evet:
                self.im.execute("DELETE FROM kitaplar WHERE id = ?",[numara])
                self.baglanti.commit()
                yeniWin.destroy()
        F_ekle = Frame(yeniWin)
        F_ekle.pack()
        kopya = self.tv.focus()
        Label(F_ekle,text="Kitap Adı: ").grid(row=0,column=0,pady=5,sticky=W)
        
        self.E1 = Entry(F_ekle, width=35)
        self.E1.insert(0, self.tv.item(kopya)["values"][1])
        # print(self.tv.item(kopya)["values"][3])
        self.E1.config(state="disable")
        self.E1.grid(row=0,column=1,pady=5)
        Label(F_ekle,text="Yazar: ").grid(row=1,column=0,pady=5,sticky=W)
        self.E2 = Entry(F_ekle, width=35)
        self.E2.insert(0, self.tv.item(kopya)["values"][2])
        self.E2.config(state="disable")
        self.E2.grid(row=1,column=1,pady=5)
        Label(F_ekle,text="Yayın Evi: ").grid(row=2,column=0,pady=5,sticky=W)
        self.E3 = Entry(F_ekle, width=35)
        self.E3.insert(0, self.tv.item(kopya)["values"][3])
        self.E3.config(state="disable")
        self.E3.grid(row=2,column=1,pady=5)
        Label(F_ekle,text="Sayfa Sayısı: ").grid(row=3,column=0,pady=5,sticky=W)
        self.SS = Spinbox(F_ekle, width=5)
        self.SS.insert(0, self.tv.item(kopya)["values"][4])
        self.SS.config(state="disable")
        self.SS.grid(row=3,column=1,pady=5,sticky=W)
        Label(F_ekle,text="Kaçıncı Baskı: ").grid(row=4,column=0,pady=5,sticky=W)
        self.BasimSay = Spinbox(F_ekle, width=5)
        self.BasimSay.insert(0, self.tv.item(kopya)["values"][5])
        self.BasimSay.config(state="disable")
        self.BasimSay.grid(row=4,column=1,pady=5,sticky=W)
        Label(F_ekle,text="Yayın Yılı: ").grid(row=5,column=0,pady=5,sticky=W)
        self.BasimYil = Spinbox(F_ekle, width=5)
        self.BasimYil.insert(0, self.tv.item(kopya)["values"][6])
        self.BasimYil.config(state="disable")
        self.BasimYil.grid(row=5,column=1,sticky=W)
        B3 = Button(F_ekle, text="KAYIT ET",command=veriKayit,fg="green", width=15)
        B3.config(state="disable")
        B3.grid(row=5,column=1,pady=8,sticky=NE)
        
        B4 = Button(F_ekle,text="Düzenle",command=veriDuzenle,fg="blue", cursor="hand2", width=15)
        B4.grid(row=6,column=1,pady=8,sticky=NE)

        B5 = Button(F_ekle,text="Veriyi Sil",command=veriSil,fg="red", cursor="hand2", width=15)
        B5.grid(row=8,column=1,pady=8,sticky=NE)
    
    def Kopyala(self):
        kopya = self.tv.focus()
        self.master.clipboard_clear()
        self.master.clipboard_append(self.tv.item(kopya)["values"])
        say = Label(self.master,text="Kopyalandı", font="bold", fg="red")
        say.pack(side=BOTTOM)
        say.after(2000, say.destroy)

    def exitProgram(self):
        exit()

root = Tk()
app = Window(root)
root.wm_title("Kitap Kayıt Sistemi | 20.05.2021")

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
root.geometry(f"755x520+{positionRight}+{positionDown}")
root.resizable(width=False, height=False)

def callback(url):
    webbrowser.open_new(url)
me = Label(root, text="Developer: yazilimfuryasi.com | @yazilimfuryasi", fg="#6E7371",cursor="hand2",font="Verdana 7 bold")
me.pack(side=BOTTOM)
me.bind("<Button-1>", lambda e: callback(webbrowser.open_new("https://www.instagram.com/yazilimfuryasi/")))

root.mainloop()