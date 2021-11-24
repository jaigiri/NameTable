import uuid

from flask import Flask, render_template, redirect, url_for
import os

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = str(uuid.uuid4())

bootstrap = Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'data.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

db.create_all()


class Name(db.Model):
    __tablename__ = 'names'
    name = db.Column(db.String(50), unique=True, primary_key=True)


class NameForm(FlaskForm):
    name = StringField("Enter a name: ",  validators=[DataRequired()])
    submit = SubmitField("Add name")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        db.session.add(Name(name=form.name.data.title()))
        db.session.commit()
        form.name.data = ""
        return redirect(url_for('home'))
    return render_template("home.html", names=Name.query.limit(50).all(), form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
