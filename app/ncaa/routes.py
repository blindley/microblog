from flask import flash, url_for, redirect, render_template, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Conference, Team
from app.ncaa.forms import AddConferenceForm, EditConferenceForm, AddOrEditTeamForm
from app.ncaa import bp


@bp.route('/conferences')
def conferences():
    conferences = Conference.query.all()
    return render_template('ncaa/conferences.html', title='Conferences', conferences=conferences)

@bp.route('/conference/<int:id>')
@bp.route('/conferences/<int:id>')
def conference(id):
    conference = Conference.query.filter_by(id=id).first_or_404()
    return render_template('ncaa/conference.html', title=conference.nickname, conference=conference)
    
@bp.route('/add_conference', methods=['GET', 'POST'])
@login_required
def add_conference():
    if not current_user.admin:
        abort(403)
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
        return redirect(url_for('ncaa.conferences', id=conference.id))
    return render_template('ncaa/add_conference.html', title='Add Conference', form=form)

@bp.route('/edit_conference/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_conference(id):
    if not current_user.admin:
        abort(403)
    conference = Conference.query.filter_by(id=id).first_or_404()
    form = EditConferenceForm(conference)
    if form.validate_on_submit():
        conference.name = form.name.data
        conference.nickname = form.nickname.data
        conference.hq = form.hq.data
        conference.logo = form.logo.data
        conference.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('ncaa.edit_conference', id=id))
    elif request.method == 'GET':
        form.name.data = conference.name
        form.nickname.data = conference.nickname
        form.hq.data = conference.hq
        form.logo.data = conference.logo
        form.about.data = conference.about
    return render_template('ncaa/edit_conference.html',
        title=f'Edit: {conference.nickname}', form=form)


@bp.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('ncaa/teams.html', title='Teams', teams=teams)

@bp.route('/team/<int:id>')
@bp.route('/teams/<int:id>')
def team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    return render_template('ncaa/team.html', title=team.abbr, team=team)

@bp.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    if not current_user.admin:
        abort(403)
    form = AddOrEditTeamForm()
    if form.validate_on_submit():
        team = Team(
                school=form.school.data,
                mascot=form.mascot.data,
                abbr=form.abbr.data,
                logo=form.logo.data,
                conference_id=form.conference_id.data,
                about=form.about.data
            )
        db.session.add(team)
        db.session.commit()
        flash(f'Team added.')
        return redirect(url_for('ncaa.teams', id=team.id))
    return render_template('ncaa/add_team.html', title='Add Team', form=form)

@bp.route('/edit_team', methods=['GET', 'POST'])
@login_required
def edit_team():
    flash('that page is not yet implemented')
    return redirect(url_for('main.index'))
