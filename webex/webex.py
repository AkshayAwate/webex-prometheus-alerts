
from flask import Flask, request
import json
import requests
from werkzeug.exceptions import HTTPException
# Define Webex API credentials
webex_token = ""
webex_room = ""

app = Flask(__name__)

@app.route('/alertmanager', methods=['POST'])
def alertmanager():
    try:
        if request.is_json:
            post_data = json.loads(request.data)
            alert_data(post_data)
    except Exception as e:
        print("Storing alerts failed in main:", e)
        return {"ERROR"}, 500

    return "NOK", 200

def alert_data(data):
    if "alerts" in data:
        for i in data["alerts"]:
            try:
                alertname = "**Alertname:** "
                summary = "**Summary:** "
                description = "**Description:** "
                if "alertname" in i["labels"]:
                    alertname = alertname + i["labels"]["alertname"]
                if "summary" in i["annotations"]:
                    summary = summary + i["annotations"]["summary"]
                if "description" in i["annotations"]:
                    description = description + i["annotations"]["description"]
                alert = alertname + "\n" + summary  + description + "\n"
                webex_data = {"roomId": webex_room, "markdown": alert}
                headers = {"Authorization": "Bearer " + webex_token}
                response = requests.post('https://webexapis.com/v1/messages', headers=headers, json=webex_data)
                response.raise_for_status()  # Raise an exception for HTTP errors
            except Exception as e:
                print("Storing alerts failed in sub:", e)
                return {"ERROR"}, 500

    return "OK", 200

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9091, debug=0)
