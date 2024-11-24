from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import (check_not_unique, check_validate_short_link,
                    generate_short_link)


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id'] != '':
        short = data['custom_id']
        if not check_validate_short_link(short):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if check_not_unique(short):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        data['custom_id'] = generate_short_link()

    url_map = URLMap(
        original=data['url'],
        short=data['custom_id'],
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200
