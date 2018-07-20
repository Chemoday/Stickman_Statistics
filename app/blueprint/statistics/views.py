from app.utils.validators import *
from models.statistics.models import *
from . import statistics


GAMEROUNDS_STRUCT_CACHE = []
SETTINGS_JOYSTICK_CACHE = []
CACHE_SIZE = 20

@statistics.route('/test', methods=['POST'])
def test():
    print("in func")
    data = request.get_data()
    print(data)
    print("________________")
    json = request.get_json()
    print(json)
    return jsonify({"result": "ok"})



@statistics.route('/round/save', methods=['POST'])
def save_round_stat():
    global GAMEROUNDS_STRUCT_CACHE
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
            'reason': 'Missing data, check attributes'
        })

    if len(GAMEROUNDS_STRUCT_CACHE) >= CACHE_SIZE:
        GameRounds.insert_bulk_data(data_to_insert=GAMEROUNDS_STRUCT_CACHE)
        GAMEROUNDS_STRUCT_CACHE = [] #clearing cache
    else:
        GAMEROUNDS_STRUCT_CACHE.append(round)

    return jsonify({
        'result': 'OK'
    })


@statistics.route('/settings/joystick/save', methods=['POST'])
def save_settings_joistick():
    global SETTINGS_JOYSTICK_CACHE
    json = request.get_json(force=True)

    pass


























