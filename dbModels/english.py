from run import db

class English(db.Model):
    __tablename__ = "english"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), unique=True, index=True)

    def __init__(self, word):
        self.word = word
