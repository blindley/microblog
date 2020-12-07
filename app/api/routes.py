from flask import jsonify

from app.api import bp
from app.models import Conference, Team

@bp.route('/api')
def api():
    conferences = Conference.query.order_by(Conference.name).all()
    teams = Team.query.order_by(Team.school).all()
    data = {
        'conferences': [
            {
                'name': c.name, 'nickname': c.nickname, 'hq': c.hq, 'logo': c.logo,
                'teams': [t.school for t in c.teams.order_by(Team.school).all() ]
            }
            for c in conferences
        ],
        'teams': [
            {
                'school': t.school, 'mascot': t.mascot, 'abbreviation': t.abbr, 'logo': t.logo,
                'conference': t.conference.name
            }
            for t in teams
        ]
    }

    return jsonify(data)

