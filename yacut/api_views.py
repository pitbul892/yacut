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
    if 'custom_id' in data and data['custom_id'] != '':
        short = data['custom_id']
        try:
            URLMap.validate_short_link(short)
        except ValueError as e:
            raise InvalidAPIUsage(str(e))
    else:
        data['custom_id'] = URLMap.generate_short_link()
    url_map = URLMap.from_dict(data['url'], data['custom_id'])
    url_map.save()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
