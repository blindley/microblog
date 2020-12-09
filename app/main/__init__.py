import requests
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User, Comment

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    response = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings')
    rankings = None
    week_number = None
    if response.status_code == 200:
        j = response.json()
        week_number = j['latestWeek']['value']
        for r in j['rankings']:
            if r['shortName'] == 'AP Poll':
                rankings = r['ranks']
                break
    return render_template('index.html', title='Home', rankings=rankings, week_number=week_number)


@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if not (current_user.admin or current_user.id == comment.user_id):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    redirect_page = request.args.get('pageref') or url_for('main.index')
    flash('The comment has been deleted')
    return redirect(redirect_page)
