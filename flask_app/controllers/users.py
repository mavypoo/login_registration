from flask_app import app
from flask import render_template, redirect, request, session, flash
# Import your models
from flask_app.models import user  # Import user model 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) # we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument


# / roote route for showing the login/registration page
@app.route("/")
def home():
    return render_template("login_reg.html")


# /dashboard - shows the dashboard - but you must be logged in 
@app.route("/dashboard")
def dashboard():
    # Check to see if someone is logged in - if not , send them back to the login/registration page. if someones not logged in they cant access those pages. 
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    logged_in_user = user.User.get_by_id(data)
    return render_template("dashboard.html", user = logged_in_user)

# /register (INVISIBLE POST route) - handles registering a new user 
@app.route("/register", methods=["POST"])
def register():
    # Validate if the form data is good or not 
    if not user.User.validate_registration(request.form):
        # If the validation fails, redirect back to the route that has that form. -- redirect("/")
        return redirect("/")
    # Save in the database by creating a dictionary
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    # Call on the model to save in the database
    session["user_id"] = user.User.register_user(data) # Save the ID in session - it will identify the user logged in
    # Redirect to /dashboard if succeed
    return redirect("/dashboard")

# /login (INVISIBLE POST route) - logs a user in 
@app.route("/login", methods=["POST"])
def login():
    # Validate- check if the email exist, if so, check if the password is correct. 
    if not user.User.validate_login(request.form):
        # If the validation fails, redirect back to the route that has that form. -- redirect("/")
        return redirect("/")
    data = {
        "email": request.form["email"]
    }
    logged_in_user = user.User.get_by_email(data)
    # Save ID in session. 
    session["user_id"] = logged_in_user.id
    # Redirect to /dashboard. 
    return redirect("/dashboard")

# /logout (INVISIBLE route) - clears session, sends the user back to login/registration page. 
@app.route("/logout")
def logout():
    # Clear session 
    session.clear() # Removes the user from session 
    # Redirect to login/registration route 
    return redirect("/")