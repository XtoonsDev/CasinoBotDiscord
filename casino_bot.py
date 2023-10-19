import discord
from discord.ext import commands
import mysql.connector
from config import TOKEN, DB_CONFIG

# Connexion à la base de données
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Configurations
PREFIX = "!"  # Préfixe pour les commandes

# Initialisation du bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Fonctions pour interagir avec la base de données

def inserer_utilisateur(username, credits):
    cursor.execute("INSERT INTO users (username, credits) VALUES (%s, %s)", (username, credits))
    conn.commit()

def selectionner_utilisateur_par_id(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

def inserer_partie(user_id, game_type, result, bet, won):
    cursor.execute("INSERT INTO games (user_id, game_type, result, bet, won) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, game_type, result, bet, won))
    conn.commit()

def selectionner_parties_utilisateur(user_id):
    cursor.execute("SELECT * FROM games WHERE user_id = %s", (user_id,))
    return cursor.fetchall()

def mettre_a_jour_solde(user_id, nouveaux_credits):
    cursor.execute("UPDATE users SET credits = %s WHERE id = %s", (nouveaux_credits, user_id))
    conn.commit()

def supprimer_partie(game_id):
    cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
    conn.commit()

def fermer_connexion():
    cursor.close()
    conn.close()

# Commandes Discord

@bot.command()
async def donner(ctx, membre: discord.Member, montant: int):
    # Fonction pour donner de l'argent à un utilisateur
    # ...

@bot.command()
async def solde(ctx):
    # Fonction pour consulter son solde
    # ...

@bot.command()
async def roulette(ctx, mise: int, choix: int):
    # Fonction pour jouer à la roulette
    # ...

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')

bot.run(TOKEN)
