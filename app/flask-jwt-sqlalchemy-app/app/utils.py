from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from .models import User, ProjectUsers, Task

def is_user_in_project(user_id, project_id):
    return ProjectUsers.query.filter_by(user_id=user_id, project_id=project_id).first() is not None

def visible_to_role(get_task_func):
    @wraps(get_task_func)
    def wrapper(task_id, *args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        task = Task.query.get_or_404(task_id)
        # Project association check (optional, for extra safety)
        if not is_user_in_project(user_id, task.project_id):
            return jsonify({"msg": "User not associated with this project"}), 403
        # Role check
        if task.visible_to_role and user.role != task.visible_to_role:
            return jsonify({"msg": f"Task not visible to your role ({user.role})"}), 403
        return get_task_func(task_id, *args, **kwargs)
    return wrapper