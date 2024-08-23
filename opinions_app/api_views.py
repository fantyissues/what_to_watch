from http import HTTPMethod, HTTPStatus

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
