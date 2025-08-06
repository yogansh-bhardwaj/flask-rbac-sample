from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

class ProjectUserSchema(Schema):
    project_user_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    project_id = fields.Int(required=True)
    user = fields.Nested(UserSchema, only=['id', 'email'])
    project = fields.Nested('ProjectSchema', only=['id', 'name'])

class ProjectSchema(Schema):
    project_id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True)
    project_description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True)
    description = fields.Str(required=True)
    task_id = fields.Int(required=True)
    project_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TaskFieldSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    value = fields.Str(required=True)
    task_id = fields.Int(required=True)
    project_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)