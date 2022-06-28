from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, RadioField, TextAreaField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Email

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my_secret_key"


# Create a Form Class
class MainForm(FlaskForm):
    name = StringField('Quelle est votre prénom', validators=[DataRequired()])
    family_name = StringField('Quelle est votre nom', validators=[DataRequired()])
    email = EmailField('Quelle est votre e-mail', validators=[DataRequired()])
    password = PasswordField("Mot Clé")
    country = SelectField("Quelle est votre pays d'origine", validators=[DataRequired()])
    genre = RadioField('Quelle est votre genre', validators=[DataRequired()])
    subjects = SelectMultipleField('Quelle sont les sujets qui vous interesse')
    message = TextAreaField('Quelle est votre message', validators=[DataRequired()])
    submit = SubmitField("Soumettre")


# Create a Route Decorator
@app.route('/')
def index():
    return render_template('index.html')


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Create Example Page
@app.route('/example')
def example():
    return render_template('example.html')


# Create Form Page
@app.route('/main-form', methods=['GET', 'POST'])
def main_form():
    name = None
    family_name = None
    email = None
    password = None
    country = None
    genre = None
    subjects = None
    message = None
    form = MainForm()

    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        family_name = form.family_name.data
        form.family_name.data = ''
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''
        country = form.country.data
        form.country.data = ''
        genre = form.genre.data
        form.genre.data = ''
        subjects = form.subjects.data
        form.subjects.data = ''
        message = form.message.data
        form.message.data = ''

    # Try to pass all variables inside a list
    # Then do a loop for to render inside the form
    return render_template('main_form.html',
                           name=name,
                           family_name=family_name,
                           email=email,
                           password=password,
                           country=country,
                           genre=genre,
                           subjects=subjects,
                           message=message,
                           form=form)
