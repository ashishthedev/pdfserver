from flask import Blueprint, render_template, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


webapp = Blueprint('webapp', __name__)


class UrlSubmissionForm(Form):
    weburl = StringField("Please enter the web url you want to convert to pdf", validators=[Required()])
    submit = SubmitField("Submit")

@webapp.route('/', methods=['GET', 'POST'])
def home():
    form = UrlSubmissionForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('home.html', form=form)
