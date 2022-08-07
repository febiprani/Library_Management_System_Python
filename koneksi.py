import mysql.connector 
from mysql.connector import Error
import pandas as pd

def connect_sql():
    nama_host = "localhost" 
    user = "root"
    password = "Praniprahestif1997"

    myconn = mysql.connector.connect(host = nama_host, user = user, passwd = password)

    mycursor = myconn.cursor()
    
 
 
