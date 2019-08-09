import psycopg2
from psycopg2.extras import RealDictCursor

DSL = "user=yanis password=04051996 host=localhost port=5432 dbname=template3"

conn = psycopg2.connect(DSL)


def select_citizens_by_import_id(import_id):
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(
            """SELECT citizen_id, town, street, building, appartement, name, birth_date, gender, relatives
            FROM citizen WHERE import_id = (%s);""",
            [import_id])
        return curs.fetchall()


def insert_citizens(import_id, citizens):
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        for c in citizens:
            curs.execute("""INSERT INTO citizen 
                               (import_id, citizen_id, town, street, building,
                               appartement, name, birth_date, gender, relatives)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                         [import_id, c["citizen_id"], c["town"], c["street"], c["building"], c["appartement"],
                          c["name"], c["birth_date"], c["gender"], c["relatives"]])


sample_citizens = [
    {
        "appartement": 7,
        "birth_date": "Fri, 26 Aug 1994 00:00:00 GMT",
        "building": "16",
        "citizen_id": 1,
        "gender": "male",
        "name": "Jack Sparrow",
        "relatives": [
            2,
            3,
            4
        ],
        "street": "Lev Tolstoy",
        "town": "Moscow"
    },
    {
        "appartement": 7,
        "birth_date": "Fri, 26 Aug 1994 00:00:00 GMT",
        "building": "16",
        "citizen_id": 1,
        "gender": "male",
        "name": "Ula Ula",
        "relatives": [
            3,
            4
        ],
        "street": "Lev Tolstoy",
        "town": "Moscow"
    }
]

# insert_citizens(123, sample_citizens)
select_citizens_by_import_id(123)
