CREATE EXTENSION "uuid-ossp";

CREATE TABLE users ( 
    userid uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
    username text UNIQUE NOT NULL,
    password text NOT NULL,
    email text UNIQUE NOT NULL,
    admin boolean DEFAULT FALSE,
    active boolean DEFAULT FALSE,
    email_confirmed boolean DEFAULT FALSE,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    role text DEFAULT '',
    bio text DEFAULT '',
    neighborhood uuid REFERENCES neighborhood(hoodid)
);

CREATE TABLE profile_images (
    userid uuid REFERENCES users(userid) ON DELETE CASCADE,
    imageid uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
    date timestamp DEFAULT CURRENT_TIMESTAMP,
    imagedata bytea NOT NULL,
    mimetype text
);

CREATE TABLE cover_image (
    userid uuid REFERENCES users(userid) ON DELETE CASCADE,
    imageid uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
    date timestamp DEFAULT CURRENT_TIMESTAMP,
    imagedata bytea NOT NULL,
    mimetype text
);

CREATE table neighborhood (
	hoodid uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
	name text
);

CREATE table message (
    id uuid UNIQUE PRIMARY KEY DEFAULT uuid_generate_v1(),
    subject uuid REFERENCES users(userid) ON DELETE SET NULL,
    author uuid REFERENCES users(userid) ON DELETE SET NULL,
    created timestamp DEFAULT CURRENT_TIMESTAMP,
    message text
);