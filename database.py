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
                                    rounds text,
                                    FOREIGN KEY (username) REFERENCES user(username),
                                    CHECK (length(TournamentName)>4 AND length(TournamentName)<30)
                            )''')
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def createTournament(self,tournamentName,currentUser,numTeams,brackets):
        try:
            connection = sql.connect(self.name)
            connection.execute("""INSERT INTO tournament 
                               VALUES (?,?,?,false,?)
                               """,(tournamentName,currentUser,numTeams,brackets))
            connection.commit()
            connection.close()
            return True
        except:
            connection.close()
            return False





    # def createTournamentTables(self):
    #     connection = sql.connect(self.name)
    #     connection.execute("""CREATE TABLE IF NOT EXISTS tournament(
    #                 tournamentName text PRIMARY KEY,
    #                 username text,
    #                 numTeams integer NOT NULL,
    #                 FOREIGN KEY (username) REFERENCES user(username),
    #                 teamNames array NOT NULL,
    #                 CHECK (length(TournamentName)>4 AND length(TournamentName)<30)
    #                        );""")




        #     def createTournament(self, tournamentName, username, numTeams, teamNames):
        # connection = sql.connect(self.name)
        # try:
        #     connection.execute("""INSERT INTO tournament
        #         VALUES (?,?,?)""",
        #         (tournamentName,username,numTeams,teamNames())
        #         )
        #     connection.commit()
        #     connection.close()
        #     return True
        # except:
        #     connection.close()
        #     return False
