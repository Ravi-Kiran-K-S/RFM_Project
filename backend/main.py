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

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = (
    "c8fb1ec1e192976c1c9fa5aa5e31c911649e6d1e031447ad3596fb5bcaf06739"
)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)


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
