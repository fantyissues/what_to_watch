import os
from datetime import datetime, timezone
from random import randrange

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI',
                                                  'sqlite:///db.sqlite3')
db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now(timezone.utc))


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return 'В базе данных мнений о фильмах нет.'
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return opinion.text


if __name__ == '__main__':
    app.run()
