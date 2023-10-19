# Casino Discord Bot

## Description

Le Casino Discord Bot est un script Python qui permet de créer un bot pour Discord avec des fonctionnalités de jeu de casino. Il inclut un jeu de roulette et un système d'économie simplifié pour les utilisateurs.

## Dépendances & Installation

- **Dépendances**:
  - Python 3.x
  - Les modules Discord.py (`discord.py`) et MySQL-connector (`mysql-connector-python`) sont requis pour exécuter le script.
  - Vous pouvez installer ces dépendances en exécutant la commande suivante :
    ```
    pip install discord mysql-connector-python
    ```

## MySQL

- **Configuration de la base de données**:
  - Vous devez créer une base de données MySQL pour stocker les informations des utilisateurs et des jeux du casino. Dans le fichier `config.py`, vous devez spécifier les informations de connexion à votre base de données, telles que l'hôte, le nom d'utilisateur, le mot de passe et le nom de la base de données.

- **Création des tables**:
  - Vous pouvez utiliser le script SQL suivant pour créer les tables nécessaires dans votre base de données :
    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        credits INT
    );

    CREATE TABLE games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        game_type VARCHAR(255),
        result VARCHAR(255),
        bet INT,
        won INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```

## Crédit ChatGPT

Ce bot a été créé en utilisant ChatGPT, un modèle de langage développé par OpenAI. Il est basé sur l'architecture GPT-3.5 et a été formé pour générer du texte à partir de requêtes humaines. Pour plus d'informations, veuillez consulter le [site d'OpenAI](https://openai.com/).
