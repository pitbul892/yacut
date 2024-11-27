from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Regexp

from .constants import PATTERN_FOR_SHORT_LINK


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Regexp(PATTERN_FOR_SHORT_LINK)]
    )
    submit = SubmitField('Создать')
