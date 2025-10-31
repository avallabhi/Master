from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

@app.route("/github", methods=["POST"])
def github_to_slack():
    try:
        event_type = request.headers.get("X-GitHub-Event")
        if event_type == "ping":
            return jsonify({"msg": "pong"}), 200

        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        repo_name = data.get("repository", {}).get("name", "Unknown repo")
        pusher_name = data.get("pusher", {}).get("name", "Unknown pusher")
        commits = data.get("commits", [])

        if not commits:
            message = f"⚠️ Push to {repo_name} by {pusher_name}, but no commits to show."
        else:
            lines = [f"🚀 New push to `{repo_name}` by `{pusher_name}`"]
            for c in commits:
                msg = c.get("message", "No message")
                url = c.get("url", "")
                lines.append(f"• <{url}|{msg}>")
            message = "\n".join(lines)

        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code != 200:
            print("Slack error:", response.text)
            return jsonify({"status": "error", "slack_response": response.text}), 500

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Error handling GitHub payload:", e)
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
