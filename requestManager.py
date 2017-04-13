import flask_login
from flask import render_template, request, redirect, url_for
from dbModels.english import English
from dbModels.lithuanian import Lithuanian
from dbModels.users import Users
from run import db, app, bcrypt, login_manager
from sqlalchemy import func


@app.route('/search', methods=['GET'])
def getSeachResultPage():
    if request.method == 'GET':
        word = request.args.get('word')
        wordLow = func.lower(word)
        expanded = request.args.get('expanded')
        if expanded:
            q = db.session.query(English.word, Lithuanian.word, Lithuanian.link).join(Lithuanian).filter(func.lower(
                English.word).like('%' + wordLow + '%'))
        else:
            q = db.session.query(English.word, Lithuanian.word, Lithuanian.link).join(Lithuanian).filter(
                func.lower(English.word).like(wordLow +
                                  '%')).all()
        found=dictFormating(q)
        return render_template('pageByLetter.html', letter=word, dictionary=found)
    return render_template('index.html')

@app.route('/result/<letter>')
def getEnglishPage(letter):
    q = db.session.query(English.word,Lithuanian.word,Lithuanian.link).join(Lithuanian).filter(func.lower(English.word).like(
        letter +
                                                                                                     '%')).all()
    found = dictFormating(q)
    return render_template('pageByLetter.html', letter=letter, dictionary=found)

def dictFormating(listOfWords):
    found = []
    for words in listOfWords:
        ltWord = {}
        ltWord[words[1]] = words[2]
        if found:
            if found[len(found) - 1]['english'] == words[0]:
                found[len(found) - 1]['lithuanian'].update(ltWord)
            else:
                found.append({'english': words[0], 'lithuanian': ltWord})
        else:
            found.append({'english': words[0], 'lithuanian': ltWord})
    return found

@app.route('/')
def index():
    return render_template('index.html')

@flask_login.login_required
@app.route('/add', methods=['POST'])
def addToDictionary():
    if request.method == 'POST':
        engWord = request.form['engWord']
        ltWord = request.form['ltWord']
        if 'link' in request.form:
            link = request.form['link']
        else:
            link = None
        query = db.session.query(English).filter(English.word == engWord)
        if query.count():
            english = query.first()
        else:
            english = English(engWord)
            db.session.add(english)
        regLt = Lithuanian(english, ltWord, link)
        db.session.add(regLt)
        db.session.commit()
        return "Done with word: " + engWord
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        try:
            userName = request.form['user']
            password = request.form['password']
            user = Users.query.get(userName)
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    flask_login.login_user(user)
                    return redirect(url_for('index'))
        except Exception:
            pass
    error="Blogi prisijungimo duomenys"
    return render_template('index.html', error=error)

@app.route("/manage/<word>")
@app.route("/manage",methods=["GET", "DELETE","PUT"])
@flask_login.login_required
def manage(word=''):
    if request.method == 'GET':
        q = db.session.query(English.word, Lithuanian.word, Lithuanian.link, English.id).join(Lithuanian).filter(
            English.word ==
                                                                                                     word)
        found = dictFormating(q)
        return render_template("manage.html", dictionary=found, id=q.first()[3])
    if request.method == 'DELETE':
        id = request.form['id']
        eng = db.session.query(English).filter(English.id == id).first()
        db.session.delete(eng)
        db.session.commit()
        return "Žodis ištrintas"
    if request.method == 'PUT':
        id = request.form['id']
        eng = request.form['eng']
        ltWords={}
        form = request.form
        for i in range(1,len(form)-2,2):
            link=form["link"+str(i)]
            ltWords[form["lt" + str(i)]]=link
        q = db.session.query(English).filter(English.id == id).first()
        q.word=eng
        for lt in q.lithuanian:
            key,value=ltWords.popitem()
            lt.link=value
            lt.word=key
        db.session.commit()
        return "Žodis pakeistas"
    return redirect(url_for('index'))


@app.route("/logout", methods=["POST"])
@flask_login.login_required
def logout():
    """Logout the current user."""
    flask_login.logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def userLoader(userName):
    return Users.query.get(userName)