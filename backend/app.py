from flask import Flask, jsonify, request
from flask_cors import CORS
from game import PongGame

app = Flask(__name__)
CORS(app)
game = PongGame()

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(game.state())

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    game.move_paddle(data["player"], data["direction"])
    return jsonify(game.state())

@app.route("/update", methods=["POST"])
def update():
    return jsonify(game.update())

@app.route("/reset", methods=["POST"])
def reset():
    game.reset()
    return jsonify(game.state())

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(port=5000, debug=debug_mode)