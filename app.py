import requests
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, PasswordField, EmailField, SelectField, RadioField, TextAreaField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.csrf import CSRFProtect


# Create a Flask Instance
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "my_secret_key"

countries_api = 'https://restcountries.com/v2/all'
countries_response = requests.get(countries_api).json()
countries = []
for elem in countries_response:
    countries.append(list(elem.items())[0][1])

# [] = square brakets
# {} = curly braquets
# () = parenthesis


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# Create a Form Class
class MainForm(FlaskForm):
    subject_choices = [("fix", "Réparation"), ("order", "Commande"), ("other", "Autres")]
    genres = ["M", "F", "X"]
    name = StringField('Quelle est votre prénom', validators=[DataRequired()]) # 1
    family_name = StringField('Quelle est votre nom', validators=[DataRequired()]) # 2
    email = EmailField('Quelle est votre e-mail', validators=[DataRequired(), Email(message="Vous devez entrer un e-mail valide")]) # 3
    password = PasswordField("Mot Clé", validators=[DataRequired(), Length(min=8, message="Votre mot de passe doit avoir un minimum de 8 character")]) # 4
    country = SelectField("Quelle est votre pays d'origine", validators=[DataRequired()], choices=countries) # 5
    genre = RadioField('Quelle est votre genre', validators=[DataRequired()], choices=genres) # 6
    subjects = MultiCheckboxField('Quelle sont les sujets qui vous interesse', choices=subject_choices) # 7
    message = TextAreaField('Quelle est votre message', validators=[DataRequired()]) # 8
    message1 = TextAreaField('Message extra', validators=[DataRequired()]) # 9
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


# XSS Defense
name_replacements = {
    '<': '',
    '>': '',
    '=': '',
    '"': '',
    '”': '',
    '`': '',
    "'": '',
    '%': '',
    '&': '',
    '!': '',
    '@': '',
    '#': '',
    '$': '',
    '(': '',
    ')': '',
    '{': '',
    '}': '',
    '[': '',
    ']': '',
    '|': '',
    '/': '',
    "\\": '',
    '?': '',
    '+': '',
    '-': '',
    '_': '',
    '*': '',
    '^': '',
    'ˆ': '',
    '˜': '',
    '~': '',
    '.': '',
    ',': '',
    ':': '',
    ';': '',
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': '',
    '6': '',
    '7': '',
    '8': '',
    '9': ''
}

message_replacements = {
    '<': '&lt',
    '>': '&gt',
    '=': '&eq',
    '"': '&quot',
    '”': '&quot',
    "'": '&apos',
    '&': '&amp',
    # '%': '',
    # '!': '',
    # '@': '',
    # '#': '',
    # '$': ''
}


def replace_all(input_str, dic):
    for i, j in dic.items():
        input_str = input_str.replace(i, j)
    return input_str


# Create Form Page
@app.route('/main-form', methods=['GET', 'POST'])
def main_form():
    name = None # 1
    family_name = None # 2
    email = None # 3
    password = None # 4
    country = None # 5
    genre = None # 6
    subjects = None # 7
    message = None # 8
    message1 = None # 8
    form = MainForm()

    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        family_name = replace_all(form.family_name.data, name_replacements)
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
        message = replace_all(form.message.data, message_replacements)
        form.message.data = ''
        message1 = form.message1.data
        form.message1.data = ''

        return render_template('success.html',
                               name=name, # 1 
                               family_name=family_name, # 2
                               email=email, # 3
                               password=password, # 4
                               country=country, # 5
                               genre=genre, # 6
                               subjects=subjects, # 7
                               message=message, # 8
                               message1=message1) # 9

    return render_template('main_form.html',
                           name=name,
                           family_name=family_name,
                           email=email,
                           password=password,
                           country=country,
                           genre=genre,
                           subjects=subjects,
                           message=message,
                           message1=message1,
                           form=form)


if __name__ == '__main__':
    app.run(debug=True)
