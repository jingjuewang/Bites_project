from flask import Flask, redirect, render_template, request, url_for
from flask_login import (current_user, LoginManager, login_required,
                         login_user, logout_user, UserMixin)
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import check_password_hash, generate_password_hash
from plot_map import plotMap
from order_data import *

# Create and configure an app.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
order_data = pd.read_csv('order_data.csv')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/', methods=['GET', 'POST'])
def foo():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/city", methods=['GET', 'POST'])
def citymap():
    """
    Generate the city map (currently only san francisco)
    Currently only map and markers
    """
    plotMap()
    with open('mapPlot.html', 'r') as f:
        text = f.read()
    maps = text.split('<body>')[1].split('</body>')[0]
    with open('templates/map.html', 'r') as f:
        text = f.read()
    map_html = maps.join(text.split('{ map }'))
    with open('templates/citymap.html', 'w') as f:
        f.write(map_html)
    return render_template('citymap.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    """
    Generate the order page
    """
    item = request.form.get('item')
    day = request.form.get('day')

    filt = {'data': order_data, 'item': item, 'day': day}
    new_order_data = select_data(**filt)
    new_order_data = [(d[0], d[1], d[2]) for d in
                      zip(list(new_order_data['name']),
                          list(new_order_data['items']),
                          list(new_order_data['days']))]

    return render_template('order.html', order_data=new_order_data)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', fail=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['userpassword']
    email = request.form['useremail']

    user_name_count = User.query.filter_by(username=username).count()
    user_email_count = User.query.filter_by(email=email).count()
    if(user_name_count > 0 or user_email_count > 0):
        return render_template('signup.html', fail=True)
    else:
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return render_template('signin.html',
                               register_success=True, login_fail=False)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('signin.html',
                           register_success=False, login_fail=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    password = request.form['userpassword']
    username = request.form['username']

    user = User.query.filter_by(username=username).first()

    # Login and validate the user.
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for('user', username=username))
    else:
        return render_template('signin.html',
                               register_success=False, login_fail=True)


@login_manager.user_loader
def load_user(id):  # id is the ID in User.
    return User.query.get(int(id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout_success.html')


@app.route('/user/<username>')
@login_required
def user(username):
    return render_template('user.html', username=username)


if __name__ == '__main__':
    # login_manager needs to be initiated before running the app
    login_manager.init_app(app)
    # flask-login uses sessions which require a secret Key
    app.secret_key = os.urandom(24)

    # Create tables.
    db.create_all()
    db.session.commit()

    app.run(host='0.0.0.0', port=5000, debug=True)
