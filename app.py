from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db, Feedback
from forms import RegForm, LoginForm, FeedBackForm, FeedBackEditForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

ctx = app.app_context()
ctx.push()

@app.route("/") 
def redirecturl():
    return redirect("/register")


@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegForm()
    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(f"/users/{user.username}")

    return render_template("Register.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    form2 = LoginForm()
    if form2.validate_on_submit(): 
        username = form2.username.data
        password = form2.password.data
        user = User.authenticate(username, password)
        if user:   
            session["user_id"] = user.id
            return redirect(f"/users/{user.username}")
    return render_template("login.html", form2 = form2)

@app.route("/users/<username>")
def userdetails(username): 
    user = User.query.filter_by(username=username).first()

    if 'user_id' in session:
        return render_template("details.html", user = user)
    return redirect('/login')

@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def addpost(username):
    if "user_id" in session:
        user = User.query.filter_by(username=username).first()
        form3 = FeedBackForm()
    if form3.validate_on_submit(): 
        title = form3.title.data
        content = form3.content.data
        post = Feedback(title = title, content = content, fb_username = user.username)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/users/{ post.username.username }")
    else:
        redirect("/")
    return render_template("feedback.html", form3 = form3)


@app.route("/feedback/<feedback_id>/update", methods = ["GET", "POST"])
def updatepost(feedback_id):
    if "user_id" in session:
        feedback = Feedback.query.get_or_404(feedback_id)
        form4 = FeedBackForm(obj= feedback)
    if form4.validate_on_submit(): 
        feedback.title = form4.title.data
        feedback.content = form4.content.data
        db.session.commit()
        return redirect(f"/users/{ feedback.username.username }")
    else:
        redirect("/")
    return render_template("feedbackedit.html", form4 = form4, feedback = feedback)



@app.route("/logout")
def logout(): 
   session.pop("user_id")
   return redirect("/")



@app.route("/users/<username>/delete", methods = ["POST"])
def delete (username): 
    if "user_id" not in session:
        redirect("/")
    user = User.query.filter_by(username=username).first()
    if user.id == session["user_id"]:
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        return redirect("/")

    flash("you dont have permission to do that!!!", "danger")
    return redirect('/')

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def deletefeedback(feedback_id): 
    if "user_id" not in session:
        return redirect("/")
    
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    if feedback.fb_username != session["user_id"]:
        flash("You don't have permission to do that!", "danger")
        return redirect(f"/users/{feedback.fb_username}")
    
    
    flash("Feedback deleted successfully!", "success")
    return redirect("/")

