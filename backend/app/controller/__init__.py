from flask import Blueprint
from flask_restx import Api
from .sentiment import api as sentiment_ns


blueprint = Blueprint("api", __name__)

api = Api(
    blueprint, title="Sentiment Analysis", version="1.0", description=""
)

api.add_namespace(sentiment_ns, path="/sentiment")


