from flask import flash, url_for, redirect, render_template, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Conference, Team, Post
from app.ncaa.forms import AddConferenceForm, EditConferenceForm, AddOrEditTeamForm
from app.ncaa import bp
from app.main.forms import PostForm


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

@bp.route('/team/<int:id>', methods=['GET', 'POST'])
@bp.route('/teams/<int:id>', methods=['GET', 'POST'])
@login_required
def team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, team_page=team)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('ncaa.team', id=id))
    return render_template('ncaa/team.html', title=team.abbr, team=team, form=form)

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

@bp.route('/edit_team/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    if not current_user.admin:
        abort(403)
    team = Team.query.filter_by(id=id).first_or_404()
    form = AddOrEditTeamForm(team)
    if form.validate_on_submit():
        team.school = form.school.data
        team.mascot = form.mascot.data
        team.abbr = form.abbr.data
        team.logo = form.logo.data
        team.conference_id = form.conference_id.data
        team.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('ncaa.edit_team', id=id))
    elif request.method == 'GET':
        form.school.data = team.school
        form.mascot.data = team.mascot
        form.abbr.data = team.abbr
        form.logo.data = team.logo
        form.conference_id.data = team.conference_id
        form.about.data = team.about
    return render_template('ncaa/edit_team.html',
        title=f'Edit: {team.school}', form=form)


@bp.route('/follow_team/<int:id>')
@login_required
def follow_team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    current_user.teams.append(team)
    db.session.commit()
    flash(f'You are now following {team.abbr}!', 'success')
    return redirect(url_for('ncaa.team', id=id))

@bp.route('/unfollow_team/<int:id>')
@login_required
def unfollow_team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    current_user.teams.remove(team)
    db.session.commit()
    flash(f'You are no longer following {team.abbr}.', 'success')
    return redirect(url_for('ncaa.team', id=id))
