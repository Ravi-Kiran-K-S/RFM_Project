import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from models import Session, Users
from werkzeug.security import check_password_hash, generate_password_hash

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Get JWT secret from environment variable
jwt_secret = os.getenv("JWT_SECRET_KEY")
if not jwt_secret:
    raise ValueError("JWT_SECRET_KEY environment variable is not set. Please configure it properly.")

app.config["JWT_SECRET_KEY"] = jwt_secret

jwt = JWTManager(app)

# Configure CORS with allowed origins from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:80")
CORS(app, origins=cors_origins.split(","), supports_credentials=True)


@app.route("/api/users")
@jwt_required()
def list_users():
    session = Session()
    try:
        current_user_id = get_jwt_identity()
        users = session.query(Users).all()

        users_list = [{"id": u.id, "email": u.email} for u in users]

        return jsonify(users_list)

    finally:
        session.close()


@app.route("/api/signup", methods=["POST"])
def signup():
    session = Session()
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user_exists = session.query(Users).filter_by(email=email).first() is not None
        if user_exists:
            return jsonify({"message": "Email already exists"})
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )

        new_user = Users(email=email, password=hashed_password)
        session.add(new_user)
        session.commit()

        return jsonify({"message": "Successfully created"}), 201

    except Exception as e:
        print(f"SOMETHING WENT WRONG: {e}")
        session.rollback()
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


@app.route("/api/login", methods=["POST"])
def login():
    session = Session()
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = session.query(Users).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Please check your login details and try again"})
        else:
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"message": "Logged in successfuly", "token": access_token})
    except Exception as e:
        print(f"SOMETHING WENT WRONG: {e}")
    finally:
        session.close()


app.run()
