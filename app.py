import recommend
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# http://localhost:5000/api?query=happy

@app.route('/api', methods = ['GET'])
def getTracks():
    mood = str(request.args['query'])
    re = recommend.mood_based_recommend(mood)
    track_list = [i for i in re['track_name']]
    data = {'query': mood, 'tracks': track_list}
    json_dump = json.dumps(data)
    return json_dump

if __name__ == "__main__":
    app.run(port=7775)
