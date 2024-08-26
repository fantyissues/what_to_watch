from http import HTTPMethod, HTTPStatus
from random import randrange

from flask import request

from . import app, db
from .models import Opinion


@app.route('/api/opinions/<int:id>/', methods=[HTTPMethod.GET])
def get_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    return {'opinion': opinion.to_dict()}, HTTPStatus.OK


@app.route('/api/opinions/<int:id>/', methods=[HTTPMethod.PATCH])
def update_opinion(id):
    data = request.get_json()
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
    data = request.get_json()
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return {'opinion': opinion.to_dict()}, HTTPStatus.CREATED


@app.route('/api/get-random-opinion/', methods=[HTTPMethod.GET])
def get_random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return {'opinion': opinion.to_dict()}, HTTPStatus.OK
