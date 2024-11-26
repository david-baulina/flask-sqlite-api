from flask import Flask, request, jsonify
import requests
from markupsafe import escape
import json
from app.models.db import DB
from app.utils.helpers import extra_source_response_adapter

app = Flask(__name__)

@app.route('/', methods=['POST'])
def add_job():
    if request.method == 'POST':
        db = DB()
        create_table = db.create_table()
        create_job = db.create_job(request.json)
        return json.dumps(create_job)
    else:
        return "error"

@app.route('/', methods=['GET'])
def search_job():
    if request.method == 'GET':
        db = DB()
        try:
            search_job = db.search_job(request.args.to_dict())
            # return search_job

            url = "http://localhost:8081/jobs"
            response = requests.get(url, params=request.args.to_dict())
            response.raise_for_status()
            alt_source = extra_source_response_adapter(response.json())

            return search_job+alt_source


        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
    else:
        return "error"

if __name__ == "__main__":
    app.run(debug=True)