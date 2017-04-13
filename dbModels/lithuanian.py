from run import db


# Create our database model
class Lithuanian(db.Model):
    __tablename__ = "lithuanian"

    id = db.Column(db.Integer, primary_key=True)
    english_id = db.Column(db.Integer, db.ForeignKey('english.id'))
    english = db.relationship('English', cascade="all,delete",
                               backref=db.backref('lithuanian', lazy='dynamic'))
    word = db.Column(db.String(120))
    link = db.Column(db.String(220),  nullable=True)


    def __init__(self,english, word,link=None):
        self.english=english
        self.word = word
        self.link=link

