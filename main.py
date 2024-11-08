import sqlite3 as sql
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

def createDB():
    conn =sql.connect("test-kuku.db")
    conn.commit()
    conn.close()

def createTabla():
    conn =sql.connect("./db/test-kuku.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE Users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        userNickname TEXT NOT NULL,
        Email TEXT NOT NULL,
        ps TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()
    print("Table Create.")

def createUser(userNickname,Email,ps):
    conn = sql.connect("./db/test-kuku.db")
    cursor = conn.cursor()
    ps = f.encrypt(b'ps')
    data = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?)"
    cursor.execute(data,(userNickname,Email,ps))
    conn.commit()
    conn.close()
    print("Insertion Complit.")

def selctData():
    conn=sql.connect("./db/test-kuku.db")
    cusrsor=conn.cursor()
    cusrsor.execute(
        """
        SELECT userID
        FROM Users;
        """
    )
    conn.commit()
    conn.close()
    print("SELECT USER ID.")

def delateUserById():
    conn = sql.connect("./db/test-kuku.db")
    cursor = conn.cursor()
    cursor.execute("DELeTE FROM Users WHERE userID=2;")
    conn.commit()
    conn.close()
    print("User delate in Table Users.")

def delateTable():
    conn = sql.connect("./db/test-kuku.db")
    cursor = conn.cursor()
    cursor.execute(
    """
    DROP TABLE Users;
    """
    )
    conn.commit()
    conn.close()
    print("Table eliminate.")

if __name__ == "__main__":
    createUser("sanches","sanche@gmail.com","12343")