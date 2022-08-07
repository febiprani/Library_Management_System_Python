import koneksi
import pandas as pd
from mysql.connector import Error
from datetime import date

def cari():
    
    try:
        mydb = koneksi.connect_sql()
        mycursor = mydb.cursor()
        mycursor.execute("DESCRIBE daftar_buku")
        describe_buku = pd.DataFrame(mycursor.fetchall())
        nama_kolom = describe_buku.iloc[:, 0]
    
        keyword = input("Masukkan Keyword Yang Ingin Dicari: ")
        mycursor.execute("SELECT * FROM daftar_buku WHERE MATCH(Nama_Buku, Kategori) \
                         AGAINST (%s IN NATURAL LANGUAGE MODE)",(keyword,))
        hasil = mycursor.fetchall()
        jumlah_hasil = len(hasil)
        if jumlah_hasil < 1:
            print("Buku Tidak Ditemukan")
        else:
            hasil = pd.DataFrame(hasil)
            hasil = hasil.rename(columns = nama_kolom)
            print(hasil)
    except Error as err:
        print(f"Error: {err}")
        

def pinjam():

    today = date.today()
    mydb = koneksi.connect_sql()
    mycursor = mydb.cursor()
    
    try:
        mycursor.execute("SELECT Id_User FROM daftar_user")
        list_user = mycursor.fetchall()
        
        id_user = []
        for x in list_user:
            id_user.append(str(x[0]))
            
        cek_id_peminjam = input("Masukkan ID Peminjam: ")
        
        while cek_id_peminjam not in id_user:
            print("ID User Tidak Ditemukan, Silahkan Masukkan ID Yang Sesuai")
            cek_id_peminjam = input("Masukkan ID Peminjam: ")
            
        print("ID User: "+cek_id_peminjam)
        
    except Error as err:
        print(f"Error: {err}")
        
    try:
        mycursor.execute("SELECT U_Name FROM daftar_user WHERE Id_User = %s", (cek_id_peminjam,))
        nama_user = mycursor.fetchall()[0][0]
        print("Nama User: "+nama_user)
    except Error as err:
        print(f"Error: {err}")
        
    try:
        mycursor.execute("SELECT Id_Buku FROM daftar_buku")
        list_buku = mycursor.fetchall()
        
        id_buku = []
        for x in list_buku:
            id_buku.append(str(x[0]))
        cek_id_buku = input("Masukkan ID Buku: ")
        
        while cek_id_buku not in id_buku:
            print("ID Buku Tidak Ditemukan, Silahkan Masukkan ID Yang Sesuai")
            cek_id_buku = input("Masukkan ID Buku: ")  
        print("ID Buku: "+cek_id_buku)
        
    except Error as err:
        print(f"Error: {err}")
        
    try:
        mycursor.execute("SELECT Nama_Buku FROM daftar_buku WHERE Id_Buku = %s", (cek_id_buku,))
        nama_buku = mycursor.fetchall()[0][0]
        print("Judul Buku: "+nama_buku)
    except Error as err:
        print(f"Error: {err}")
        
    try:
        mycursor.execute("SELECT Stock FROM daftar_buku WHERE Id_Buku = %s", (cek_id_buku,))
        stock_buku = mycursor.fetchall()
        sisa_stock_buku = stock_buku[0][0]
        print("Stock Buku: "+str(sisa_stock_buku))
        
        if sisa_stock_buku < 1:
            print("Buku Tidak Tersedia")
        else:
            print("Buku Dipinjamkan ke: "+ nama_user)
            sisa_stock_buku -= 1
            print("Sisa Stock Buku: "+str(sisa_stock_buku))
            mycursor.execute("UPDATE daftar_buku SET Stock = %s WHERE Id_Buku = %s" %(sisa_stock_buku,cek_id_buku))
            mycursor.execute("INSERT INTO peminjaman(Id_User, Nama_User, Id_Buku, Nama_Buku, Tanggal_Pinjam)\
                                     VALUES(%s,%s,%s,%s,%s)",(cek_id_peminjam, nama_user, cek_id_buku, nama_buku, today))           
            mydb.commit()
             
    except Error as err:
        print(f"Error: {err}")
        

def daftar_buku():
    mydb = koneksi.connect_sql()
    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT Id_Buku FROM daftar_buku")
        list_id_buku = mycursor.fetchall()
        
        id_buku = []
        for x in list_id_buku:
            id_buku.append(str(x[0]))
            
        cek_id_buku = input("Masukkan ID Buku: ")
        
        while cek_id_buku in id_buku:
            print("ID Sudah Ada, Silahkan Masukkan ID Yang Lain")
            cek_id_buku = input("Masukkan ID Buku: ")
            
        nama_buku = input("Masukkan Nama Buku: ")
        kategori = input("Masukkan Kategori Buku: ")
        stock = input("Masukkan Stock Buku: ")
        data = (cek_id_buku, nama_buku, kategori, stock)
        
        query = """
INSERT INTO daftar_buku(Id_Buku,Nama_Buku,Kategori,Stock) VALUES(%s,%s,%s,%s)
"""
        mycursor.execute(query, data)
        mydb.commit()
        print('Query berhasil dieksekusi')
        print('..........................')
        print('Data berhasil ditambahkan!')
        
    except Error as err:
        print(f"Error: {err}")
        
        
def daftar_user():
    nama_user = input("Masukkan Nama User: ")
    tanggal_lahir = input("Masukkan Tanggal Lahir (YYYY-MM-DD): ")
    pekerjaan = input("Masukkan Pekerjaan: ")
    alamat = input("Masukkan Alamat: ")
    data = (nama_user, tanggal_lahir, pekerjaan, alamat)
     
    try:
        query = """
INSERT INTO daftar_user(U_Name,Tgl_Lahir,Pekerjaan,Alamat) VALUES(%s,%s,%s,%s)
"""
        mydb = koneksi.connect_sql()
        mycursor = mydb.cursor()
        mycursor.execute(query, data)
        mydb.commit()
        print('Query berhasil dieksekusi')
        print('..........................')
        print('Data berhasil ditambahkan!')
    except Error as err:
        print(f"Error: {err}")
        
        
        
def pengembalian_buku():
    
    today = date.today()
    mydb = koneksi.connect_sql()
    mycursor = mydb.cursor()
    
    try:
        mycursor.execute("SELECT Id_User FROM peminjaman WHERE Tanggal_Kembali IS NULL")
        list_peminjaman = mycursor.fetchall()
        if len(list_peminjaman) > 0: 
            id_peminjam = []
            for x in list_peminjaman:
                id_peminjam.append(str(x[0]))
            cek_id_peminjam = input("Masukkan ID Peminjam: ")
            while cek_id_peminjam not in id_peminjam:
                print("ID Peminjam Tidak Ditemukan, Silahkan Masukkan ID Yang Sesuai")
                cek_id_peminjam = input("Masukkan ID Peminjam: ")
            print("ID Peminjam: "+cek_id_peminjam)
            
            mycursor.execute("SELECT Id_Buku, Nama_Buku FROM peminjaman WHERE Id_User = %s \
                              AND Tanggal_Kembali IS NULL", (cek_id_peminjam,))
            list_pinjam_buku = mycursor.fetchall()
            id_buku = []
            print("Buku Yang Dipinjam:")
            result = pd.DataFrame(list_pinjam_buku)
            print(result)
            
            for y in list_pinjam_buku:
                id_buku.append(str(y[0]))
            cek_id_buku = input("Masukkan ID Buku Yang Akan Dikembalikan: ")
            while cek_id_buku not in id_buku:
                print("ID Buku Tidak Ditemukan, Silahkan Masukkan ID Yang Sesuai")
                cek_id_buku = input("Masukkan ID Buku Yang Akan Dikembalikan: ")
            mycursor.execute("UPDATE peminjaman SET Tanggal_Kembali = %s WHERE Id_User = %s \
                              AND Id_Buku = %s",(today, cek_id_peminjam, cek_id_buku))
            mycursor.execute("UPDATE daftar_buku SET Stock = Stock+1 WHERE Id_Buku = %s",(cek_id_buku,))
            mydb.commit()
            print("Buku telah berhasil dikembalikan, terima kasih")
            print("============================================================")
            
        else:
            print("Tidak Ada Buku Yang Dipinjam")
            
    except Error as err:
        print(f"Error: {err}")
        
        
def list_buku():
    print('......................Daftar Buku..............................')
    print('---------------------------------------------------------------')
    mydb = koneksi.connect_sql()
    query = 'SELECT * FROM daftar_buku'
    query_describe = 'DESCRIBE daftar_buku'
    mycursor = mydb.cursor()
    result = None
    nama_kolom = None

    try:
        mycursor.execute(query_describe)
        describe_user = pd.DataFrame(mycursor.fetchall())
        nama_kolom = describe_user.iloc[:, 0]
    except Error as err:
        print(f"Error: {err}")
    
    try:
        mycursor.execute(query)
        result = pd.DataFrame(mycursor.fetchall())
        result = result.rename(columns = nama_kolom)
        print(result)
        print('---------------------------------------------------------------')
        return pd.DataFrame(result)
    except Error as err:
        print(f"Error: {err}")
        
        
        
def daftar_peminjaman():
    print('..............................Daftar Peminjaman......................................')
    print('-------------------------------------------------------------------------------------')
    mydb = koneksi.connect_sql()
    query = 'SELECT * FROM peminjaman'
    query_describe = 'DESCRIBE peminjaman'
    mycursor = mydb.cursor()
    result = None
    nama_kolom = None

    try:
        mycursor.execute(query_describe)
        describe_user = pd.DataFrame(mycursor.fetchall())
        nama_kolom = describe_user.iloc[:, 0]
    except Error as err:
        print(f"Error: {err}")
    
    try:
        mycursor.execute(query)
        result = pd.DataFrame(mycursor.fetchall())
        result = result.rename(columns = nama_kolom)
        print(result)
        print('-------------------------------------------------------------------------------------')
        return pd.DataFrame(result)
    except Error as err:
        print(f"Error: {err}")

        
def list_user():
    print('......................Daftar User..............................')
    print('---------------------------------------------------------------')
    mydb = koneksi.connect_sql()
    query = 'SELECT * FROM daftar_user'
    query_describe = 'DESCRIBE daftar_user'
    mycursor = mydb.cursor()
    result = None
    nama_kolom = None

    try:
        mycursor.execute(query_describe)
        describe_user = pd.DataFrame(mycursor.fetchall())
        nama_kolom = describe_user.iloc[:, 0]
    except Error as err:
        print(f"Error: {err}")
    
    try:
        mycursor.execute(query)
        result = pd.DataFrame(mycursor.fetchall())
        result = result.rename(columns = nama_kolom)
        print(result)
        print('---------------------------------------------------------------')
        return pd.DataFrame(result)
    except Error as err:
        print(f"Error: {err}")