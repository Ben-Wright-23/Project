import sqlite3 as sql

class DatabaseHandler:
    def __init__(self, databaseName):
        self.name = databaseName

    def createTables(self):
        connection = sql.connect(self.name)

        connection.execute("""CREATE TABLE IF NOT EXISTS user(
                           
                           username text PRIMARY KEY,
                           password text NOT NULL,
                           CHECK ((length(password)>6 AND password GLOB'*[0-9]*') AND (length(username)>3 AND length(username)<16))

                           );""")
        
        connection.close()



# AND password LIKE %[0-9]%


    def dropUsers(self):
        connection = sql.connect(self.name)

        connection.execute("""DROP TABLE user;""")
        
        connection.close()
    
    def createUser(self, username, password):
        connection = sql.connect(self.name)
        try:
            connection.execute("""INSERT INTO user
                            VALUES (?,?)""", (username,password))
        
            connection.commit()
            connection.close()
            return True
        except Exception as e:                      
            connection.close()
            return e
        

    def authenticateUser(self, username, password):
        connection = sql.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("""SELECT username 
                       FROM user
                       WHERE username = ? 
                       AND password = ? ;""",
                       (username,password))
        result = cursor.fetchone()
        connection.close()
        if result != None:
            return True
        else:
            return False

    def deleteUser(self,currentUser):
        connection = sql.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM user
                       WHERE username == currentUser ;""",
                       (currentUser))
        connection.commit()
        connection.close()
