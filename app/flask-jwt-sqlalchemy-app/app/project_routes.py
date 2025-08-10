from flask import Blueprint, request, jsonify
from .models import db, Project, Task, TaskFields, ProjectUsers, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from .schemas import ProjectSchema, TaskSchema, TaskFieldSchema, ProjectUserSchema
from .utils import is_user_in_project, visible_to_role

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    name = data.get('project_name')
    description = data.get('project_description')
    creator_id = get_jwt_identity()  # Get the current user's ID

    # 1. Create the project
    project = Project(project_name=name, project_description=description)
    db.session.add(project)
    db.session.commit()  # Commit to get project

    # 1.1 Add creator to ProjectUsers
    project_user = ProjectUsers(user_id=creator_id, project_id=project.project_id)
    db.session.add(project_user)
    db.session.commit()

    # 2. Create two tasks
    task1 = Task(task_name=f"{name}_Task1", project_id=project.project_id,visible_to_role="maintainer")
    task2 = Task(task_name=f"{name}_Task2", project_id=project.project_id,visible_to_role="reviewer")
    db.session.add_all([task1, task2])
    db.session.commit()  # Commit to get task

    # 3. Add fields for task1 (2 fields)
    tf1 = TaskFields(field_name="Task1_Field1", field_type="text", task_id=task1.task_id, project_id=project.project_id)
    tf2 = TaskFields(field_name="Task1_Field2", field_type="text", task_id=task1.task_id, project_id=project.project_id)
    # Add fields for task2 (3 fields)
    tf3 = TaskFields(field_name="Task2_Field1", field_type="text", task_id=task2.task_id, project_id=project.project_id)
    tf4 = TaskFields(field_name="Task2_Field2", field_type="text", task_id=task2.task_id, project_id=project.project_id)
    tf5 = TaskFields(field_name="Task2_Field3", field_type="text", task_id=task2.task_id, project_id=project.project_id)
    db.session.add_all([tf1, tf2, tf3, tf4, tf5])
    db.session.commit()

    return jsonify({"msg": "Project, tasks, fields, and project user created successfully", "project_id": project.project_id}), 201


@project_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    project_schema = ProjectSchema(many=True)
    return jsonify(project_schema.dump(projects)), 200

@project_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    if not is_user_in_project(user_id, project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    project = Project.query.get_or_404(project_id)
    project_schema = ProjectSchema()
    return jsonify(project_schema.dump(project)), 200


@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    if not is_user_in_project(user_id, project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    project = Project.query.get_or_404(project_id)
    project_schema = ProjectSchema(partial=True)  
    updated_project = project_schema.load(request.json, instance=project)
    updated_project.save()
    return jsonify(project_schema.dump(updated_project)), 200

@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    if not is_user_in_project(user_id, project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    project = Project.query.get_or_404(project_id)
    project.delete()
    return jsonify({'message': 'Project deleted'}), 204
       

@project_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
@visible_to_role
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_schema = TaskSchema()
    task_data = task_schema.dump(task)

    # Add fields info
    fields_list = []
    field_values = {}
    for field in task.fields:
        field_info = {
            "field_id": field.field_id,
            "field_name": field.field_name,
            "field_type": field.field_type,
            "field_value": field.field_value
        }
        fields_list.append(field_info)
        if field.field_value is not None:
            field_values[field.field_name] = field.field_value

    task_data["fields"] = fields_list
    if field_values:
        task_data["field_values"] = field_values

    return jsonify(task_data), 200 

@project_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    task_schema = TaskSchema()
    task = task_schema.load(request.json)
    new_task = Task(**task)
    new_task.save()
    return jsonify(task_schema.dump(new_task)), 201

@project_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@jwt_required()
def get_tasks_for_project(project_id):
    user_id = get_jwt_identity()
    if not is_user_in_project(user_id, project_id):
        return {"msg": "User not associated with this project"}, 403

    user = User.query.get(user_id)
    # Only show tasks visible to the user's role
    tasks = Task.query.filter_by(project_id=project_id, visible_to_role=user.role).all()
    if not tasks:
        return jsonify({"msg": f"No tasks found for your role '{user.role}' in this project."}), 200

    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(tasks)), 200


@project_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_schema = TaskSchema(partial=True)
    updated_task = task_schema.load(request.json, instance=task)
    updated_task.save()
    return jsonify(task_schema.dump(updated_task)), 200

@project_bp.route('/tasks/<int:task_id>/fields', methods=['POST'])
@jwt_required()
def create_task_field(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    # Check project association
    if not is_user_in_project(user_id, task.project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    # Check if user is maintainer
    user = User.query.get(user_id)
    if user.role != "maintainer":
        return jsonify({"msg": "Only maintainers can create task fields"}), 403

    field_schema = TaskFieldSchema()
    field_data = field_schema.load(request.json)
    new_field = TaskFields(**field_data, task_id=task_id, project_id=task.project_id)
    db.session.add(new_field)
    db.session.commit()
    return jsonify(field_schema.dump(new_field)), 201

@project_bp.route('/tasks/<int:task_id>/fields', methods=['GET'])
@jwt_required()
def get_task_fields(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    if not is_user_in_project(user_id, task.project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    

    fields = TaskFields.query.filter_by(task_id=task_id).all()
    field_schema = TaskFieldSchema(many=True)
    return jsonify(field_schema.dump(fields)), 200

@project_bp.route('/tasks/fields/<int:field_id>', methods=['PUT'])
@jwt_required()
def update_task_field(field_id):
    user_id = get_jwt_identity()
    field = TaskFields.query.get_or_404(field_id)
    # Check project association
    if not is_user_in_project(user_id, field.project_id):
        return jsonify({"msg": "User not associated with this project"}), 403
    # Check if user is maintainer
    user = User.query.get(user_id)
    if user.role != "maintainer":
        return jsonify({"msg": "Only maintainers can update task fields"}), 403

    field_schema = TaskFieldSchema(partial=True)
    updated_field = field_schema.load(request.json, instance=field)
    db.session.commit()
    return jsonify(field_schema.dump(updated_field)), 200