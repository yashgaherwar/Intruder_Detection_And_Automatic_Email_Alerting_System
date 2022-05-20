import mysql.connector
import mysql.connector as sql

class connections:
    
    
    __HOST = 'localhost'
    __USERNAME = ''
    __PASSWORD = ''
    __DATABASE = 'edi_project'

    def __init__(self):
        self.con = sql.connect(host=connections.__HOST,user=connections.__USERNAME,password=connections.__PASSWORD,database=connections.__DATABASE)
        #self.con = sql.connect(host=HOST,user=USERNAME,password=PASSWORD,database=DATABASE)
        


    def my_verify_user(self,username,password):
        self.con = sql.connect(host=connections.__HOST,user=connections.__USERNAME,password=connections.__PASSWORD,database=connections.__DATABASE)
        
        print(self.con)
        
        sql_query = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (username, password)
        mycursor = self.con.cursor()
        
        
        mycursor.execute(sql_query)
        myresults =mycursor.fetchall()
        print(myresults)
        if len(myresults) <=0 :
          return False
        else:
          return True
       

    def database_insert(self,username,password):
        my_sql = "INSERT INTO login (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor = self.con.cursor()
        mycursor.execute(my_sql, val)

        self.con.close()

    

    
    