from flask import flash, redirect, render_template, url_for

from . import app
from .forms import UrlMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if not form.validate_on_submit():
        return render_template('new_link.html', form=form)
    short = form.custom_id.data
    if short:
        try:
            URLMap.validate_short_link(short)
        except ValueError as e:
            flash(str(e))
            return render_template('new_link.html', form=form)

    else:
        short = URLMap.generate_short_link()
    url_map = URLMap.from_dict(form.original_link.data, short)
    url_map.save()
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
