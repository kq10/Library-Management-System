from flask_restful import Resource, Api, reqparse, marshal_with, fields
from application.models import db, User, Section, Ebook, Request, Feedback, Role
from application.sec import datastore

api = Api(prefix='/api')

# Request Parsers
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='Username is required', required=True)
user_parser.add_argument('password_hash', type=str, help='Password is required', required=True)
user_parser.add_argument('role', type=str, help='Role is required', required=True)
user_parser.add_argument('active', type=bool, help='Active status is required', required=True)

section_parser = reqparse.RequestParser()
section_parser.add_argument('name', type=str, help='Name is required', required=True)

ebook_parser = reqparse.RequestParser()
ebook_parser.add_argument('title', type=str, help='Title is required', required=True)
ebook_parser.add_argument('author', type=str, help='Author is required', required=True)
ebook_parser.add_argument('content', type=str, help='Content is required', required=True)
ebook_parser.add_argument('section_id', type=int, help='Section ID is required', required=True)

request_parser = reqparse.RequestParser()
request_parser.add_argument('user_id', type=int, help='User ID is required', required=True)
request_parser.add_argument('ebook_id', type=int, help='Ebook ID is required', required=True)
request_parser.add_argument('status', type=str, help='Status is required', required=True)
request_parser.add_argument('feedback', type=str, help='Feedback is optional')

feedback_parser = reqparse.RequestParser()
feedback_parser.add_argument('user_id', type=int, help='User ID is required', required=True)
feedback_parser.add_argument('ebook_id', type=int, help='Ebook ID is required', required=True)
feedback_parser.add_argument('rating', type=int, help='Rating is required', required=True)
feedback_parser.add_argument('comment', type=str, help='Comment is optional')

# Fields for marshalling
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'role': fields.String,
    'active': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

ebook_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'content': fields.String,
    'section_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

request_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'ebook_id': fields.Integer,
    'status': fields.String,
    'request_date': fields.DateTime,
    'grant_date': fields.DateTime,
    'return_date': fields.DateTime,
    'feedback': fields.String
}

feedback_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'ebook_id': fields.Integer,
    'rating': fields.Integer,
    'comment': fields.String,
    'created_at': fields.DateTime
}

# Resource Classes
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        all_users = User.query.all()
        if len(all_users) > 0:
            return all_users
        return {"message": "No Users"}, 404

    def post(self):
        args = user_parser.parse_args()
        role = Role.query.filter_by(name=args['role']).first()
        if not role:
            return {"message": "Role not found"}, 404

        new_user = User(
            username=args['username'],
            password_hash=args['password_hash'],
            role_id=role.id,
            active=args['active']
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

class SectionResource(Resource):
    @marshal_with(section_fields)
    def get(self):
        all_sections = Section.query.all()
        if len(all_sections) > 0:
            return all_sections
        return {"message": "No Sections"}, 404

    def post(self):
        args = section_parser.parse_args()
        new_section = Section(name=args['name'])
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201

class EbookResource(Resource):
    @marshal_with(ebook_fields)
    def get(self):
        all_ebooks = Ebook.query.all()
        if len(all_ebooks) > 0:
            return all_ebooks
        return {"message": "No E-books"}, 404

    def post(self):
        args = ebook_parser.parse_args()
        new_ebook = Ebook(
            title=args['title'],
            author=args['author'],
            content=args['content'],
            section_id=args['section_id']
        )
        db.session.add(new_ebook)
        db.session.commit()
        return {"message": "E-book created successfully"}, 201

class RequestResource(Resource):
    @marshal_with(request_fields)
    def get(self):
        all_requests = Request.query.all()
        if len(all_requests) > 0:
            return all_requests
        return {"message": "No Requests"}, 404

    def post(self):
        args = request_parser.parse_args()
        new_request = Request(
            user_id=args['user_id'],
            ebook_id=args['ebook_id'],
            status=args['status'],
            feedback=args.get('feedback')
        )
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Request created successfully"}, 201

class FeedbackResource(Resource):
    @marshal_with(feedback_fields)
    def get(self):
        all_feedbacks = Feedback.query.all()
        if len(all_feedbacks) > 0:
            return all_feedbacks
        return {"message": "No Feedback"}, 404

    def post(self):
        args = feedback_parser.parse_args()
        new_feedback = Feedback(
            user_id=args['user_id'],
            ebook_id=args['ebook_id'],
            rating=args['rating'],
            comment=args.get('comment')
        )
        db.session.add(new_feedback)
        db.session.commit()
        return {"message": "Feedback added successfully"}, 201

# Adding resources to the API
api.add_resource(UserResource, '/users')
api.add_resource(SectionResource, '/sections')
api.add_resource(EbookResource, '/ebooks')
api.add_resource(RequestResource, '/requests')
api.add_resource(FeedbackResource, '/feedback')
