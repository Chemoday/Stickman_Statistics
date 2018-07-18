from app.utils.validators import *
from models.statistics.models import *
from . import statistics






#TODO ATT HANDLER FOR
@statistics.route('/round/save', methods=['GET', 'POST'])
def save_round_stat():
    try:

            roundDict = {'mode': request.json.get('mode'),
                         'type': request.json.get('type'),
                         'map': request.json.get('map'),
                         'total_players': request.json.get('total_players'),
                         'total_kills': request.json.get('total_kills'),
                         'total_deaths': request.json.get('total_deaths'),
                         'most_kills': request.json.get('most_kills'),
                         'most_deaths': request.json.get('most_deaths')}
            GameRounds.insert(**roundDict).execute()

    except Exception as e:
        return jsonify({
            'result': 'Error',
            'reason': e
        })



    #TODO CHECK PERFORMANCE AND MAKE BULK INSERT IF NEEDED, STORE IN CACHE AND LOAD AFTER 100 rounds
    return jsonify({
        'result': 'OK'
    })