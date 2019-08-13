CREATE TABLE citizen
(
    import_id   UUID         NOT NULL,
    citizen_id  INTEGER      NOT NULL,
    town        VARCHAR(100) NOT NULL,
    street      VARCHAR(100) NOT NULL,
    building    VARCHAR(100) NOT NULL,
    appartement INTEGER      NOT NULL,
    name        VARCHAR(100) NOT NULL,
    birth_date  DATE         NOT NULL,
    gender      VARCHAR(20)  NOT NULL,
    relatives   INTEGER[],
    PRIMARY KEY (import_id, citizen_id)
);

CREATE TABLE relation
(
    citizen_import_id UUID    NOT NULL,
    citizen1_id       INTEGER NOT NULL,
    citizen2_id       INTEGER NOT NULL,
    FOREIGN KEY (citizen_import_id, citizen1_id) REFERENCES citizen (import_id, citizen_id),
    FOREIGN KEY (citizen_import_id, citizen2_id) REFERENCES citizen (import_id, citizen_id)
);

DROP TABLE relation, citizen;

SELECT *
FROM citizen;

SELECT *
FROM relation;

SELECT citizen_id, town
FROM citizen
WHERE import_id = 1;

DELETE
FROM citizen
WHERE citizen_id = 2;

DELETE
FROM citizen
WHERE import_id = 123;

INSERT INTO citizen (import_id, citizen_id, town, street, building, appartement, name, birth_date, gender,
                     relatives)
VALUES ('77482648-bde7-11e9-9cb5-2a2ae2dbcce4', 1, 'Moscow', 'Lev Tolstoy', '16', 7, 'Ivan Ivanov', '1994-08-26',
        'male', ARRAY [2, 3, 4]);

INSERT INTO citizen (import_id, citizen_id, town, street, building, appartement, name, birth_date, gender,
                     relatives)
VALUES ('774828dc-bde7-11e9-9cb5-2a2ae2dbcce4', 1, 'Moscow', 'Lev Tolstoy', '16', 7, 'Yanis Urbis', '1994-08-26',
        'male', ARRAY [3, 4]);