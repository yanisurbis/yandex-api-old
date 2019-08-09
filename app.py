from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://yanis:04051996@localhost/template3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __init__(self, name, birthday, city):
        self.city = city
        self.birthday = birthday
        self.name = name


class BoxSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'birthday', 'city')
        model = Box


box_schema = BoxSchema(strict=True)
boxes_schema = BoxSchema(many=True, strict=True)


@app.route('/box', methods=['POST'])
def add_box():
    name = request.json['name']
    birthday = request.json['birthday']
    city = request.json['city']

    new_box = Box(name, birthday, city)

    db.session.add(new_box)
    db.session.commit()

    return box_schema.jsonify(new_box)


if __name__ == '__main__':
    app.run(debug=True)
