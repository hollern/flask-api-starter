from flask import request, send_file, make_response
from flask_jwt_extended import jwt_required
from app.routes.utils import ErrorHandler
from app.routes import blueprint
from app import models

from marshmallow import Schema, fields, validate, post_load, ValidationError


@blueprint.route('/report', methods=['GET'])
def get_single_report():
    try:
        # Get requested data
        data = request.args.to_dict()
        validated_data = ReportGetArgumentsSchema(many=False).load(data)
        # Generate report file
        # ...
        # Send file
        # return send_file()
        return make_response(ReportGetArgumentsSchema().dump(validated_data), 200)
    except ValidationError as e:
        return make_response(*ErrorHandler.custom_error(e.messages, 400))
    except Exception as e:
        return make_response(*ErrorHandler.generic_error)


class ReportGetArgumentsSchema(Schema):
    report_name = fields.String(required=True, validate=validate.OneOf(['test']))
    start_datetime = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%SZ')
    end_datetime = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%SZ')

    @post_load
    def end_datetime_greater_than_start_datetime(self, data, **kwargs):
        if data['end_datetime'] <= data['start_datetime']:
            raise ValidationError('Reporting end datetime must be greater than start datetime.')
        return data
