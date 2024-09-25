from datetime import datetime, timezone
from flask import Flask, render_template, session, redirect, url_for, flash
import re
from flask_wtf import FlaskForm
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, Regexp, ValidationError, InputRequired
from wtforms import StringField, SubmitField

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'a_very_secret_key' 


class CustomRegexp(Regexp):
    def __init__(self, regex, flags=0, message=None):
        # Call the parent constructor (Regexp)
        super().__init__(regex, flags, message)
        
        # Initialize the field_flags attribute
        self.field_flags = {"required": True}  # Default value if not provided
        

    def __call__(self, form, field, message=None):
        match = self.regex.match(field.data or "")
        if match:
            return match

        if message is None:
            if self.message is None:
                message = field.gettext(f"Please include an '@' in the email address. {field.data} is missing an '@'.")
            else:
                message = self.message
        field.errors[:] = []
        raise ValidationError(message)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    utemail = StringField('What is your UofT Email address?', validators=[CustomRegexp(regex=r'^\S+@\S')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('utemail')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.utemail.data and "utoronto" in form.utemail.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        if "utoronto" in form.utemail.data:
            session['utemail'] = form.utemail.data
        return redirect(url_for('index'))
    utemail_ = session.get("utemail")
    if utemail_ == None:
        utemail_ = ''
    return render_template('index.html', form = form, name = session.get('name'), utemail = session.get("utemail"), isut = "utoronto" in utemail_)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)