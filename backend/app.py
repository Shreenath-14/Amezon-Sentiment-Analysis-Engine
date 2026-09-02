import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

# Custom module imports
from scraper import fetch_product_details, fetch_product_reviews
from nlp_engine import analyze_review_sentiments
from db_manager import save_analysis_results

app = flask.Flask(__name__)
CORS(app) # Allows Next.js to communicate with Flask

# Your first API endpoint
@app.route('/api/fetch-product', methods=['POST'])
def fetch_product():
    # 1. Receive the data from Next.js
    data = flask.request.get_json()
    
    if not data or 'url' not in data:
        return flask.jsonify({"error": "No URL provided"}), 400
        
    amazon_url = data.get('url')
    # Input Sanitization: Auto-correct missing schemes
    if not amazon_url.startswith('http'):
        amazon_url = 'https://' + amazon_url
    
    # 1. Call the function from scraper.py and pass the URL
    product_title = fetch_product_details(amazon_url)
    
    # 2. Check if the scraper failed (returned None)
    if not product_title:
         return flask.jsonify({"error": "Failed to scrape product. Amazon might have blocked us."}), 503
    
    # 3. Return the successful title back to Next.js
    return flask.jsonify({
        "status": "success", 
        "product_title": product_title, 
        "url_received": amazon_url
    })

@app.route('/api/analyze-reviews', methods=['POST'])
def analyze_reviews():
    data = flask.request.get_json()
    
    if not data or 'url' not in data:
        return flask.jsonify({"error": "No URL provided"}), 400
        
    amazon_url = data.get('url')
    if not amazon_url.startswith('http'):
        amazon_url = 'https://' + amazon_url
        
    # 1. Call the new review scraper function
    reviews = fetch_product_reviews(amazon_url)
    
    if reviews is None:
        return flask.jsonify({"error": "Failed to scrape reviews. Amazon might have blocked us."}), 503
        
    if len(reviews) == 0:
        return flask.jsonify({"error": "No reviews found on this page."}), 404
    
    # 2. To-do later: Pass these reviews to the Hugging Face NLP engine
    sentiment_results = analyze_review_sentiments(reviews)
    
    # 3. Save the results to MySQL
    db_success = save_analysis_results(amazon_url, sentiment_results)
    
    if not db_success:
        return flask.jsonify({"error": "Failed to save results to database"}), 500
    
    return flask.jsonify({
        "status": "success",
        "review_count": len(reviews),
        "sentiment_summary": sentiment_results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)