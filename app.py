from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def getArg():
  return jsonify({
    "yourJSON": request.json
  })

if __name__ == "__main__":
  app.run(debug=True, port=8080)
