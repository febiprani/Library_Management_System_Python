import buku
import koneksi

exit = False
while not exit:
    homepage = """
.................LIBRARY MANAGEMENT.................
----------------------------------------------------
    1. Pendaftaran User Baru
    2. Pendaftaran Buku Baru
    3. Peminjaman
    4. Tampilkan Daftar Buku
    5. Tampilkan Daftar User
    6. Tampilkan Daftar Peminjaman
    7. Cari Buku
    8. Pengembalian
    9. Exit
----------------------------------------------------
Masukkan Nomor Tugas:
====================================================
"""
    daftar_perintah = ("1","2","3","4","5","6","7","8","9")
    perintah = input(homepage)
    while perintah not in daftar_perintah:
      
        print("""
    
Masukkan angka 1 sampai 9""")
        perintah = input(homepage)
            
    if perintah == "9":
        exit = True
        print("Terima Kasih, Sampai Bertemu kembali")
        print("====================================================")
    elif perintah == "8":
        buku.pengembalian_buku()
    elif perintah == "7":
        buku.cari()
    elif perintah == "6":
        buku.daftar_peminjaman()
    elif perintah == "5":
        buku.list_user()
    elif perintah == "4":
        buku.list_buku()
    elif perintah == "3":
        buku.pinjam()
    elif perintah == "2":
        buku.daftar_buku()
    elif perintah == "1":
        buku.daftar_user()