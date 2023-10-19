-- Création de la table 'users'
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    credits INT
);

-- Création de la table 'games'
CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    game_type VARCHAR(255),
    result VARCHAR(255),
    bet INT,
    won INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
