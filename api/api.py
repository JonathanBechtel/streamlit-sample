"""
simple flask app that hosts an API for monthly returns gbm model
"""
from flask import Flask, request
import pandas as pd
import pickle
import json

app = Flask(__name__)

# fn to load in model
def load_model():
    with open('models/mod.pickle', 'rb') as mod:
        pipe = pickle.load(mod)
    return pipe

pipe = load_model()

@app.route('/', methods = ['GET'])
def view():
    return 'Hello World!'

@app.route('/predict', methods = ['POST'])
def predict():
    data    = request.json
    samples = pd.DataFrame(json.loads(data['arr']))
    samples.columns = ['Ticker', 'monthRet', 'annRet', 'qRet', 'monthRetMkt', 
                       'qRetMkt', 'annRetMkt','regime']
    preds   = pipe.predict(samples)
    return json.dumps(preds.tolist())

if __name__ == '__main__':
    app.run(host = 0.0.0.0, port = 80)