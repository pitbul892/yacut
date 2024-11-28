from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short = data.get('custom_id', None)
    url_map = URLMap.from_dict(data['url'], short)
    try:
        url_map.save()
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
