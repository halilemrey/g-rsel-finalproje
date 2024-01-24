from flask import Flask, render_template, request,redirect ,url_for
import sqlite3


app = Flask(__name__)


data =[]

def veriAl():
    global data
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("select * from tblBook")
        data = cur.fetchall()
        for i in data:
            print(i)

def veriEkle(title, author , year):
    
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("insert into tblBook (booktitle, bookauthor,bookyear) values (?,?,?)",(title,author,year))
        con.commit()
        print("Veriler eklendi")

def veriSil(id):
    
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id=?",[id])
        
        print("Veriler silindi")
                
def veriGuncelle(id,title, author , year):
    
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("update tblBook set booktitle=?, bookauthor=?,bookyear=? where id=?",(title,author,year,id))
        con.commit()
        print("Veriler güncellendi")       


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/kitap")
def kitap():
    veriAl()
    return render_template("kitap.html", veri = data)

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/proje")
def proje():
    return render_template("proje.html")
@app.route("/hakkımızda")
def hakkmızda():
    return render_template("hakkımızda.html")

@app.route("/kitapekle", methods=['GET','POST'])
def kitapekle():
    print("kitapekle")
    if request.method == "POST":
        
        bookTitle = request.form['bookTitle']
        bookAuthor = request.form['bookAuthor']
        bookYear = request.form['bookYear']
        veriEkle(bookTitle, bookAuthor, bookYear)
    return render_template("kitapekle.html")

@app.route("/kitapsil/<string:id>")
def kitapsil(id):
    print("kitap silinecek id", id)
    veriSil(id)
    return redirect(url_for("kitap"))

@app.route("/kitapguncelle/<string:id>", methods=['GET','POST'])
def kitapguncelle(id):
    if request.method== 'GET':
        print("Güncellenecek  id", id)

        guncellenecekVeri =[]
        for d in data:
            if str(d[0])==id:
                guncellenecekVeri = list(d)
        return render_template("kitapguncelle.html", veri = guncellenecekVeri)                
    else:
        bookID = request.form['bookID']
        bookTitle = request.form['bookTitle']
        bookAuthor = request.form['bookAuthor']
        bookYear = request.form['bookYear']
        veriGuncelle(bookID, bookTitle, bookAuthor, bookYear)
        return redirect(url_for("kitap"))
    

@app.route("/kitapdetay/<string:id>")
def kitapdetay(id):
    
    detayVeri =[]
    for d in data:
        if str(d[0])==id:
            detayVeri= list(d)
    return render_template("kitapdetay.html", veri = detayVeri)                
     



if __name__ == "__main__":
    app.run(debug= True)