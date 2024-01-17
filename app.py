from flask import Flask, render_template, request
from textblob import TextBlob  # Import TextBlob for sentiment analysis
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to perform sentiment analysis on a single review
def analyze_sentiment(review):
    sentiment_score = TextBlob(review).sentiment.polarity
    return 'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the URL from the form submission
        url = request.form['url']

        # Send a GET request to the provided URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <p> tags with the specified class
            p_tags = soup.find_all('p', class_='comment__09f24__D0cxf css-qgunke')

            # Extract the text content of each matching <p> tag
            p_texts = [p_tag.get_text() for p_tag in p_tags]

            # Perform sentiment analysis on each review
            sentiments = [analyze_sentiment(review) for review in p_texts]

            # Calculate positive and negative percentages
            total_reviews = len(sentiments)
            positive_percentage = (sentiments.count('Positive') / total_reviews) * 100
            negative_percentage = (sentiments.count('Negative') / total_reviews) * 100

            return render_template('dashboard.html', url=url, p_texts=p_texts,
                                   positive_percentage=positive_percentage, negative_percentage=negative_percentage)

        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"

    return render_template('dashboard.html', url=None, p_texts=None,
                           positive_percentage=None, negative_percentage=None)

if __name__ == '__main__':
    app.run(debug=True)
