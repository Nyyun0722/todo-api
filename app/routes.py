# app/routes.py
from flask import Blueprint, request, jsonify, g
from .models import db, Todo, User
from functools import wraps

routes_bp = Blueprint('routes', __name__)

# Token-based login_required using Authorization header
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        try:
            user_id = int(auth_header.split(" ")[1])
        except (IndexError, ValueError):
            return jsonify({"error": "Invalid token format"}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 401
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function

@routes_bp.route('/todos', methods=['POST'])
@login_required
def create_todo():
    data = request.get_json()
    todo = Todo(title=data['title'], description=data.get('description', ''), user_id=g.user_id)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@routes_bp.route('/todos', methods=['GET'])
@login_required
def list_todos():
    todos = Todo.query.filter_by(user_id=g.user_id).all()
    return jsonify([t.to_dict() for t in todos])

@routes_bp.route('/todos/<int:todo_id>', methods=['GET'])
@login_required
def get_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=g.user_id).first()
    if not todo:
        return jsonify({"error": "Not found"}), 404
    return jsonify(todo.to_dict())

@routes_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@login_required
def update_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.filter_by(id=todo_id, user_id=g.user_id).first()
    if not todo:
        return jsonify({"error": "Not found"}), 404
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)

    if 'completed' in data:
        todo.completed = data['completed']

    db.session.commit()
    return jsonify(todo.to_dict())

@routes_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=g.user_id).first()
    if not todo:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@routes_bp.route('/todos/<int:todo_id>/complete', methods=['PUT'])
@login_required
def mark_complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=g.user_id).first()
    if not todo:
        return jsonify({"error": "Not found"}), 404
    todo.completed = True
    db.session.commit()
    return jsonify(todo.to_dict())

