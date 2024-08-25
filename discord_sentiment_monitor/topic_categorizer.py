from transformers import pipeline

classifier = pipeline("zero-shot-classification")

def categorize_topic(text):
    categories = [
        "suggestion", 
        "positive feedback", 
        "negative feedback", 
        "neutral feedback", 
        "discussion", 
        "bug report", 
        "support request", 
        "off-topic", 
        "spam",
        "competitor mentions"
    ]

    result = classifier(text, categories)
    
    return result['labels'][0]  # Return the most likely category
