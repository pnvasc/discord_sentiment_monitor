from transformers import pipeline

# Update the pipeline to use the Cardiff NLP model
sentiment_pipeline = pipeline("sentiment-analysis", model="j-hartmann/sentiment-roberta-large-english-5-classes")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    
    if result['label'] == 'very negative':
        return -1
    elif result['label'] == 'negative':
        return -0.5
    elif result['label'] == 'neutral':
        return 0
    elif result['label'] == 'positive':
        return 0.5
    else:  # very positive
        return 1