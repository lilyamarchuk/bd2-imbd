CREATE DATABASE IF NOT EXISTS imdb_lab
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE imdb_lab;

DROP TABLE IF EXISTS box_office;
DROP TABLE IF EXISTS trivia;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS movie_cast;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS movie_countries;
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS genres;

CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
) ENGINE = INNODB;

CREATE TABLE countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code CHAR(2) NOT NULL UNIQUE
) ENGINE = INNODB;

CREATE TABLE persons (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    birth_date DATE,
    birth_place VARCHAR(150),
    biography TEXT
) ENGINE = INNODB;

CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255),
    release_year YEAR NOT NULL,
    duration_min INT,
    description TEXT,
    age_rating VARCHAR(10),
    INDEX idx_movies_year (release_year),
    INDEX idx_movies_title (title)
) ENGINE = INNODB;

CREATE TABLE movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE movie_countries (
    movie_id INT NOT NULL,
    country_id INT NOT NULL,
    PRIMARY KEY (movie_id, country_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
) ENGINE = INNODB;

CREATE TABLE movie_cast (
    cast_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    person_id INT NOT NULL,
    role_id INT NOT NULL,
    character_name VARCHAR(150),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES persons(person_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT,
    INDEX idx_cast_movie (movie_id),
    INDEX idx_cast_person (person_id)
) ENGINE = INNODB;

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    author_name VARCHAR(100) NOT NULL,
    review_text TEXT NOT NULL,
    review_date DATE NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    score DECIMAL(3,1) NOT NULL CHECK (score >= 0 AND score <= 10),
    rating_date DATE NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    INDEX idx_ratings_movie (movie_id),
    UNIQUE KEY uk_rating_user_movie (movie_id, user_name)
) ENGINE = INNODB;

CREATE TABLE trivia (
    trivia_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    fact_text TEXT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE box_office (
    box_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    country_id INT NOT NULL,
    amount_usd DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE,
    UNIQUE KEY uk_movie_country (movie_id, country_id)
) ENGINE = INNODB;

CREATE INDEX idx_persons_full_name ON persons (full_name);
CREATE INDEX idx_ratings_score ON ratings (score);
CREATE INDEX idx_reviews_date ON reviews (review_date);
CREATE INDEX idx_box_amount ON box_office (amount_usd);

INSERT INTO genres (genre_id, name) VALUES
 (1,'Action'),(2,'Drama'),(3,'Comedy'),(4,'Sci-Fi'),(5,'Thriller'),
 (6,'Horror'),(7,'Romance'),(8,'Adventure'),(9,'Fantasy'),(10,'Crime'),
 (11,'Biography'),(12,'History');

INSERT INTO countries (country_id, name, code) VALUES
 (1,'United States','US'),(2,'United Kingdom','GB'),(3,'France','FR'),
 (4,'Germany','DE'),(5,'Japan','JP'),(6,'Canada','CA'),
 (7,'Australia','AU'),(8,'Italy','IT'),(9,'Spain','ES'),
 (10,'South Korea','KR'),(11,'Ukraine','UA'),(12,'Ireland','IE');

INSERT INTO persons (person_id, full_name, birth_date, birth_place, biography) VALUES
 (1,'Leonardo DiCaprio','1974-11-11','Los Angeles, USA','American actor and producer'),
 (2,'Christopher Nolan','1970-07-30','London, UK','British-American film director'),
 (3,'Scarlett Johansson','1984-11-22','New York, USA','American actress'),
 (4,'Tom Hanks','1956-07-09','Concord, USA','American actor and filmmaker'),
 (5,'Quentin Tarantino','1963-03-27','Knoxville, USA','American film director and screenwriter'),
 (6,'Natalie Portman','1981-06-09','Jerusalem, Israel','Israeli-American actress'),
 (7,'Brad Pitt','1963-12-18','Shawnee, USA','American actor and producer'),
 (8,'Emma Stone','1988-11-06','Scottsdale, USA','American actress'),
 (9,'Keanu Reeves','1964-09-02','Beirut, Lebanon','Canadian actor'),
 (10,'Greta Gerwig','1983-08-04','Sacramento, USA','American actress and director'),
 (11,'Cillian Murphy','1976-05-25','Douglas, Cork, Ireland','Irish actor'),
 (12,'Timothée Chalamet','1995-12-27','New York, USA','American actor'),
 (13,'Margot Robbie','1990-07-02','Dalby, Australia','Australian actress and producer'),
 (14,'Song Kang-ho','1967-01-17','Gimhae, South Korea','South Korean actor'),
 (15,'Christian Bale','1974-01-30','Haverfordwest, UK','British actor');

INSERT INTO roles (role_id, role_name) VALUES
 (1,'Actor'),(2,'Director'),(3,'Writer'),(4,'Producer'),(5,'Cinematographer'),
 (6,'Composer'),(7,'Editor'),(8,'Production Designer'),(9,'Costume Designer'),(10,'Sound Designer');

INSERT INTO movies (movie_id, title, original_title, release_year, duration_min, description, age_rating) VALUES
 (1,'Inception','Inception',2010,148,'A thief who steals corporate secrets through dream-sharing technology','PG-13'),
 (2,'The Dark Knight','The Dark Knight',2008,152,'Batman faces the Joker in Gotham City','PG-13'),
 (3,'Pulp Fiction','Pulp Fiction',1994,154,'The lives of two mob hitmen, a boxer and others intertwine','R'),
 (4,'Interstellar','Interstellar',2014,169,'A team of explorers travel through a wormhole in space','PG-13'),
 (5,'La La Land','La La Land',2016,128,'A jazz pianist falls for an aspiring actress in Los Angeles','PG-13'),
 (6,'The Matrix','The Matrix',1999,136,'A computer hacker learns about the true nature of reality','R'),
 (7,'Forrest Gump','Forrest Gump',1994,142,'The life of a slow-witted but kind-hearted man','PG-13'),
 (8,'Fight Club','Fight Club',1999,139,'An office worker and a soap maker form an underground fight club','R'),
 (9,'Avengers: Endgame','Avengers: Endgame',2019,181,'The Avengers assemble once more to reverse Thanos actions','PG-13'),
 (10,'Parasite','Gisaengchung',2019,132,'A poor family schemes to become employed by a wealthy family','R'),
 (11,'Oppenheimer','Oppenheimer',2023,180,'The story of American scientist J. Robert Oppenheimer','R'),
 (12,'Dune: Part Two','Dune: Part Two',2024,166,'Paul Atreides unites with Chani and the Fremen','PG-13'),
 (13,'Tenet','Tenet',2020,150,'A secret agent learns to manipulate the flow of time','PG-13'),
 (14,'Barbie','Barbie',2023,114,'Barbie leaves Barbieland and discovers the real world','PG-13');

INSERT INTO movie_genres (movie_id, genre_id) VALUES
 (1,1),(1,4),(1,5),
 (2,1),(2,5),(2,10),
 (3,10),(3,2),
 (4,4),(4,2),(4,8),
 (5,7),(5,3),
 (6,1),(6,4),
 (7,2),(7,3),
 (8,2),(8,5),
 (9,1),(9,4),(9,8),
 (10,2),(10,5),(10,10),
 (11,2),(11,11),(11,12),
 (12,1),(12,4),(12,8),
 (13,1),(13,4),(13,5),
 (14,3),(14,8),(14,9);

INSERT INTO movie_countries (movie_id, country_id) VALUES
 (1,1),(1,2),
 (2,1),(2,2),
 (3,1),
 (4,1),(4,2),
 (5,1),
 (6,1),(6,7),
 (7,1),
 (8,1),(8,4),
 (9,1),
 (10,10),
 (11,1),(11,2),
 (12,1),(12,6),
 (13,1),(13,2),
 (14,1),(14,2);

INSERT INTO movie_cast (cast_id, movie_id, person_id, role_id, character_name) VALUES
 (1,1,1,1,'Dom Cobb'),
 (2,1,2,2,NULL),
 (3,1,2,3,NULL),
 (4,2,15,1,'Bruce Wayne / Batman'),
 (5,2,2,2,NULL),
 (6,3,5,2,NULL),
 (7,3,5,3,NULL),
 (8,4,2,2,NULL),
 (9,5,8,1,'Mia'),
 (10,6,9,1,'Neo'),
 (11,7,4,1,'Forrest Gump'),
 (12,8,7,1,'Tyler Durden'),
 (13,9,3,1,'Natasha Romanoff / Black Widow'),
 (14,10,14,1,'Kim Ki-taek'),
 (15,11,11,1,'J. Robert Oppenheimer'),
 (16,11,2,2,NULL),
 (17,12,12,1,'Paul Atreides'),
 (18,13,2,2,NULL),
 (19,13,2,3,NULL),
 (20,14,13,1,'Barbie'),
 (21,14,10,2,NULL),
 (22,14,10,3,NULL);

INSERT INTO reviews (review_id, movie_id, author_name, review_text, review_date) VALUES
 (1,1,'Alex M.','Mind-bending masterpiece with stunning visuals.','2023-05-12'),
 (2,1,'Maria K.','Complex plot that rewards multiple viewings.','2023-06-01'),
 (3,2,'John D.','Heath Ledger delivers an unforgettable performance.','2023-04-20'),
 (4,3,'Sophie L.','Tarantino at his absolute best.','2023-03-15'),
 (5,4,'Chris P.','Emotionally powerful and scientifically intriguing.','2023-07-08'),
 (6,5,'Anna R.','Beautiful music and cinematography.','2023-02-28'),
 (7,6,'Mike T.','Revolutionary for its time and still holds up.','2023-01-10'),
 (8,7,'Elena V.','Tom Hanks is perfect in this role.','2023-08-05'),
 (9,8,'David S.','Twists that stay with you for years.','2023-09-12'),
 (10,9,'Kate B.','Epic conclusion to the Infinity Saga.','2023-05-30'),
 (11,10,'Olena S.','A razor-sharp and unsettling social satire.','2023-10-14'),
 (12,11,'Taras H.','Gripping and visually powerful biographical drama.','2023-08-20'),
 (13,12,'Iryna P.','Visually stunning sci-fi epic.','2024-03-05'),
 (14,13,'Andrii L.','Complex time inversion concept that demands attention.','2023-09-18');

INSERT INTO ratings (rating_id, movie_id, user_name, score, rating_date) VALUES
 (1,1,'user01',9.0,'2023-05-10'),
 (2,1,'user02',8.5,'2023-05-15'),
 (3,2,'user03',9.5,'2023-04-18'),
 (4,3,'user04',9.0,'2023-03-12'),
 (5,4,'user05',8.8,'2023-07-05'),
 (6,5,'user06',8.0,'2023-02-25'),
 (7,6,'user07',8.7,'2023-01-08'),
 (8,7,'user08',8.9,'2023-08-01'),
 (9,8,'user09',8.6,'2023-09-10'),
 (10,9,'user10',8.4,'2023-05-28'),
 (11,10,'user11',8.9,'2023-06-20'),
 (12,11,'user12',8.9,'2023-08-12'),
 (13,12,'user13',8.6,'2024-03-10'),
 (14,13,'user14',7.3,'2023-09-10'),
 (15,14,'user15',6.9,'2023-07-25');

INSERT INTO trivia (trivia_id, movie_id, fact_text) VALUES
 (1,1,'The spinning top at the end was left deliberately ambiguous by Nolan.'),
 (2,2,'Heath Ledger locked himself in a hotel room for weeks to prepare the Joker.'),
 (3,3,'The script was written in a non-linear fashion from the beginning.'),
 (4,4,'The black hole visual effects were based on real scientific calculations.'),
 (5,5,'Emma Stone and Ryan Gosling performed most of the dancing themselves.'),
 (6,6,'The red pill / blue pill scene became a cultural phenomenon.'),
 (7,7,'Tom Hanks gained and lost significant weight for different stages of the character.'),
 (8,8,'Brad Pitt and Edward Norton trained extensively for the fight scenes.'),
 (9,9,'The final battle sequence took months to film and involved thousands of VFX shots.'),
 (10,10,'The film won the Palme d''Or at Cannes before becoming a global hit.'),
 (11,11,'Filmed using IMAX 65mm and Panavision 65mm large-format film.'),
 (12,12,'Filmed extensively in the deserts of Abu Dhabi and Jordan.'),
 (13,13,'The word Tenet is a palindrome.'),
 (14,14,'The production used so much pink paint that a shortage of it was reported.');

INSERT INTO box_office (box_id, movie_id, country_id, amount_usd) VALUES
 (1,1,1,292600000.00),
 (2,1,2,56000000.00),
 (3,2,1,534900000.00),
 (4,2,2,89000000.00),
 (5,3,1,107900000.00),
 (6,4,1,188000000.00),
 (7,5,1,151100000.00),
 (8,6,1,171500000.00),
 (9,9,1,858400000.00),
 (10,10,1,53370000.00),
 (11,10,10,72000000.00),
 (12,11,1,329000000.00),
 (13,12,1,282000000.00),
 (14,13,1,58500000.00),
 (15,14,1,636200000.00);