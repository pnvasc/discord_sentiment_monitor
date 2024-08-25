from sqlalchemy import func
from .database import Session, Message

def segment_users():
    session = Session()
    user_sentiments = session.query(
        Message.user_id,
        func.avg(Message.sentiment_score).label('avg_sentiment')
    ).group_by(Message.user_id).all()

    segments = {'optimists': [], 'neutrals': [], 'pessimists': []}
    for user_id, avg_sentiment in user_sentiments:
        if avg_sentiment > 0.35:
            segments['optimists'].append(user_id)
        elif avg_sentiment < -0.35:
            segments['pessimists'].append(user_id)
        else:
            segments['neutrals'].append(user_id)

    session.close()
    return segments