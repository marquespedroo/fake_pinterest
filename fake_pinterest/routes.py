from flask import render_template, url_for, redirect
from fake_pinterest import app, database, bcrypt
from fake_pinterest.models import User, Posts
from flask_login import login_required, login_user, logout_user, current_user
from fake_pinterest.forms import FormLogin, FormCreateAccount, FormPhoto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin() 
    user = User.query.filter_by(email=formlogin.email.data).first()
    if user and bcrypt.check_password_hash(user.password, formlogin.password.data):
        login_user(user)
        return redirect(url_for("profile", user_id=user.id))
    return render_template('homepage.html', form=formlogin)

@app.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    formcreateaccount = FormCreateAccount()
    if formcreateaccount.validate_on_submit():
        password = bcrypt.generate_password_hash(formcreateaccount.password.data)
        user = User(username=formcreateaccount.username.data , password=password, email=formcreateaccount.email.data)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))

    return render_template("createaccount.html", form=formcreateaccount)


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        form_photo = FormPhoto()
        if form_photo.validate_on_submit():
            file = form_photo.photo.data
            safe_name = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], safe_name)
            file.save(path)
            photo = Posts(image=safe_name, user=current_user)
            database.session.add(photo)
            database.session.commit()

        return render_template("profile.html", user=current_user, form=form_photo)
    
    else:
        user = User.query.get(int(user_id))
        return render_template('profile.html', user=user, form=None)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def  feed():
    photos = Posts.query.order_by(Posts.created_at.desc()).all()
    return render_template("feed.html",photos=photos)