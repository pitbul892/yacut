import random
import re
from datetime import datetime

from flask import url_for

from yacut import db

from .constants import (CHARACTERS, MAX_ATTEMPTS, PATTERN_FOR_SHORT_LINK,
                        MAX_GENERATE_LiNK)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_link',
                               short=self.short,
                               _external=True
                               )
        )

    @classmethod
    def from_dict(cls, original, short):
        return cls(
            original=original,
            short=short
        )

    @classmethod
    def get(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def generate_short_link(cls, length=MAX_GENERATE_LiNK, max=MAX_ATTEMPTS):
        characters = CHARACTERS
        attemts = 0
        while attemts <= max:
            short_link = ''.join(random.choices(characters, k=length))
            if not cls.check_not_unique(short_link):
                return short_link
            attemts += 1
        raise ValueError('Больше нет вариантов вариантов кротких ссылок.')

    @staticmethod
    def check_not_unique(short):
        return URLMap.query.filter_by(short=short).first() is not None

    @staticmethod
    def check_validate_short_link(short):
        return re.findall(PATTERN_FOR_SHORT_LINK, short)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def validate_short_link(cls, short):
        if not cls.check_validate_short_link(short):
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        if cls.check_not_unique(short):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
