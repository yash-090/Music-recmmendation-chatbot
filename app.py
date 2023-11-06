from flask import Flask, request, render_template
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests

app = Flask(_name_)

# Download NLTK data (if not already downloaded)
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Last.fm API credentials
LASTFM_API_KEY = '18324e0e4dd989e783ca4ca318b6f969'

@app.route('/', methods=['GET', 'POST'])
def music_recommendation():
    mood = None
    recommendations = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        mood = get_user_mood(user_input)

        # Fetch music recommendations based on mood
        recommendations = get_music_recommendations(mood)

    return render_template('index.html', mood=mood, recommendations=recommendations)

def get_user_mood(text):
    sentiment = sid.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'happy'
    elif sentiment['compound'] <= -0.05:
        return 'sad'
    else:
        return 'neutral'

def get_music_recommendations(mood):
    url = f'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={mood}&api_key={LASTFM_API_KEY}&format=json'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('track', [])
            recommendations = [track['name'] for track in tracks]
            return recommendations
        else:
            return []

    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

if _name_ == '_main_':
    app.run(debug=False)
