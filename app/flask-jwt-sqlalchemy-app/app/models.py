from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64),nullable = True)

    def __repr__(self):
        return f'<User {self.username}>'


class ProjectUsers(db.Model):
    project_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('project_users', lazy=True))
    project = db.relationship('Project', backref=db.backref('project_users', lazy=True))
    
    def __repr__(self):
        return f'<ProjectUser {self.user.email} in {self.project.project_name}>'


class Project(db.Model):
    project_id = db.Column(db.Integer,primary_key=True)
    project_name = db.Column(db.String(120), nullable=False)
    project_description = db.Column(db.String(500), nullable=True)


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(120), nullable=False)
    task_description = db.Column(db.String(500), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    visible_to_role = db.Column(db.String(64), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('tasks', lazy=True))
    
    def __repr__(self):
        return f'<Task {self.task_name}>'


class TaskFields(db.Model):
    field_id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(120), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)
    field_value = db.Column(db.String(500), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('fields', lazy=True))
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('project_fields', lazy=True))

    def __repr__(self):
        return f'<TaskField {self.field_name}>'