CREATE TABLE COMPANY
(
    ID      INT PRIMARY KEY NOT NULL,
    NAME    TEXT            NOT NULL,
    AGE     INT             NOT NULL,
    ADDRESS CHAR(50),
    SALARY  REAL
);

SELECT *
FROM COMPANY;

create type gender as enum ('male', 'female');

CREATE TABLE citizen
(
    id          SERIAL PRIMARY KEY NOT NULL,
    town        VARCHAR(100)       NOT NULL,
    street      VARCHAR(100)       NOT NULL,
    building    VARCHAR(100)       NOT NULL,
    appartement INTEGER            NOT NULL,
    name        VARCHAR(100)       NOT NULL,
    birthday    DATE               NOT NULL,
    city        VARCHAR(100)       NOT NULL,
    gender      VARCHAR(20)        NOT NULL,
    relatives   INTEGER[]
);

CREATE TABLE relation
(
    citizen1_id SERIAL REFERENCES citizen (id),
    citizen2_id SERIAL REFERENCES citizen (id)
);

SELECT *
FROM users;

INSERT INTO users (name, birthday, city)
VALUES ('urbis', '1994-08-26', 'ivanovo'),
       ('ksusha', '1996-05-04', 'yaroslavl'),
       ('svetlana', '1967-04-23', 'ivanovo'),
       ('algis', '1972-04-18', 'ivanovo'),
       ('lesha', '1992-08-25', 'ivanovo');

INSERT INTO users (name, birthday, city)
VALUES ('yanis1', '1994-08-26', 'ivanovo'),
       ('urbis1', '1994-08-26', 'ivanovo'),
       ('ksusha1', '1996-05-04', 'yaroslavl'),
       ('svetlana1', '1967-04-23', 'ivanovo'),
       ('algis1', '1972-04-18', 'ivanovo'),
       ('lesha1', '1992-08-25', 'ivanovo');

CREATE TABLE relatives
(
    id1 SERIAL REFERENCES users (id),
    id2 SERIAL REFERENCES users (id)
);

INSERT INTO relatives
VALUES (1, 3),
       (1, 4),
       (1, 6);

INSERT INTO relatives
VALUES (1, 5);

INSERT INTO relatives
VALUES (7, 9),
       (7, 10),
       (7, 11),
       (7, 12);

SELECT *
FROM relatives;

/* --------------------------------------------------- */

DELETE
FROM relatives
WHERE relatives.id1 = 1;

/* --------------------------------------------------- */

SELECT users.name, u.name, u.birthday
FROM users
         INNER JOIN relatives r on users.id = r.id1
         INNER JOIN users u on u.id = r.id2;

SELECT EXTRACT(YEAR FROM u.birthday) as mon, users.name, COUNT(u.name)
FROM users
         INNER JOIN relatives r on users.id = r.id1
         INNER JOIN users u on u.id = r.id2
GROUP BY mon, users.name
ORDER BY mon;

/* --------------------------------------------------- */

SELECT users.name, EXTRACT(YEAR FROM AGE(users.birthday))
FROM users;

SELECT users.city, users.name, EXTRACT(YEAR FROM AGE(users.birthday)) as age
FROM users
ORDER BY users.city, age;

SELECT DISTINCT city,
                PERCENTILE_CONT(0.5) WITHIN
                    GROUP (ORDER BY EXTRACT(YEAR FROM AGE(users.birthday)) asc)   as p50,
                PERCENTILE_CONT(0.75) WITHIN
                    GROUP ( ORDER BY EXTRACT(YEAR FROM AGE(users.birthday)) asc ) as p75,
                PERCENTILE_CONT(0.99) WITHIN
                    GROUP ( ORDER BY EXTRACT(YEAR FROM AGE(users.birthday)) asc ) as p99
FROM users
GROUP BY city