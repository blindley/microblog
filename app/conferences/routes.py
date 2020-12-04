from flask import flash, url_for, redirect, render_template

from app import db
from app.models import Conference
from app.conferences.forms import AddConferenceForm
from app.conferences import bp

@bp.route('/addconference', methods=['GET', 'POST'])
def addconference():
    form = AddConferenceForm()
    if form.validate_on_submit():
        conference = Conference(
                name=form.name.data,
                nickname=form.nickname.data,
                hq=form.hq.data,
                logo=form.logo.data,
                about=form.about.data
            )
        db.session.add(conference)
        db.session.commit()
        flash(f'Conference added.')
        return redirect(url_for('main.index'))
    return render_template('conferences/addconference.html', form=form)


@bp.route('/conferences')
def conferences():
    conferences = Conference.query.all()
    return render_template('conferences/conferences.html', conferences=conferences)
