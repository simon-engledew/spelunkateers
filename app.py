import flask
import feedparser
import json
import datetime
import time
import base64
import binascii
import os

def to_isodate(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')

class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, time.struct_time):
            return to_isodate(datetime.datetime.fromtimestamp(time.mktime(o)))
        return json.JSONEncoder.default(self, o)

app = flask.Flask(__name__, static_url_path='')
app.json_encoder = DateEncoder

def token(bytes=32):
    return base64.urlsafe_b64encode(os.urandom(bytes))

@app.context_processor
def functions():
    return {'token': token}

@app.route('/')
def root():
    return flask.render_template('index.html')

@app.route('/feed.json')
def feed():
    data = feedparser.parse('http://gdata.youtube.com/feeds/base/users/Spelunkateers/uploads?alt=rss&v=2&orderby=published')
    # return flask.json.dumps(data)
    return flask.Response('var data = {0};'.format(json.dumps(data, cls=DateEncoder)), mimetype='application/json')

if __name__ == "__main__":
    app.debug = True
    app.run()
