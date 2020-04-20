from flask import Flask, render_template, redirect, request, url_for, send_file, flash
from flask_login import login_required, current_user, UserMixin, LoginManager,login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
    
app=Flask(__name__)
app.config['SECRET_KEY'] = 'IAMSECRETOKSANA'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    user_database = {"oksana": ("oksana", "task3"),
               "oksana2": ("oksana2", "login")}
    def __init__(self, username, password):
        self.id = username
        self.password = password
        
    @classmethod
    def getuser(cls,username):
        return User(username,cls.user_database.get(username)[1])
    
    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

@login_manager.user_loader
def load_user(username):
    return User.getuser(username)

def load_user_class(username,password):
    user_entry = User.get(username)
    if (user_entry is not None):
        user = User(user_entry[0],user_entry[1])
        if (user.password == password):
            return user
    return None

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

#When we go to localhost:5000/ , visit login page
@app.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data
        u = load_user_class(user,password)
        if u is not None:
            login_user(u)
            flash("Successfully logged in")
            return redirect(url_for('cabinet'))
        else:
            flash( "Wrong login credentials")
    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template("logout.html")


#Secret page cabinet, only when authenticated

@app.route('/cabinet', methods=['GET'])
@login_required
def cabinet():
    error = None
    print(current_user)
    return render_template('cabinet.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
