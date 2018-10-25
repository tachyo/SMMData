class DBService:
    def __init__(self, conn):
        self.conn = conn
        self.db = conn.cursor()

    def persistLevelInfo(self, card):
        lvl = card[0]
        author = card[1]
        self.db.execute("INSERT OR IGNORE INTO Levels VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            lvl.id, lvl.name, lvl.theme, lvl.created, lvl.difficulty, lvl.tag,
            lvl.likes, lvl.played, lvl.shared, lvl.clearRate, lvl.triesTaken, lvl.triesSuccess, lvl.authorId))
        if author is not None:
            self.db.execute("INSERT OR IGNORE INTO authors VALUES (?,?,?,?)",
                       (author.id, author.name, author.medals, author.country))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()