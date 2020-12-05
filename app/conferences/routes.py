from flask import flash, url_for, redirect, render_template, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Conference
from app.conferences.forms import AddConferenceForm, EditConferenceForm, AddOrEditConferenceForm
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

@bp.route('/conferences/<int:id>')
def conference(id):
    conference = Conference.query.filter_by(id=id).first_or_404()
    return render_template('conferences/conference.html', conference=conference)

@bp.route('/edit_conference/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_conference(id):
    if not current_user.admin:
        abort(403)
    conference = Conference.query.filter_by(id=id).first_or_404()
    form = AddOrEditConferenceForm(original_conference=conference)
    if form.validate_on_submit():
        conference.name = form.name.data
        conference.nickname = form.nickname.data
        conference.hq = form.hq.data
        conference.logo = form.logo.data
        conference.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('conferences.edit_conference', id=id))
    elif request.method == 'GET':
        form.name.data = conference.name
        form.nickname.data = conference.nickname
        form.hq.data = conference.hq
        form.logo.data = conference.logo
        form.about.data = conference.about
    return render_template('conferences/edit_conference.html', title='Edit Conference',
                           form=form)
