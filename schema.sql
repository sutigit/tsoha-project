
-- create tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    image TEXT
);

CREATE TABLE gamevotes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games
);


CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    message TEXT,
);

CREATE TABLE messagelikes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages
);



-- insert mockup games
INSERT INTO games (name, description, image)
VALUES (
    'The Legend of Zelda: Breath of the Wild',
    'The Legend of Zelda: Breath of the Wild is an action-adventure game developed and published by Nintendo, released for the Nintendo Switch and Wii U consoles on March 3, 2017.',
    'https://upload.wikimedia.org/wikipedia/en/c/c6/The_Legend_of_Zelda_Breath_of_the_Wild.jpg'
);

INSERT INTO games (name, description, image)
VALUES (
    'Super Mario Odyssey',
    'Super Mario Odyssey is a platform game published by Nintendo for the Nintendo Switch on October 27, 2017.',
    'https://upload.wikimedia.org/wikipedia/en/8/8d/Super_Mario_Odyssey.jpg'
);

INSERT INTO games (name, description, image)
VALUES (
    'Mario Kart 8 Deluxe',
    'Mario Kart 8 Deluxe is a racing game for the Nintendo Switch, and the first Mario game overall for the console. It is a port in the Mario Kart series, being a port of Mario Kart 8 from the Wii U.',
    'https://upload.wikimedia.org/wikipedia/fi/d/dd/Mario_Kart_8_Deluxe.jpg'
);

INSERT INTO games (name, description, image)
VALUES (
    'Super Smash Bros. Ultimate',
    'Super Smash Bros. Ultimate is a 2018 crossover fighting game developed by Bandai Namco Studios and Sora Ltd. and published by Nintendo for the Nintendo Switch.',
    'https://upload.wikimedia.org/wikipedia/en/5/50/Super_Smash_Bros._Ultimate.jpg'
);

INSERT INTO games (name, description, image)
VALUES (
    'The Legend of Zelda: Tears of the Kingdom',
    'Tears of the Kingdom is a 2018 crossover fighting game developed by Bandai Namco Studios and Sora Ltd. and published by Nintendo for the Nintendo Switch.',
    'https://upload.wikimedia.org/wikipedia/pt/2/25/Zelda_TotK_capa.jpg'
);

