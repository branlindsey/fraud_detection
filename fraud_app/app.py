import pandas as pd
import psycopg2 as pg 
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('fraud.html', tables)

@app.route("/table")
def show_table():
    data = pd.DataFrame({'a': 1, 'b': 2, 'c': 3}, index=['Time', 'Space', "Everything"])
table = data.to_html()
    return render_template('fraud.html', tables =table)
'''
@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    a, b, c, d = user_data['a'], user_data['b'], user_data['c'], user_data['d']
    prediction = _return_prediction(a, b, c, d)
    return jsonify({'prediction': prediction})


def _return_prediction(a, b, c, d):
    gbc = pickle.load(open('gbc.sav', 'rb'))
    X = np.array([[a,b,c,d]])
    prediction = gbc.predict_proba(X)[0][1]
    return prediction.round(2) * 100
'''    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
