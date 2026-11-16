from flask import Flask, request, jsonify
from repositories.user_repository import UserRepository
from routes.conflict_routes import conflict_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(conflict_bp)
    repo = UserRepository()

    @app.get("/")
    def home():
        return jsonify({"app": "StudentSync", "status": "running"})

    # Create a new user
    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()

        full_name = data["full_name"]
        email = data["email"]

        user = repo.create_user(full_name, email)

        return jsonify({
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email
        })

    # Find a user by ID
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = repo.find_by_id(user_id)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email
        })

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
