from flask_restx import Resource
from flask import request, send_file, render_template
from app.util.sentiment_dto import SentimentDto
from flask_cors import  cross_origin

api = SentimentDto.api
_sentiment = SentimentDto.model
_sentiment_analysis = SentimentDto.model_sentiment_analysis
_tsa = SentimentDto.model_tsa

@api.route('/SentimentAnalysis')
class SentimentAnalysis(Resource):
    @api.doc('SentimentAnalysis')
    @api.expect(_sentiment_analysis, envelope='data')
    @api.response(404, 'SentimentAnalysis')
    def post(self):
        data = request.json
        from app.services.keyword_sentiment import keyword_sentiment 
        #keyword_sentiment(data["stock"], data["tweets"])
        print("Done with Sentiment")
        return {"status" : "success"}

@api.route('/TSA')
class TSA(Resource):
    @api.doc('TSA')
    @api.expect(_tsa, envelope='data')
    @api.response(404, 'TSA')
    def post(self):
        data = request.json
        from app.services.TSA import updatePNGsAndReturnPrediction, ModelPricePred, closePriceHistory
        prices = updatePNGsAndReturnPrediction(data["ticker"])
        valid_price = prices[0]
        pred_price = prices[1]
        print("Done with TSA")
        return {"status" : "success", "price": str(valid_price), "pred_price": str(pred_price)}



@api.route('/WordloudAll')
class WordloudAll(Resource):
    @api.doc('WordloudAll')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/wordcloud_all.png")

@api.route('/WordloudPositive')
class WordloudPositive(Resource):
    @api.doc('WordloudPositive')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/wordcloud_positive.png")

@api.route('/WordloudNegative')
class WordloudNegative(Resource):
    @api.doc('WordloudNegative')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/wordcloud_negative.png")

@api.route('/SentimentAmount')
class SentimentAmount(Resource):
    @api.doc('SentimentAmount')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/Sentiment_Amount.png")

@api.route('/SentimentBoxplot')
class SentimentBoxplot(Resource):
    @api.doc('SentimentBoxplot')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/Sentiment_Boxplot.png")

@api.route('/PriceHistory')
class PriceHistory(Resource):
    @api.doc('PriceHistory')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/PriceHistory.png")

@api.route('/ModelPrediction')
class ModelPrediction(Resource):
    @api.doc('ModelPrediction')
    @api.response(404, 'Error')
    def get(self):
        return send_file("../output/ModelPrediction.png")

