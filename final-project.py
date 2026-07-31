from flask import Flask, render_template, request
import pandas as pd
import csv
import random

# creates flask instance
app = Flask(__name__)

# reads pokemon database and sets as variable
df = pd.read_csv('pokemon_dataset.csv')

# home page route for pack opening page
@app.route('/')
def home():
    return render_template('final_project.html', money=50)

# get/post req and adds persistent csv info, or replaces old info if the name already exists, loads back to pack page with the original battle info
@app.route('/signup/<card_signup>/<money_signup>', methods=['GET', 'POST'])
def signup(card_signup, money_signup):
    if request.method == 'POST':
        name = request.form['name']
        with open("data.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            players = list(reader)
        for player in players:
            if player["name"] == name:
                player["card"] = card_signup
                player["money"] = money_signup
                break
        with open("data.csv", "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["name", "card", "money"]
            )
            writer.writeheader()
            writer.writerows(players)
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, card_signup, money_signup])
    return render_template("signup.html", card=card_signup, money=money_signup)

# get/post req and gets info from csv and loads to pokemon pack opener with the saved user info or original battle info if they didn't log in
@app.route('/login/<card_login>/<money_login>', methods=['GET', 'POST'])
def login(card_login, money_login):
    if request.method == 'POST':
        name = request.form['name']
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == name:
                    player = row
                    card_login = player['card']
                    money_login = player['money']
                    break
    return render_template("login.html", card=card_login, money=money_login)

# battle page route, generates random card for opponent, and reads/interprets the pokemon dataset to find rarity of player and opponents card for battle to determine who wins
@app.route('/battle/<card1>/<money1>')
def battle(card1,money1):
    try:
        int(card1)
    except ValueError:
        card1 = 0
    opp_card = random.randint(0,120)
    player_card_rarity = df.loc[df['Number'] == int(card1), 'Rarity'].iloc[0]
    opp_card_rarity = df.loc[df['Number'] == int(opp_card), 'Rarity'].iloc[0]
    return render_template('battle.html', card=card1, money=money1, player_card_rarity=player_card_rarity, opp_card_rarity=opp_card_rarity, opp_card=opp_card)

# shop page that uses the pokemon dataset to get the actual card value of the player's rarest card and returns it to the shop page with money and the card
@app.route('/shop/<card2>/<money2>')
def shop(card2,money2):
    try:
        int(card2)
    except ValueError:
        card2 = 0
    card_value = df.loc[df['Number'] == int(card2), 'Market Price'].iloc[0]
    return render_template('shop.html', card=card2, money=money2, card_value=card_value)

# route set after entering shop/battle so that money isn't reset to $50.00 and is set as a parameter along with their rarest card
@app.route('/<card3>/<money3>')
def homer(card3, money3):
    return render_template('final_project.html', card=card3, money=money3)

# runs file info when run
if __name__ == '__main__':
    app.run(debug=True)

