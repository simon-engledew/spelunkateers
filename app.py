import flask
import feedparser
import json
import datetime
import time
import base64
import binascii
import os
import time

def to_isodate(value):
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')

class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, time.struct_time):
            return to_isodate(datetime.datetime.fromtimestamp(time.mktime(o)))
        return json.JSONEncoder.default(self, o)

app = flask.Flask(__name__)
app.json_encoder = DateEncoder

def now():
    return str(int(time.time()))

def static(path):
    return flask.url_for('static', filename=path, cache=str(int(os.stat(os.path.join(app.static_folder, path)).st_mtime)))

@app.context_processor
def functions():
    return {'now': now, 'static': static}

@app.route('/')
def root():
    return flask.render_template('index.html')

def data():
    return feedparser.parse('http://gdata.youtube.com/feeds/base/users/Spelunkateers/uploads?alt=rss&v=2&orderby=published')

@app.route('/feed.json')
def feed():
    return flask.Response('var data = {0};'.format(json.dumps(data(), cls=DateEncoder)), mimetype='application/json')

if __name__ == "__main__":
    app.debug = True
    app.run()
