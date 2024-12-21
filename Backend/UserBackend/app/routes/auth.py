from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import db
from app.models.user import User
from flask_bcrypt import Bcrypt

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Create new user
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password,
            phone_number=data.get("phone_number"),
            address=data.get("address"),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id)
            return (
                jsonify(
                    {
                        "access_token": access_token,
                        "user_id": user.id,
                        "name": user.name,
                    }
                ),
                200,
            )

        return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 400
