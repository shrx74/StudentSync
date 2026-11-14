from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def home():
        return jsonify({"app": "StudentSync", "status": "running"})

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
