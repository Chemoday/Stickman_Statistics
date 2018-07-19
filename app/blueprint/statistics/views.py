from app.utils.validators import *
from models.statistics.models import *
from . import statistics


GAMEROUNDS_CACHE = []
GAMEROUNDS_CACHE_LIMIT = 8

@statistics.route('/test', methods=['POST'])
def test():
    print("in func")
    data = request.get_data()
    print(data)
    print("________________")
    json = request.get_json()
    print(json)
    return jsonify({"result": "ok"})



#TODO ATT HANDLER FOR
@statistics.route('/round/save', methods=['POST'])
def save_round_stat():
    global GAMEROUNDS_CACHE
    json = request.get_json(force=True)
    try:

            #mode = validate_string_json_data('mode')
            #TODO add validators
            round = {'mode': json['mode'],
                         'type': json['type'],
                         'map': json['map'],
                         'total_players': json['total_players'],
                         'total_kills': json['total_kills'],
                         'total_deaths': json['total_deaths'],
                         'most_kills': json['most_kills'],
                         'most_deaths': json['most_deaths']}

    except Exception as e:
        return jsonify({
            'result': 'Error',
            'reason': e
        })

    if len(GAMEROUNDS_CACHE) >= GAMEROUNDS_CACHE_LIMIT:
        GameRounds.insert_gamerounds(GAMEROUNDS_CACHE)
        GAMEROUNDS_CACHE = []
    else:
        GAMEROUNDS_CACHE.append(round)


    #TODO CHECK PERFORMANCE AND MAKE BULK INSERT IF NEEDED, STORE IN CACHE AND LOAD AFTER 100 rounds
    return jsonify({
        'result': 'OK'
    })