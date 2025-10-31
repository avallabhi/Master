from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Paste your Slack webhook URL here
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/KKK"

@app.route("/github", methods=["POST"])
def github_event():
    data = request.json

    # Extract some basic info from GitHub payload
    repo = data["repository"]["name"]
    pusher = data["pusher"]["name"]
    commit_msg = data["head_commit"]["message"]
    commit_url = data["head_commit"]["url"]

    # Format Slack message
    slack_data = {
        "text": f"🚀 *New push to {repo}* by *{pusher}*\n"
                f"💬 Commit message: {commit_msg}\n"
                f"🔗 <{commit_url}|View Commit>"
    }

    # Send to Slack
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)

    if response.status_code != 200:
        print("Error sending to Slack:", response.text)
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
