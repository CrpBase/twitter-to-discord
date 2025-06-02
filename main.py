import requests
import time
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# Список акаунтів Twitter
users = [
    'pauliepunt',
    'C_Angermayer',
    'proofofnathan',
    'scene999',
    '0xG00gly',
    'lucidxpl',
    'rongplace',
    'kay00nee',
    'jakewittman',
    'hwbehrens',
    'Digorithm'
]

WEBHOOK_URL = 'https://discord.com/api/webhooks/1379113918324019241/LljwZcm9Yux0ooGMczqLdwVqBRTNo1R_konIvn51Kufs7bWOaE1crvkXnfF3-D3evPmh'

last_tweets = {}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def fetch_latest_tweet(username):
    url = f"https://nitter.net/{username}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        first_tweet = soup.find('div', {'class': 'timeline-item'})
        if not first_tweet:
            return None, None
        tweet_link = first_tweet.find('a', href=True)['href']
        tweet_id = tweet_link.split('/')[-1]
        tweet_text = first_tweet.find('div', {'class': 'tweet-content'}).text.strip()
        return tweet_id, tweet_text
    except:
        return None, None

def send_to_discord(user, text, tweet_id):
    link = f"https://x.com/{user}/status/{tweet_id}"
    content = f"Новий твіт від @{user}:
{text}
{link}"
    data = {"content": content}
    requests.post(WEBHOOK_URL, json=data)

# Flask вебсервер для підтримки активності
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# Основний цикл перевірки твітів
while True:
    for user in users:
        tweet_id, tweet_text = fetch_latest_tweet(user)
        if tweet_id and (user not in last_tweets or last_tweets[user] != tweet_id):
            last_tweets[user] = tweet_id
            send_to_discord(user, tweet_text, tweet_id)
    time.sleep(90)