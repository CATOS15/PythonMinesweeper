import mysql.connector

class Database:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="130.225.170.81",
            user="root",
            password="kagemand123",
            database="minesweeper"
        )
        ## Global cursor
        cur = self.con.cursor()
        print("Connection established")

    def get_highscores(self):
        self.cur.execute("SELECT * FROM higscores")
        return self.cur.fetchall()


    def insert_highscore(self,width,height,timer,numberOfPlayers,usernames):
        ## Creat user if no name exist
        sql = "INSERT INTO highscores (width,height,timer,numberOfPlayers,usernames) VALUES (%d, %d, %d, %d, %s)"
        val = (width,height,timer,numberOfPlayers,usernames)
        ##val = (24, 24, 200, 4, 'oliver, frost, tobi, soeren')
        self.cur.execute(sql, val)

        self.con.commit()





