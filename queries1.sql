CREATE TABLE citizen
(
    id          SERIAL PRIMARY KEY NOT NULL,
    import_id   BIGINT             NOT NULL,
    citizen_id  INTEGER            NOT NULL,
    town        VARCHAR(100)       NOT NULL,
    street      VARCHAR(100)       NOT NULL,
    building    VARCHAR(100)       NOT NULL,
    appartement INTEGER            NOT NULL,
    name        VARCHAR(100)       NOT NULL,
    birth_date  DATE               NOT NULL,
    gender      VARCHAR(20)        NOT NULL,
    relatives   INTEGER[]
);

CREATE TABLE relation
(
    citizen1_id SERIAL REFERENCES citizen (id),
    citizen2_id SERIAL REFERENCES citizen (id)
);

DROP TABLE relation, citizen;

SELECT *
FROM citizen;

SELECT citizen_id, town
FROM citizen
WHERE import_id = 1;

DELETE
FROM citizen
WHERE id = 2;

DELETE
FROM citizen
WHERE import_id = 123;

INSERT INTO citizen (import_id, citizen_id, town, street, building, appartement, name, birth_date, gender,
                     relatives)
VALUES (1, 1, 'Moscow', 'Lev Tolstoy', '16', 7, 'Ivan Ivanov', '1994-08-26', 'male', ARRAY [2, 3, 4]);

INSERT INTO citizen (import_id, citizen_id, town, street, building, appartement, name, birth_date, gender,
                     relatives)
VALUES (1, 1, 'Moscow', 'Lev Tolstoy', '16', 7, 'Yanis Urbis', '1994-08-26', 'male', ARRAY [3, 4]);