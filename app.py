from flask import Flask, jsonify
from main import run
import time


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def home_page():
    text ="<h1>Ensure that the url you are inputing is the base(homepage url)</h1>"
    return text

@app.route('/pathroute/<path:url>')
def scrape(url):
    now = time.time()
    result = run(url)
    print(time.time()-now)
    return jsonify(result)

if __name__ =='__main__':
    app.run()
#export FLASK_ENV=development
