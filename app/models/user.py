from werkzeug.security import generate_password_hash, check_password_hash
from app.models.utils import CoreModel, CoreSchema, exceptions
from flask_jwt_extended import create_access_token
from flask import current_app, render_template
from app.services import Mailer
from marshmallow import fields
from app import db
import datetime

from sqlalchemy.dialects.postgresql import UUID


class UserSchema(CoreSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    first_name = fields.String()
    last_name = fields.String()
    is_admin = fields.Boolean()
    is_readonly = fields.Boolean()
    linked_company = fields.UUID(required=True)


class UserChangePasswordSchema(CoreSchema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True)


class User(CoreModel):
    __tablename__ = 'users'
    email = db.Column(db.String(299), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(99))
    last_name = db.Column(db.String(99))
    is_admin = db.Column(db.Boolean, default=False)
    is_readonly = db.Column(db.Boolean, default=False)
    linked_company = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id'), index=True, nullable=True)

    # Relationships
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    # Schemas
    single_schema = UserSchema()
    many_schema = UserSchema(many=True)
    partial_schema = UserSchema(partial=True)
    authentication_schema = UserSchema(partial=('linked_company',))
    change_password_schema = UserChangePasswordSchema()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create(cls, data, commit=True):
        if type(data) is dict:
            data = [data]
        obj_list = []
        for item in data:
            obj = User.from_dict(item)
            db.session.add(obj)
            obj_list.append(obj)
        if commit:
            db.session.commit()
        return obj_list

    @classmethod
    def from_dict(cls, data: dict):
        # Create user from parameters and hash password
        user = cls(**{k: v for k, v in data.items() if k != 'password'})  # unpack parameters w/o password
        user.set_password(data['password'])
        user.save()
        return user

    def issue_access_token(self):
        expires = datetime.timedelta(hours=current_app.config['DEFAULT_TOKEN_EXPIRY'])
        access_token = create_access_token(
            identity=self.id,
            expires_delta=expires,
            user_claims={
                'is_admin': self.is_admin,
                'is_readonly': self.is_readonly,
                'company_id': self.linked_company
            }
        )
        return access_token

    def issue_password_reset_token(self, current_url: str):
        # Create password reset token
        expires = datetime.timedelta(hours=current_app.config['DEFAULT_TOKEN_EXPIRY'])
        reset_token = create_access_token(
            identity=self.id,
            expires_delta=expires
        )
        # Format password reset url with current token
        formatted_url = '{}user/reset_password/{}'.format(current_url, reset_token)  # TODO: this needs to redirect to the front-end i.e., website.com/reset_password which will make a POST request to api/v1/reset_password
        # Send email to user with password reset token
        mail_resp = Mailer.send_mail(
            from_email=current_app.config['SYSTEM_EMAIL'],
            to_emails=[self.email],
            subject='Your password reset token',
            html_content=render_template('emails/password-reset.html', url=formatted_url)
        )
        return mail_resp

    def change_password(self, current_password: str, new_password: str):
        is_valid_password = self.check_password(current_password)
        if is_valid_password:
            self.set_password(new_password)
            self.save()
        else:
            raise exceptions.InvalidPasswordError('User current password is invalid. Password not updated.')
