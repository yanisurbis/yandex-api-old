import collections
import random

from flask import Flask, jsonify, request

from db import insert_citizens, select_citizens_by_import_id, select_presents_amount_by_month, select_citizen, \
    update_citizen, delete_relation, insert_relation, select_stats_by_town
from utils import diff

app = Flask(__name__)


# TODO: try validation with https://pypi.org/project/flask-expects-json/

@app.route('/imports', methods=['POST'])
def import_citizens():
    citizens = request.get_json()['citizens']
    # import_id = str(uuid.uuid1())
    import_id = random.randint(1, 2147483647)
    insert_citizens(import_id, citizens)

    res = {'data': {
        "import_id": import_id
    }}

    return jsonify(res), 201


# TODO: check if relatives exists

@app.route('/imports/<int:import_id>/citizens/<int:citizen_id>', methods=['PATCH'])
def patch_citizen(import_id, citizen_id):
    citizen_patch = request.get_json()['data']
    citizen = select_citizen(import_id, citizen_id)
    citizen_copy = citizen.copy()

    # update citizen
    for key in citizen.keys():
        if citizen_patch[key]:
            citizen[key] = citizen_patch[key]

    update_citizen(import_id, citizen)

    if citizen_patch['relatives']:
        past_relatives_ids = diff(citizen_copy['relatives'], citizen_patch['relatives'])
        future_relatives_ids = diff(citizen_patch['relatives'], citizen_copy['relatives'])
        # update past relatives
        for relative_id in past_relatives_ids:
            relative = select_citizen(import_id, relative_id)
            relative["relatives"].remove(citizen_id)
            update_citizen(import_id, relative)

        # update future relatives
        for relative_id in future_relatives_ids:
            relative = select_citizen(import_id, relative_id)
            relative["relatives"].append(citizen_id)
            update_citizen(import_id, relative)

        for relative_id in past_relatives_ids:
            delete_relation(import_id, relative_id, citizen_id)
            delete_relation(import_id, citizen_id, relative_id)

        for relative_id in future_relatives_ids:
            insert_relation(import_id, relative_id, citizen_id)
            insert_relation(import_id, citizen_id, relative_id)

    res = {'data': citizen}

    return jsonify(res), 200


@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_citizens(import_id):
    citizens = select_citizens_by_import_id(import_id)

    res = {'data': citizens}

    return jsonify(res), 200


@app.route('/imports/<int:import_id>/citizens/birthdays', methods=['GET'])
def get_citizens_birthdays(import_id):
    presents_amount_by_month = select_presents_amount_by_month(import_id)

    months = collections.defaultdict(list)
    for row in presents_amount_by_month:
        months[row["mon"]].append({
            "citizen_id": row["citizen_id"],
            "name": row["name"],
            "presents": row["presents"]
        })
    year_resume = {}
    for i in range(1, 13):
        year_resume[i] = months[i]

    res = {'data': year_resume}

    return jsonify(res), 200


@app.route('/imports/<int:import_id>/towns/stat/percentile/age', methods=['GET'])
def get_towns_stats(import_id):
    stat_rows = select_stats_by_town(import_id)

    res = {'data': stat_rows}
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(debug=True)
