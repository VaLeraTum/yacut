from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if URLMap.query.filter_by(short=form.custom_id.data).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    if not form.custom_id.data:
        form.custom_id.data = get_unique_short_id()
    new_url = URLMap(original=form.original_link.data, short=form.custom_id.data)
    db.session.add(new_url)
    db.session.commit()
    return render_template('index.html', form=form, result_url=url_for('index_view', _external=True) + new_url.short)


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    old_url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(old_url.original)
