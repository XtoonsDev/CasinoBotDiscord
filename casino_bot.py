import discord
from discord.ext import commands
import mysql.connector
from datetime import datetime, timedelta
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

# Nouvelles fonctions pour gérer les sessions

sessions = []  # Une liste pour suivre les sessions actives
session_en_cours = None

def creer_session(heure_debut, heure_fin):
    session = {
        'heure_debut': heure_debut,
        'heure_fin': heure_fin,
        'participants': []
    }
    sessions.append(session)
    return session

def trouver_session_en_cours():
    maintenant = datetime.now()
    for session in sessions:
        if session['heure_debut'] <= maintenant <= session['heure_fin']:
            return session
    return None

def demarrer_decompte():
    global session_en_cours
    session_en_cours = trouver_session_en_cours()
    if session_en_cours is not None:
        session_en_cours['heure_fin'] = datetime.now() + timedelta(minutes=5)
        return True
    return False

# Commandes Discord

@bot.command()
async def lancer_session(ctx, heure_debut, heure_fin):
    heure_debut = datetime.strptime(heure_debut, "%H:%M")
    heure_fin = datetime.strptime(heure_fin, "%H:%M")
    session = creer_session(heure_debut, heure_fin)
    await ctx.send(f"Session créée ! Elle débute à {heure_debut.strftime('%H:%M')} et se termine à {heure_fin.strftime('%H:%M')}.")

@bot.command()
async def miser(ctx, montant):
    global session_en_cours
    if session_en_cours is not None and session_en_cours['heure_fin'] >= datetime.now():
        session_en_cours['participants'].append({'user_id': ctx.author.id, 'montant': montant})
        await ctx.send(f"Mise de {montant} crédits enregistrée.")
    else:
        await ctx.send("Il n'y a pas de session en cours ou le délai pour miser est écoulé.")

@bot.command()
async def lancer_roulette(ctx):
    global session_en_cours
    if session_en_cours is not None and session_en_cours['heure_fin'] >= datetime.now():
        # Logique de la roulette
        import random
        resultat = random.randint(0, 36)

        for participant in session_en_cours['participants']:
            participant['resultat'] = random.randint(0, 36)  # Résultat pour chaque participant (pour cet exemple, c'est aléatoire)
            participant['gagne'] = participant['resultat'] == resultat

            if participant['gagne']:
                mettre_a_jour_solde(participant['user_id'], participant['montant'])

        await ctx.send("La roulette a été lancée ! Voici les résultats pour chaque participant :")
        for participant in session_en_cours['participants']:
            await ctx.send(f"Utilisateur {participant['user_id']} a obtenu {participant['resultat']}. {'Gagné !' if participant['gagne'] else 'Perdu.'}")
        
        sessions.remove(session_en_cours)
        session_en_cours = None
    else:
        await ctx.send("Il n'y a pas de session en cours ou le délai pour miser est écoulé.")

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')

bot.run(TOKEN)
