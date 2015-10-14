CREATE EXTENSION "uuid-ossp";

CREATE TABLE users ( 
    userid uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
    username text UNIQUE NOT NULL,
    password text NOT NULL,
    email text UNIQUE NOT NULL,
    admin boolean DEFAULT FALSE,
    active boolean DEFAULT FALSE,
    email_confirmed boolean DEFAULT FALSE,
    created timestamp DEFAULT CURRENT_TIMESTAMP
);