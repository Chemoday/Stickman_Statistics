from flask import render_template, url_for
from models.statistics.models import Admins
from . import main_bp
from .forms import NameForm


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        Admins.create(username=form.name.data)
        return url_for('.index')
    return render_template('index.html', form=form)

