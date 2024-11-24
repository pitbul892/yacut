import random
import re
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .constants import MAX_GENERATE_LiNK, MAX_SHORT_LINK
from .forms import UrlMapForm
from .models import URLMap


def generate_short_link(length=MAX_GENERATE_LiNK):
    characters = string.ascii_letters + string.digits
    short_link = ''.join(random.choices(characters, k=length))
    if check_not_unique(short_link):
        return generate_short_link()
    return short_link


def check_not_unique(short):
    return URLMap.query.filter_by(short=short).first() is not None


def check_validate_short_link(short):
    return re.findall('^[a-zA-Z0-9]+$', short) and len(short) <= MAX_SHORT_LINK


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if not form.validate_on_submit():
        return render_template('new_link.html', form=form)
    short = form.custom_id.data
    if short is not None and short != '':
        if not check_validate_short_link(short):
            flash('Указано недопустимое имя для короткой ссылки')
            return render_template('new_link.html', form=form)
        if check_not_unique(short):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('new_link.html', form=form)
    else:
        short = generate_short_link()
    url_map = URLMap(
        original=form.original_link.data,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()
    return render_template(
        'new_link.html',
        form=form,
        link=url_for('redirect_link', short=url_map.short, _external=True)
    )


@app.route('/<short>')
def redirect_link(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
