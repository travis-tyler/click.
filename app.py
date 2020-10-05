from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    clicks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Number of clicks %r>' % self.clicks

@app.route('/', methods=["GET", "POST"])
def home():
    click_num = db.session.query(Clicks).filter(Clicks.title == 'click_num').one()
    if request.method == "POST":
        click_num.clicks += 1
        db.session.commit()
        print(click_num)
        return render_template("index.html", click_num=click_num.clicks)
    return render_template("index.html", click_num=click_num.clicks)

if __name__=='__main__':
    app.run(debug=True)