from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import User, Project, Task, TaskFields, ProjectUsers
from .schemas import UserSchema, ProjectSchema, TaskSchema, TaskFieldSchema, ProjectUserSchema

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200

@routes_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200

@routes_bp.route('/users', methods=['POST'])
def create_user():
    user_schema = UserSchema()
    user = user_schema.load(request.json)
    new_user = User(**user)
    new_user.save()
    return jsonify(user_schema.dump(new_user)), 201

@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user_schema = UserSchema(partial=True)  # Allow partial updates
    updated_user = user_schema.load(request.json, instance=user)
    updated_user.save()
    return jsonify(user_schema.dump(updated_user)), 200

@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.delete()
    return jsonify({'message': 'User deleted'}), 204


