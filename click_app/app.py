from flask import Flask, render_template, request, session, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkeydonttellanyone'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id'])[0]
        g.user = user

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User: {self.username}; Clicks: {self.clicks}>'

@app.route('/', methods=['GET', 'POST'])
def home():
    # if not g.user:
    #     return redirect(url_for('login'))

    total_clicks = db.engine.execute(f'SELECT SUM(clicks) FROM User').fetchone()[0]

    if request.method == 'POST':
        if request.form['login']:
            return redirect(url_for('login'))
        if request.form['signup']:
            return redirect(url_for('signup'))

    return render_template('index.html', total_clicks=total_clicks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username)[0]
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session.pop('user_id', None)
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']

        if db.session.query(User.id).filter_by(username=username).scalar() is None:

            if password_1 == password_2:

                if db.session.query(User.id).filter_by(password=password_1).scalar() is None:

                    new_user = User(username=username, password=password_1)
                    db.session.add(new_user)
                    db.session.commit()
        
                    return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if not g.user:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        g.user.clicks += 1
        db.session.commit()
        return render_template("profile.html", click_num=g.user.clicks)

    return render_template('profile.html', click_num=g.user.clicks)


if __name__=='__main__':
    app.run(debug=True)