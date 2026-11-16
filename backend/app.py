from flask import Flask, jsonify

from routes.user_routes import user_bp
from routes.academic_routes import academic_bp
from routes.work_routes import work_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_bp)
    app.register_blueprint(academic_bp)
    app.register_blueprint(work_bp)

    @app.errorhandler(ValueError)
    def invalid_data(error):
        return jsonify({"error": str(error)}), 400

    @app.get("/")
    def home():
        return jsonify({
            "app": "StudentSync",
            "status": "running"
        })

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
