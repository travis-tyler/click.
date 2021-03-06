import os
from flask import Flask, render_template, request, session, redirect, url_for, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY

# App setup
app = Flask(__name__)
app.secret_key = SECRET_KEY

# DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create user table model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(125), unique=True, nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User: {self.username}; Clicks: {self.clicks}>'

db.create_all()

# Session set up and set global stuff
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id'])[0]
        g.user = user
    g.total_clicks = db.session.query(func.sum(User.clicks))[0][0]
    # db.engine.execute(f'SELECT SUM(clicks) FROM User').fetchone()[0]
    g.leaderboard = db.session.query(User.username, User.clicks).order_by(desc(User.clicks)).limit(10)
    # db.engine.execute(f'SELECT username, clicks FROM User ORDER BY clicks DESC LIMIT 10').fetchall()

# Route for landing page
@app.route('/', methods=['GET', 'POST'])
def home():
    # Displays total clicks and leaderboard whether user in session or not
    return render_template('index.html', total_clicks=g.total_clicks, leaderboard=g.leaderboard)

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)
    if request.method == 'POST':
        # End session
        username = request.form['username']
        password_1 = request.form['password']

        # Check if user exists and hashed pw matches
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password_1):
            # Start session and redirect to profile
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        # On failed login, redirect back to login page
        # TODO: Add message/alert
        return redirect(url_for('login'))

    return render_template('login.html')

# Route for account creation
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # End existing session
    session.pop('user_id', None)
    if request.method == 'POST':
        session.pop('user_id', None)

        # Get account info
        username = request.form['username']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']

        # Check if username already exists
        if db.session.query(User.id).filter_by(username=username).scalar() is None:
            # Check that both passwords match
            if password_1 == password_2:
                # Generate a hashed pw and check if it already exists
                hashed_password = generate_password_hash(password_1, method='sha256')
                if db.session.query(User.id).filter_by(password=hashed_password).scalar() is None:
                    # Create new user and add and commit to DB
                    new_user = User(username=username, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
        
                    return redirect(url_for('login'))

    # TODO: Add fail message/alert
    return render_template('signup.html')

# Route for profile
@app.route('/profile', methods=['POST', 'GET'])
def profile():

    # Redirect to login if not in session
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html', leaderboard=g.leaderboard)

@app.route('/api/clickdata', methods=['GET', 'POST'])
def data():

    if request.method == 'POST':
        # Add 1 to current users click total (User.clicks) if button pressed
        g.user.clicks += 1
        db.session.commit()

    # Return dictionary of click data to api
    click_data = [{
        'user_clicks':g.user.clicks, 
        'total_clicks':db.session.query(func.sum(User.clicks))[0][0],
        'leaderboard':{'users':[], 'clicks':[]}
    }]

    # Add top usernames and number of clicks to lists in API data
    new_leaderboard = db.session.query(User.username, User.clicks).order_by(desc(User.clicks)).limit(10)
    for i in range(0, 6):
        click_data[0]['leaderboard']['users'].append(new_leaderboard[i][0])
        click_data[0]['leaderboard']['clicks'].append(new_leaderboard[i][1])

    return jsonify(click_data)


if __name__=='__main__':
    app.run(debug=True)