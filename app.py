import random

from flask import Flask, jsonify, request

from db import insert_citizens, select_citizens_by_import_id

app = Flask(__name__)


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


@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_citizens(import_id):
    citizens = select_citizens_by_import_id(str(import_id))

    res = {'data': citizens}

    return jsonify(res), 200


# # TODO: should UUID:import_id?
# @app.route('/imports/<string:import_id>/citizens/<string:citizen_id>', methods=['PATCH'])
# def update_citizen(import_id, citizen_id):
#     partial_citizen = request.get_json()
#
#     citizen = db.update_citizen(import_id, citizen_id, partial_citizen)
#
#     res = {'data': citizen}
#
#     return jsonify(res), 200


if __name__ == '__main__':
    app.run(debug=True)
