from os import EX_CANTCREAT
from re import A
import mysql.connector
import crypt
from cryptography.fernet import Fernet
import base64
import pyperclip 

class user:
    def __init__(self):
        self.id = -1

    def loginAvailable(self, name: str):
        try:
            con = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
            cur = con.cursor()
            cur.execute("select * from user where name = '%s'" % name) 
            temp = cur.fetchall()
            res = temp[0][1]
            cur.close()
            con.close()
            if res is not None:
                return False
            return 5/0
        except:
            return True

    def register(self, name: str, passwd: str):
        try:
            if self.loginAvailable(name) == False:
                return None
            conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db") 
            cur = conn.cursor()
            a = crypt.crypt()
            key = Fernet.generate_key().decode()
            passwd = a.encrypt_message(passwd,key, 1)
            key = key.encode("ascii")
            key = base64.b64encode(key)
            key = key.decode()
            cur.execute("insert into user(name, passwd, gen_keys) values('%s','%s','%s')" % (name, passwd, key))
            conn.commit()
            cur.close()
            conn.close()
            return 1
        except:
            return None

    def unregister(self):
        try:
            conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
            cur = conn.cursor()
            cur.execute("delete from user where id='%d'" % self.getUserId())
            conn.commit()
            conn.close()
            self.id = -1
        except:
            pass
        
    def idToDef(self):
        self.id = -1
    
    def printSelfId(self):
        pass
    def setId(self, id):
        self.id = id

    def login(self, name: str, passwd: str):
        try:
            conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
            cur = conn.cursor()
            cur.execute("select * from user where name = '%s'" % (name))
            row = cur.fetchone()
            b = row[0]
            c = row[2]
            d = row[3]
            a = crypt.crypt()
            passw = a.decrypt_message(c, d)
            self.id = row[0]
            conn.close()
            if(passw == passwd):
                return b
            return 5/0
        except:
            return None
    
    def returnLoginUsername(self):
        try:
            conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
            cur = conn.cursor()
            cur.execute("select * from user where id = '%d'" % self.id)
            res = cur.fetchall()
            return res[0][1]
        except:
            return None

    def passwordUpdate(self, name: str, passwd: str):
        conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
        cur = conn.cursor()
        cur.execute("select * from user where name = '%s'" % name)
        temp = cur.fetchone()
        key = temp[3]
        cur.close()
        cur = conn.cursor()
        a = crypt.crypt()
        passwd = a.encrypt_message(passwd, key, 0)
        cur.execute("update user set passwd = '%s' where name = '%s'" % (passwd, name))
        conn.commit()
        cur.close()
        conn.close()
        return 1


    def getUserId(self) -> int:
        return self.id

    def getGenKeys(self):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'db')
        cur = conn.cursor()
        cur.execute("select * from user where id = '%d'" % (self.getUserId()))
        tmp = cur.fetchall()
        conn.close()
        cur.close()
        key = tmp[0][3]
        return key
        
    def show_data(self):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'db')
        cur = conn.cursor() 
        cur.execute("select id, password, name, source from artefact where user_id = '%d'" % (self.getUserId()))
        res = cur.fetchall()
        ans = []
        a = crypt.crypt()
        key = self.getGenKeys()
        for ch in res:
            ans.append((ch[0], ch[2], ch[3]))
        conn.close() 
        return ans

    def insert_passwd(self, source: str, name: str, passwd: str):
        conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
        cur = conn.cursor()
        key = self.getGenKeys()
        a = crypt.crypt()
        passwd = a.encrypt_message(passwd, key, 0)
        cur.execute("insert into artefact(user_id, password, name, source) values('%d', '%s', '%s', '%s')" % (self.getUserId(), passwd, name, source))
        conn.commit()
        conn.close()
        return self.row_id(source, name, passwd)

    def row_id(self, source: str, name:str, passwd: str):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'db')
        cur = conn.cursor()
        cur.execute("select * from artefact where user_id = '%d'  and password = '%s' and name = '%s' and source = '%s'" % (self.getUserId(), passwd, name, source))
        data = cur.fetchall()
        id = data[0][0]
        conn.commit()
        conn.close()
        return id 

    def delete_passwd(self, id: int):
        conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "1234", database = "db")
        cur = conn.cursor()
        cur.execute("delete from artefact where id = '%d' and user_id = '%d'" % (id, self.getUserId()))
        conn.commit()
        conn.close()

    def update_passwd(self, id: int, source: str, name:str, passwd: str):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'db')
        cur = conn.cursor()
        a = crypt.crypt()
        key = self.getGenKeys()
        passwd = a.encrypt_message(passwd, key, 0)
        cur.execute("update artefact set password = '%s', name = '%s', source = '%s' where id = '%d' and user_id = '%d'" % (passwd, name, source, id, self.getUserId()))
        conn.commit()
        conn.close()
    
    def showRowData(self, id: int):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234', database = 'db')
        cur = conn.cursor()
        cur.execute("select  password, name, source from artefact where user_id = '%d' and id = '%d'" % (self.getUserId(), id))
        data = cur.fetchall()
        key = self.getGenKeys()
        a = crypt.crypt()
        passwd = data[0][0]
        passwd = a.decrypt_message(passwd, key)
        name = data[0][1]
        source = data[0][2]
        res = (passwd, name, source)
        conn.commit()
        conn.close()
        return res


    
