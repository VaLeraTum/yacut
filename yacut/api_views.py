from flask import jsonify, request, url_for
import re
import http

from . import app, db
from .error_handelers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


def validate_short(short_id):
    match = re.match(r'^[a-zA-Z\d]{1,16}$', short_id)
    return match is not None and match.group() == short_id


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    original, short = data['url'], None
    if ('custom_id' in data and data['custom_id'] is not None and data['custom_id'] != ''):
        short = data['custom_id']
        if not validate_short(short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    if not short:
        short = get_unique_short_id()
    new_url = URLMap(original=original, short=short)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({
        'url': new_url.original,
        'short_link': url_for('index_view', _external=True) + new_url.short
    }), http.HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    old_url = URLMap.query.filter_by(short=short_id).first()
    if not old_url:
        raise InvalidAPIUsage('Указанный id не найден', http.HTTPStatus.NOT_FOUND)
    return jsonify({'url': old_url.original}), http.HTTPStatus.OK
