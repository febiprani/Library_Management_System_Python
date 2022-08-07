CREATE DATABASE lms_pytugas4;
USE lms_pytugas4;

CREATE TABLE daftar_user(
Id_User INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
U_Name VARCHAR(50) NOT NULL,
Tgl_Lahir DATE,
Pekerjaan VARCHAR(50),
Alamat VARCHAR(100)
);

CREATE TABLE daftar_buku(
Id_Buku VARCHAR(10) NOT NULL PRIMARY KEY,
Nama_Buku VARCHAR(100) NOT NULL,
Kategori VARCHAR(50),
Stock INT NOT NULL,
FULLTEXT (Nama_Buku, Kategori)
);

CREATE TABLE peminjaman(
Id_Peminjaman INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Id_User INT NOT NULL,
Nama_User VARCHAR(50) NOT NULL,
Id_Buku VARCHAR(10),
Nama_Buku VARCHAR(100) NOT NULL,
Tanggal_Pinjam DATE,
Tanggal_Kembali DATE,
FOREIGN KEY(Id_User) REFERENCES daftar_user(Id_User),
FOREIGN KEY(Id_Buku) REFERENCES daftar_buku(Id_Buku)
);