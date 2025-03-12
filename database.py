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
                                    roundStartTimes text,
                                    matchDuration text,
                                    breakLength text,
                                    matchScores text,
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
                               VALUES (?,?,?,false,?)
                               """,(tournamentName,currentUser,numTeams,bracket))
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False
        
    def getTournamentFields(self,tournamentName):
        #name changed to better suit its multiple purposes
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
                               SET bracket = ?, matchScores = ?
                               WHERE tournamentName = ?
                               """,(bracket, bracket, tournamentName))
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
            

    def getTournaments(self,currentUser):
        #defines getTournaments function, the current user trying to access their tournaments passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #creates a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT * FROM tournament WHERE username = ?;""",[currentUser])
            #exectutes the previously designed SQL statement to select all tournaments where the username matches the given current user
            results = cursor.fetchall()
            #fetches all the tournaments that have a username matching the passed in username for the current user 
            connection.close()
            #close the connection to the database
            return results
            #returns all the tournaments, including all of the data in it's fields, where the username assigned to the tournament matches the given current user
        except Exception as e:
            connection.close()
            #close the connection to the database
            print(e)
            #print the error in the SQL statement if there has been one
            return False
            #returns false signifying the selection was unsuccessful
            

    def deleteTournament(self,tournamentName):
        #defines deleteTournament function, with the tournament name of the tournament that needs to be deleted passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""DELETE FROM tournament
                                WHERE tournamentName = ? ;""",
                                [tournamentName])
            #exectutes the previously designed SQL statement to delete the tournament with a given tournament name
            connection.commit()
            #commit the deletion of the tournament to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the tournament has been deleted successfully

        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns false signifying the tournament has not been deleted successfully



    def addFixtureInfo(self, startTimes, duration, breakLength, tournamentName):
        #defines addFixtureInfo function, with the round start times, match duration and break length to be added passed in as well as the tournament they should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET roundStartTimes = ?, matchDuration = ?, breakLength = ?
                               WHERE tournamentName = ?;
                               """,(startTimes,duration,breakLength,tournamentName))
            #exectutes the previously designed SQL statement to add the round start times, match duration and break length to the current tournament
            connection.commit()
            #commit the addition of the round start times, match duration and break length to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the round start times, match duration and break length have been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns false signifying the round start times, match duration and break length have not been added to the current tournament successfully

    def addMatchScores(self, matchScores, tournamentName):
        #defines addMatchScores function, with the match scores to be added passed in as well as the tournament they should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET matchScores = ?
                               WHERE tournamentName = ?;
                               """,(matchScores,tournamentName))
            #executes the previously designed SQL statement to add the match scores to the current tournament
            connection.commit()
            #commit the addition of the match scores to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the match scores have been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns false signifying the match scores have not been added to the current tournament successfully


    def getTournamentName(self,viewCode):
        #defines getTournamentName function, with the view code to be checked for passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #creates a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT tournamentName FROM tournament WHERE viewCode = ?;""", [viewCode])
            #exectutes the previously designed SQL statement using the cursor to select the tournament name for the tournament with the view code that has been passed in
            results = cursor.fetchone()
            #fetches the tournament name if there is a tournament with a view code that matches the passed in view code
            connection.close()
            #close the connection to the database
            return results
            #returns the tournament name from the database if the tournament's view code matches the view code passed in
        except Exception as e:
            #if there was an error executing the SQL statement:
            connection.close()
            #close the connection to the database
            print(e)
            #print the error that has occured
            return False
            #returns false signifying the selection has not been completed