from app.utils.validators import *
from models.statistics.models import *
from . import statistics


GAMEROUNDS_STRUCT_CACHE = []
SETTINGS_JOYSTICK_CACHE = []
TUTORIAL_FLOW_CACHE = []
CACHE_SIZE = 5

@statistics.route('/test', methods=['POST'])
def test():
    print("in func")
    data = request.get_data()
    print(data)
    print("________________")
    json = request.get_json()
    print(json)
    return jsonify({"result": "OK"})



@statistics.route('/round/save', methods=['POST'])
def save_round_stat():
    global GAMEROUNDS_STRUCT_CACHE
    json = request.get_json(force=True)
    try:

            #mode = validate_string_json_data('mode')
            #TODO add validators
            round_struct = {'mode': json['mode'],
                         'type': json['type'],
                         'map': json['map'],
                         'total_players': json['total_players'],
                         'total_kills': json['total_kills'],
                         'total_deaths': json['total_deaths'],
                         'most_kills': json['most_kills'],
                         'most_deaths': json['most_deaths']}

    except Exception as e:
        return jsonify({
            'result': 'ERROR',
            'reason': 'Missing data, check attributes'
        })

    if len(GAMEROUNDS_STRUCT_CACHE) >= CACHE_SIZE:
        GameRounds.insert_bulk_data(data_to_insert=GAMEROUNDS_STRUCT_CACHE)
        GAMEROUNDS_STRUCT_CACHE = [] #clearing cache
    else:
        GAMEROUNDS_STRUCT_CACHE.append(round_struct)

    return jsonify({
        'result': 'OK'
    })


@statistics.route('/settings/joystick/save', methods=['POST'])
def save_settings_joistick():
    global SETTINGS_JOYSTICK_CACHE
    json = request.get_json(force=True)

    try:
        user_id = json['user_id']
        controls_type = json['controls_type']

    except Exception as e:
        return jsonify({
            'result': 'ERROR',
            'reason': 'Missing data, check attributes'
        })


    if SettingsJoystick.select().where(SettingsJoystick.user_id == user_id).exists():
        settings = SettingsJoystick.get(SettingsJoystick.user_id == user_id)
        if settings.controls_type != controls_type:
            #complex query for update, just to make it fast - atomic
            SettingsJoystick.update({SettingsJoystick.controls_type: controls_type,
                                     SettingsJoystick.changed: True}).where(
                SettingsJoystick.user_id == user_id).execute()
            print('updated')
    else:
        SettingsJoystick.insert(user_id=user_id, controls_type=controls_type).execute()


    return jsonify({
        'result': 'OK'
    })

@statistics.route('/tutorial-flow/save', methods=['POST'])
def save_tutorial_flow():
    global TUTORIAL_FLOW_CACHE
    json = request.get_json(force=True)

    try:
        tutorial = {
            'phase': json['phase'],
            'completion_time': json['completion_time'],
            'deaths': json['deaths'],
            'grenade_used': json['grenade_used'],
            'weapon_changed': json['weapon_changed'],
            'crouch_used': json['crouch_used']
        }

    except Exception as e:
        print(e)
        return jsonify({
            'result': 'ERROR',
            'reason': 'Missing data, check attributes',
            'exception': e
        })

    if len(TUTORIAL_FLOW_CACHE) >= CACHE_SIZE:
        TutorialFlow.insert_bulk_data(data_to_insert=TUTORIAL_FLOW_CACHE)
        TUTORIAL_FLOW_CACHE = [] #clearing cache
    else:
        TUTORIAL_FLOW_CACHE.append(tutorial)

    return jsonify({
        'result': 'OK'
    })




#TODO resolve this shit, rewrite
def check_cache_condition(cache_type, model):
    global GAMEROUNDS_STRUCT_CACHE, SETTINGS_JOYSTICK_CACHE

    if len(GAMEROUNDS_STRUCT_CACHE) >= CACHE_SIZE:
        model.insert_bulk_data(data_to_insert=GAMEROUNDS_STRUCT_CACHE)
        cache_type = [] #clearing cache
    else:
        cache_type.append(round)






















