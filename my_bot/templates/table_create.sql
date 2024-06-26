CREATE TABLE TelegramUsers (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(25),
    username VARCHAR(25),
    firstname VARCHAR(25),
    adress VARCHAR(255)
);

CREATE TABLE Mailing (
    id SERIAL PRIMARY KEY,
    username_tg INTEGER REFERENCES TelegramUsers(id),
    date_send VARCHAR(15),
    error_text VARCHAR(255)
);
