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


    def createUser(self, username, password):
        connection = sql.connect(self.name)
        try:
            connection.execute("""INSERT INTO user
                            VALUES (?,?)""", (username,password))
        
            connection.commit()
            connection.close()
            return True
        except:                      
            connection.close()
            return False

        


# AND 
#password GLOB'*[0-9]*'


    def dropUsers(self):
        connection = sql.connect(self.name)

        connection.execute("""DROP TABLE tournament;""")
        
        connection.close()
    

        

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
        
        connection.execute("""DELETE FROM user
                        WHERE username = ? ;""",
                        [currentUser])
        connection.commit()
        connection.close()

    def createTournamentTables(self):
        try:
            connection = sql.connect(self.name)
            connection.execute('''
                                create table tournament (
                                    tournamentName PRIMARY KEY,
                                    username text,
                                    numTeams integer NOT NULL,
                                    active text,
                                    bracket text,
                                    viewCode text,
                                    FOREIGN KEY (username) REFERENCES user(username),
                                    CHECK (length(TournamentName)>4 AND length(TournamentName)<30)
                            )''')
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def createTournament(self,tournamentName,currentUser,numTeams,bracket):
        try:
            connection = sql.connect(self.name)
            connection.execute("""INSERT INTO tournament 
                               (tournamentName,username,numTeams,active,bracket)
                                # Inserts the values into these specific fields, so it can ignore any other fields when inserting   
                               VALUES (?,?,?,false,?)
                               """,(tournamentName,currentUser,numTeams,bracket))
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False
        
    def getBrackets(self,tournamentName):
        try:
            connection = sql.connect(self.name)
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM tournament WHERE tournamentName = ?;""",[tournamentName])
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            results = {}
        finally:
            connection.close()
            return results
        

    def addBrackets(self, bracket, tournamentName):
        try:
            connection = sql.connect(self.name)
            connection.execute("""UPDATE tournament 
                               SET bracket = ?
                               WHERE tournamentName = ?
                               """,(bracket, tournamentName))
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False
        
    def updateActiveTrue(self, tournamentName):
        try:
            connection = sql.connect(self.name)
            connection.execute("""UPDATE tournament 
                               SET active = ?
                               WHERE tournamentName = ?
                               """,("true", tournamentName))
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False


    def checkViewCodes(self,viewCode):
        #defines checkViewCodes function, with the view code to be checked for passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #creates a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT viewCode FROM tournament WHERE viewCode = ?;""",[viewCode])
            #exectutes the previously designed SQL statement using the cursor to check through the records for the view code has been passed in
            results = cursor.fetchone()
            #fetches the view code if there is one that matches the passed in view code
            connection.close()
            #close the connection to the database
            return results
            #returns the view code from the database if it matches the view code passed in, signifying the passed in view code is not unique, otherwise it will return None
        except Exception as e:
            #if there was an error executing the SQL statement:
            connection.close()
            #close the connection to the database
            print(e)
            #print the error that has occured
            return False
            #returns false signifying the check has not been completed
            
        
    def addViewCode(self, viewCode, tournamentName):
        #defines checkViewCodes function, with the view code to be added passed in as well as the tournament it should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET viewCode = ?
                               WHERE tournamentName = ?
                               """,(viewCode, tournamentName))
            #exectutes the previously designed SQL statement to add the view code to the current tournament
            connection.commit()
            #commit the addition of the view code to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the viewCode has been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns true signifying the viewCode has not been added to the current tournament successfully
            





