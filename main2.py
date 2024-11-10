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
    c = conn.cursor()
    c.execute(
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
    conn=sql.connect("./db/test-kuku.db")
    c=conn.cursor()
    ps = f.encrypt(b'ps')
    data = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?)"
    c.execute(data,(userNickname,Email,ps))
    conn.commit()
    conn.close()
    print("Insertion Complit.")

def selctData():
    conn=sql.connect("./db/test-kuku.db")
    c=conn.cursor()
    c.execute(
        """
        SELECT ps
        FROM Users
        WHERE userID=1;
        """
    )
    conn.commit()
    print(f'SELECT USER = {c.fetchone()}.')
    conn.close()

def modiTableUsers():
    conn=sql.connect("./db/test-kuku.db")
    c=conn.cursor()
    ejecucion="""
        SELECT ps
        FROM Users
        WHERE userID=1;
        """
    c.execute(ejecucion)
    val = c.fetchone()
    val = f.encrypt(b'val')
    data="""UPDATE Users
        SET ps = ?
        WHERE userID=1;"""
    c.execute(data,(val,))
    conn.commit()
    conn.close()
    print("Actualizacion de contraceña cifrada")

def delateUserById():
    conn=sql.connect("./db/test-kuku.db")
    c=conn.cursor()
    c.execute("DELETE FROM Users WHERE userID=2;")
    conn.commit()
    conn.close()
    print("User delate in Table Users.")

def delateTable():
    conn=sql.connect("./db/test-kuku.db")
    c=conn.cursor()
    c.execute(
    """
    DROP TABLE Users;
    """
    )
    conn.commit()
    conn.close()
    print("Table eliminate.")

if __name__ == "__main__":
    main()