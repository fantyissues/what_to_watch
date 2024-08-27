from http import HTTPMethod, HTTPStatus
from random import randrange

from flask import request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=[HTTPMethod.GET])
def get_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    return {'opinion': opinion.to_dict()}, HTTPStatus.OK


@app.route('/api/opinions/<int:id>/', methods=[HTTPMethod.PATCH])
def update_opinion(id):
    data = request.get_json()
    if (
        'text' in data and
        Opinion.query.filter_by(text=data['text']).first() is not None
    ):
        return ({'error': 'Такое мнение уже есть в базе данных'},
                HTTPStatus.BAD_REQUEST)
    opinion = Opinion.query.get_or_404(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return {'opinion': opinion.to_dict()}, HTTPStatus.OK


@app.route('/api/opinions/<int:id>/', methods=[HTTPMethod.DELETE])
def delete_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT


@app.route('/api/opinions/', methods=[HTTPMethod.GET])
def get_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return {'opinions': opinions_list}, HTTPStatus.OK


@app.route('/api/opinions/', methods=[HTTPMethod.POST])
def add_opinion():
    data = request.get_json(silent=True)
    if data is None or 'title' not in data or 'text' not in data:
        return ({'error': 'В запросе отсутствуют обязательные поля'},
                HTTPStatus.BAD_REQUEST)
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        return ({'error': 'Ефкое мнение уже есть в базе данных'},
                HTTPStatus.BAD_REQUEST)
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return {'opinion': opinion.to_dict()}, HTTPStatus.CREATED


@app.route('/api/get-random-opinion/', methods=[HTTPMethod.GET])
def get_random_opinion():
    opinion = random_opinion()
    return {'opinion': opinion.to_dict()}, HTTPStatus.OK
