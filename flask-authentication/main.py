from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Use flask-login to manage logins and logouts
login_manager = LoginManager()
login_manager.init_app(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()

        if user:
            flash("You've already signed up with this email! Log in instead.")
            return redirect(url_for('login'))
        else:
            new_user = User(
                name=request.form.get('name'),
                email=request.form.get('email'),
                password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
            )
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)

            return redirect(url_for('secrets'))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
        if user is None:
            flash("No user with this email address was found! Please try again.")
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, request.form.get('password')):
            flash("You entered the wrong password! Please try again.")
            return redirect(url_for('login'))

        else:
            login_user(user)
            flash("Logged in successfully :)")
            return redirect(url_for('secrets'))


    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", logged_in=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods=["POST"])
@login_required
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
