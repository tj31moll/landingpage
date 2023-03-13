from flask import Flask, jsonify
import praw
import tweepy
import instaloader
from TikTokApi import TikTokApi
from homeassistant_api import HomeAssistant
from onenote_api import OneNoteAPI

app = Flask(__name__)

# Reddit API credentials
reddit_client_id = 'REPLACE_WITH_REDDIT_CLIENT_ID'
reddit_client_secret = 'REPLACE_WITH_REDDIT_CLIENT_SECRET'
reddit_username = 'REPLACE_WITH_REDDIT_USERNAME'
reddit_password = 'REPLACE_WITH_REDDIT_PASSWORD'

# Twitter API credentials
twitter_consumer_key = 'REPLACE_WITH_TWITTER_CONSUMER_KEY'
twitter_consumer_secret = 'REPLACE_WITH_TWITTER_CONSUMER_SECRET'
twitter_access_token = 'REPLACE_WITH_TWITTER_ACCESS_TOKEN'
twitter_access_token_secret = 'REPLACE_WITH_TWITTER_ACCESS_TOKEN_SECRET'

# Instagram API credentials
instagram_username = 'REPLACE_WITH_INSTAGRAM_USERNAME'
instagram_password = 'REPLACE_WITH_INSTAGRAM_PASSWORD'

# TikTok API credentials
tiktok_username = 'REPLACE_WITH_TIKTOK_USERNAME'
tiktok_password = 'REPLACE_WITH_TIKTOK_PASSWORD'

# Home Assistant API credentials
homeassistant_url = 'http://REPLACE_WITH_HOMEASSISTANT_IP:8123'
homeassistant_token = 'REPLACE_WITH_HOMEASSISTANT_API_TOKEN'

# OneNote API credentials
onenote_token = 'REPLACE_WITH_ONENOTE_API_TOKEN'

# Initialize APIs
reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, username=reddit_username, password=reddit_password, user_agent='my_home_website')
auth = tweepy.OAuth1UserHandler(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)
instagram = instaloader.Instaloader()
instagram.load_session_from_file(instagram_username, filename='REPLACE_WITH_INSTAGRAM_SESSION_FILE')
tiktok = TikTokApi()
tiktok.login(username=tiktok_username, password=tiktok_password)
homeassistant = HomeAssistant(homeassistant_url, homeassistant_token)
onenote = OneNoteAPI(onenote_token)

@app.route('/api/reddit')
def get_reddit_posts():
    subreddit = reddit.subreddit('REPLACE_WITH_SUBREDDIT_NAME')
    posts = []
    for post in subreddit.new(limit=10):
        posts.append({'title': post.title, 'url': post.url})
    return jsonify({'posts': posts})

@app.route('/api/twitter')
def get_twitter_tweets():
    api = tweepy.API(auth)
    tweets = api.user_timeline(count=10)
    tweets_list = []
    for tweet in tweets:
        tweets_list.append({'id_str': tweet.id_str, 'text': tweet.text, 'user': {'screen_name': tweet.user.screen_name}})
    return jsonify({'tweets': tweets_list})

@app.route('/api/instagram')
def get_instagram_posts():
    profile = instaloader.Profile.from_username(instagram.context, 'REPLACE_WITH_INSTAGRAM_USERNAME')
    posts = []
    for post in profile.get_posts():
        posts.append({'image_url': post.url, 'caption': post.caption})
        if len(posts) >= 10:
            break
    return jsonify({'posts': posts})

@app.route('/api/tiktok')
def get_tiktok_videos():
    user_videos = tiktok.by_username('REPLACE_WITH_TIKTOK_USERNAME', count=10)
    videos = []
    for video in user_videos:
        videos.append({'video_url': video['video']['downloadAddr'], 'caption': video['desc']})
    return jsonify({'
return jsonify({'videos': videos})

@app.route('/api/homeassistant')
def get_homeassistant_entities():
    entities = homeassistant.get_entities()
    return jsonify({'entities': entities})

@app.route('/api/onenote')
def get_onenote_notes():
    notebooks = onenote.get_notebooks()
    notes = []
    for notebook in notebooks:
        sections = onenote.get_sections(notebook['id'])
        for section in sections:
            section_notes = onenote.get_notes(section['id'])
            for note in section_notes:
                notes.append({'id': note['id'], 'title': note['title']})
                if len(notes) >= 10:
                    break
            if len(notes) >= 10:
                break
        if len(notes) >= 10:
            break
    return jsonify({'notes': notes})

if __name__ == '__main__':
    app.run(debug=True)
