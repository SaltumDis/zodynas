import flask_login

from run import db, bcrypt


# Create our database model
class Users(db.Model, flask_login.UserMixin):
    __tablename__ = "users"

    name = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.name = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')



    def get_id(self):
        """Return the user name to satisfy Flask-Login's requirements."""
        return self.name



