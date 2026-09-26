import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from game import PongGame

app = Flask(__name__)
CORS(app)
game = PongGame()

limiter = Limiter(get_remote_address, app=app, default_limits=["30 per second"])

API_KEY = os.environ.get("GAME_API_KEY", "dev-secret-key")

def check_auth():
    return request.headers.get("X-API-KEY") == API_KEY

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(game.state())

@app.route("/move", methods=["POST"])
@limiter.limit("10 per second")
def move():
    if not check_auth():
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    player = data.get("player")
    direction = data.get("direction")
    if player not in (1, 2) or direction not in ("up", "down"):
        return jsonify({"error": "invalid input"}), 400
    game.move_paddle(player, direction)
    return jsonify(game.state())

@app.route("/update", methods=["POST"])
@limiter.limit("15 per second")
def update():
    return jsonify(game.update())

@app.route("/reset", methods=["POST"])
@limiter.limit("1 per second")
def reset():
    if not check_auth():
        return jsonify({"error": "unauthorized"}), 401
    game.reset()
    return jsonify(game.state())

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(port=5000, debug=debug_mode)