from flask_restx import Namespace, fields

class SentimentDto():
    api = Namespace('Sentiment & TSA', description='')
    model = api.model('sentiment', {
        'stock': fields.String(required=True),
        'ticker': fields.String(required=True),
        'tweets': fields.Integer(required=False),
    })
    model_sentiment_analysis = api.model('Sentiment Analysis', {
        'stock': fields.String(required=True),
        'tweets': fields.Integer(required=False),
    })
    model_tsa = api.model('TSA', {
        'ticker': fields.String(required=True),
    })
