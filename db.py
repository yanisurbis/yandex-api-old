import psycopg2
from psycopg2.extras import RealDictCursor

DSL = "user=yanis password=04051996 host=localhost port=5432 dbname=template3"


# TODO: cursor factory, speed?
# TODO: error handling for cursor
# TODO: envinronments test, dev, production
# TODO: opening and closing connection

def select_citizens_by_import_id(import_id):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """SELECT citizen_id, town, street, building, appartement, name, birth_date, gender, relatives
                FROM citizen WHERE import_id = (%s);""",
                [import_id])
            return curs.fetchall()


def select_citizen(import_id, citizen_id):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """SELECT citizen_id, town, street, building, appartement, name, birth_date, gender, relatives
                FROM citizen WHERE import_id = (%s) and citizen_id = (%s);""",
                [import_id, citizen_id])
            return curs.fetchone()


def update_citizen(import_id, citizen):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """UPDATE citizen
                    SET town = (%s),
                        street = (%s),
                        building = (%s),
                        appartement = (%s),
                        name = (%s),
                        birth_date = (%s),
                        gender = (%s),
                        relatives = (%s)
                    WHERE import_id = (%s) AND citizen_id = (%s)""",
                [citizen["town"], citizen["street"], citizen["building"], citizen["appartement"],
                 citizen["name"], citizen["birth_date"], citizen["gender"], citizen["relatives"], import_id,
                 citizen["citizen_id"]]
            )


def delete_relation(import_id, citizen1_id, citizen2_id):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """DELETE from relation
                   WHERE citizen_import_id = (%s) AND citizen1_id = (%s) AND citizen2_id = (%s)""",
                [import_id, citizen1_id, citizen2_id]
            )


def insert_relation(import_id, citizen1_id, citizen2_id):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """INSERT INTO relation 
                   (citizen_import_id, citizen1_id, citizen2_id)
                   VALUES (%s,%s,%s);""",
                [import_id, citizen1_id, citizen2_id]
            )


# TODO: error handling for cursor
def insert_citizens(import_id, citizens):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            for c in citizens:
                curs.execute("""INSERT INTO citizen 
                                       (import_id, citizen_id, town, street, building,
                                       appartement, name, birth_date, gender, relatives)
                                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                             [import_id, c["citizen_id"], c["town"], c["street"], c["building"], c["appartement"],
                              c["name"], c["birth_date"], c["gender"], c["relatives"]])

            for c in citizens:
                for relative_id in c["relatives"]:
                    curs.execute("""INSERT INTO relation 
                                       (citizen_import_id, citizen1_id, citizen2_id)
                                       VALUES (%s,%s,%s);""",
                                 [import_id, c["citizen_id"], relative_id])


def select_presents_amount_by_month(import_id):
    with psycopg2.connect(DSL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                """WITH imported_citizens AS (
                        SELECT *
                        FROM citizen
                        WHERE import_id = (%s)
                    )
                    
                    SELECT EXTRACT(MON FROM c.birth_date) as mon,
                            imported_citizens.name,
                            imported_citizens.citizen_id,
                            COUNT(c.name) as presents
                    FROM imported_citizens
                             INNER JOIN relation r on imported_citizens.import_id = r.citizen_import_id AND 
                                                        imported_citizens.citizen_id = r.citizen1_id                  
                             INNER JOIN imported_citizens c on c.citizen_id = r.citizen2_id
                    GROUP BY mon, imported_citizens.name, imported_citizens.citizen_id
                    ORDER BY mon;""",
                [import_id])

            return curs.fetchall()


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
# select_citizens_by_import_id(123)
# print(select_citizen(1473046223, 3))
# update_citizen(1473046223, {
#     "appartement": 7,
#     "birth_date": "Fri, 26 Aug 1994 00:00:00 GMT",
#     "building": "16",
#     "citizen_id": 1,
#     "gender": "male",
#     "name": "Jack Sparrow",
#     "relatives": [
#         2,
#         3,
#         4
#     ],
#     "street": "Lev Tolstoy",
#     "town": "Moscow"
# })
