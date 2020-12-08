from flask import Blueprint, json, jsonify
from app.models import Conference, Team, Comment, User


bp = Blueprint('api', __name__)

def _team_as_object(team):
    return {
        'id': team.id,
        'school': team.school,
        'mascot': team.mascot,
        'abbreviation': team.abbr,
        'logo': team.logo,
        'about': team.about,
        'conference': team.conference.name
    }

def _comment_as_object(comment):
    return {
        'id': comment.id,
        'author': comment.author.username,
        'body': comment.body,
        'team': comment.team.abbr,
        'timestamp': comment.timestamp
    }

def _user_as_object(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'about_me': user.about_me
    }

def _conference_as_object(conference):
    return {
        'id': conference.id,
        'name': conference.name,
        'nickname': conference.nickname,
        'logo': conference.logo,
        'hq': conference.hq,
        'about': conference.about
    }


@bp.route('/teams')
def teams():
    teams = Team.query.order_by(Team.school).all()
    data = [_team_as_object(team) for team in teams]
    return jsonify(data)

@bp.route('/teams/<int:id>')
def team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    data = _team_as_object(team)
    return jsonify(data)

@bp.route('/comments')
def comments():
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    data = [_comment_as_object(comment) for comment in comments]
    return jsonify(data)

@bp.route('/comments/team/<int:id>')
def team_comments(id):
    comments = Comment.query.filter_by(team_id=id).order_by(Comment.timestamp.desc()).all()
    data = [_comment_as_object(comment) for comment in comments]
    return jsonify(data)

@bp.route('/comments/user/<int:id>')
def user_comments(id):
    comments = Comment.query.filter_by(user_id=id).order_by(Comment.timestamp.desc()).all()
    data = [_comment_as_object(comment) for comment in comments]
    return jsonify(data)

@bp.route('/users')
def users():
    users = User.query.order_by(User.username).all()
    data = [_user_as_object(user) for user in users]
    return jsonify(data)

@bp.route('/users/followers/<int:team_id>')
def team_followers(team_id):
    team = Team.query.filter_by(id=team_id).first_or_404()
    users = team.fans.all()
    data = [_user_as_object(user) for user in users]
    return jsonify(data)

@bp.route('/conferences')
def conferences():
    conferences = Conference.query.order_by(Conference.name).all()
    data = [_conference_as_object(conf) for conf in conferences]
    return jsonify(data)

@bp.route('/teams/conference/<int:id>')
def conference_teams(id):
    teams = Team.query.filter_by(conference_id=id).order_by(Team.school).all()
    data = [_team_as_object(team) for team in teams]
    return jsonify(data)

