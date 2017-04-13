import string
from flask import Flask
from flask.ext.login import LoginManager, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://adelina:password@localhost/adelina"
app.secret_key = 'paslaptis'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

@app.context_processor
def injectGlobals():
    abc = list(string.ascii_lowercase)
    userName=None
    if current_user.is_authenticated:
        userName = current_user.get_id()  # return username in get_id()
    return dict(letters=abc,userName=userName)




if __name__ == '__main__':
    from dbModels.lithuanian import *
    from dbModels.english import *
    from dbModels.users import *
    from requestManager import *
    db.create_all()
    import logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run()
