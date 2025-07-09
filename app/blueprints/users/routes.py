from marshmallow import ValidationError
from sqlalchemy import select
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from app.blueprints.users import user_bp
from app.blueprints.users.schemas import user_schema, return_user_schema, return_users_schema
from app.models import db, User
from app.utils.auth import check_password, generate_token, hash_password, token_required

@user_bp.route("/login", methods=["POST"])
def login():
  try:
    data = request.get_json()
    
    if not data or not data.get("email") or not data.get("password"):
      return jsonify({"message": "Email and password are required"}), 400
    
    user = db.session.scalar(select(User).filter_by(email=data["email"]))
    
    if not user or not check_password(data["password"], user.password):
      return jsonify({"message": "Invalid email or password"}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
      "status": "success",
      "message": "Login successfull",
      "token": token,
      "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email
      }
    }), 200
    
  except Exception as e:
    return jsonify({"message": "Internal server error", "details": str(e)}), 500

@user_bp.route("/", methods=["POST"])
def create_user():
  try:
    user_data = user_schema.load(request.json)
    user_data.password = hash_password(user_data.password)
    db.session.add(user_data)
    db.session.commit()
    return jsonify(return_user_schema.dump(user_data)), 201
  except ValidationError as e:
    return jsonify(e.messages), 400
  except IntegrityError as e:
    db.session.rollback()
    
    if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
      return jsonify({"error": "Email already registered"}), 409
    
    return jsonify({"error": "Database error"}), 500

@user_bp.route("/", methods=["GET"])
def get_users():
  users = db.session.scalars(select(User)).all()
  if not users:
    return jsonify({"message": "No users found"}), 404
  return jsonify(return_users_schema.dump(users)), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
  user = db.session.scalars(select(User).where(User.id == user_id)).first()
  if not user:
    return jsonify({"message": "User not found"}), 404
  return jsonify(return_user_schema.dump(user)), 200