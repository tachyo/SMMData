class Level:
    def __init__(self, levelId=None, name=None, theme=None, created=None, difficulty=None,
                 tag=None, likes=None, played=None, shared=None, triesTaken=None, triesSuccess=None, authorId=None):
        self.id = levelId
        self.name = name
        self.theme = theme
        self.created = created
        self.difficulty = difficulty
        self.tag = tag
        self.likes = likes
        self.played = played
        self.shared = shared
        self.triesTaken = triesTaken
        self.triesSuccess = triesSuccess
        self.authorId = authorId