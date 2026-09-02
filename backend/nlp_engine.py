from transformers import pipeline

# 1. Initialize the AI model outside the function.
# This ensures it only loads into memory once when the server starts, not every time a request is made.
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_review_sentiments(reviews_list):
    if not reviews_list:
        return None
        
    analyzed_data = []
    total_score = 0
    
    # 2. Loop through each scraped review
    for review in reviews_list:
        # Some reviews might be too long for the model's token limit, so we truncate them
        # The pipeline returns a list of dictionaries like: [{'label': 'POSITIVE', 'score': 0.98}]
        result = sentiment_pipeline(review[:512])[0] 
        
        label = result['label']
        confidence = result['score']
        
        # 3. Convert POSITIVE/NEGATIVE labels into a numerical scale (0 to 100) for aggregation
        if label == 'POSITIVE':
            numerical_score = confidence * 100
        else:
            numerical_score = (1 - confidence) * 100
            
        total_score += numerical_score
        
        analyzed_data.append({
            "text": review,
            "label": label,
            "confidence": round(confidence, 4)
        })
        
    # 4. Calculate the average score for the entire product
    average_score = total_score / len(reviews_list)
    
    # 5. Map the average score to your custom scale
    if average_score < 40:
        final_rating = "Worst"
    elif average_score < 60:
        final_rating = "Good"
    elif average_score < 80:
        final_rating = "Better"
    else:
        final_rating = "Best"
        
    return {
        "final_rating": final_rating,
        "average_score": round(average_score, 2),
        "detailed_analysis": analyzed_data
    }