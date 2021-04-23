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
        self.cur = self.con.cursor()

    def get_highscores(self):
        self.cur.execute("SELECT * FROM Highscore")
        return self.cur.fetchall()

    def insert_highscore(self,width,height,timer,numberOfPlayers,usernames):
        ## Creat user if no name exist
        sql = "INSERT INTO Highscore (width,height,timer,numberOfPlayers,usernames) VALUES (%s, %s, %s, %s, %s)"
        val = (width,height,timer,numberOfPlayers,usernames)
        self.cur.execute(sql, val)
        self.con.commit()

    def disconnect(self):
        self.con.close()