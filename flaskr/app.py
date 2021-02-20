import json
from flask import Flask, render_template, request
import data_fetch as simple_db

def is_int(obj): 
    ''' To check for type integer 
    '''
    try:
        int(obj)
    except:
        return False
    return True


app = Flask(__name__)


@app.route("/")
def sgf():
    ''' Default route to load html page
    '''
    return render_template("index.html")


@app.route("/api/artist", methods=["POST"])
def fetch_artist():
    ''' Method to fetch artist based on search criteria
    '''
    artist = request.form.get("artist", "")
    skip = request.form.get("skip", 0)
    if not is_int(skip):
        skip = 0

    limit = request.form.get("limit", 50)
    if not is_int(limit):
        limit = 50

    # fetch and filter from JSON
    data = simple_db.fetch_artist(artist, int(skip), int(limit))
    # Response
    output = {
        "filter": {"name": artist, "skip": skip, "limit": limit},
        "allDataCount": data[1],
        "count": len(data[0]),
        "data": data[0],
    }

    return output


if __name__ == "__main__":
    app.run(debug=True)
