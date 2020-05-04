from app.routes.utils import exceptions
from marshmallow import Schema, ValidationError, fields, validate, pre_load
from flask import request
import json


class QueryBuilder:
    def __init__(self, model, user):
        self.model = model
        self.user = user
        self.data = request.data
        self.params = json.loads(self.data).get('query')

        if self.params is None:
            raise exceptions.QueryBuilderError('GET many request parameters can not be empty.')

        self.params = RequestDataSchema(many=False).load(self.params)

        pagination = self.params.get('pagination')
        self.page = pagination.get('page')
        self.limit = pagination.get('limit')

    def get_data(self):
        base_query = self.model.query
        current_tenant_query = self._filter_for_database_tenant(base_query)
        filtered_query = self._apply_filter_fields(current_tenant_query)
        sorted_query = self._apply_sort_fields(filtered_query)
        paginated = sorted_query.paginate(self.page, self.limit, False)
        return paginated.items, paginated.total

    def _apply_filter_fields(self, query):
        filter_fields = self.params.get('filter_fields')
        if filter_fields is not None:
            for filtr in filter_fields:
                try:
                    field = getattr(self.model, filtr['field'])
                except Exception:
                    raise exceptions.QueryBuilderError('Entity has no field: "{}"'.format(filtr['field']))
                filter_type = filtr['filter_type']
                value = filtr['value']
                if filter_type == 'eq':
                    query = query.filter(field == value)
                elif filter_type == 'lt':
                    query = query.filter(field < value)
                elif filter_type == 'gt':
                    query = query.filter(field > value)
                elif filter_type == 'lte':
                    query = query.filter(field <= value)
                elif filter_type == 'gte':
                    query = query.filter(field >= value)
                elif filter_type == 'not':
                    query = query.filter(field != value)
                elif filter_type == 'in':
                    value = tuple(value.split('|||'))
                    query = query.filter(field.in_(value))
                elif filter_type == 'like':
                    query = query.filter(field.like(value))
        return query

    def _apply_sort_fields(self, query):
        sort_fields = self.params.get('sort_fields')
        if sort_fields is not None:
            for sort in sort_fields:
                try:
                    field = getattr(self.model, sort['field'])
                except Exception:
                    raise exceptions.QueryBuilderError('Entity has no field: "{}"'.format(sort['field']))
                if sort['descending'] is True:
                    query = query.order_by(field.desc())
                else:
                    query = query.order_by(field)
        return query

    def _filter_for_database_tenant(self, query):
        return query.filter_by(database_tenant_id=self.user.database_tenant_id)


class _FilterFieldSchema(Schema):
    field = fields.String(required=True)
    filter_type = fields.String(required=True, validate=validate.OneOf(['eq', 'lt', 'gt', 'lte', 'gte', 'not', 'in', 'like']))
    value = fields.String(required=True)

    @pre_load
    def convert_value_from_list(self, data, **kwargs):
        if data.get('filter_type') == 'in':
            if type(data.get('value')) is list:
                data['value'] = '|||'.join(data['value'])
            else:
                raise ValidationError('"value" must be list like when using "in" filter_type')
        return data


class _SortFieldSchema(Schema):
    field = fields.String(required=True)
    descending = fields.Boolean(required=True)


class _PaginationSchema(Schema):
    page = fields.Integer(required=True, validate=validate.Range(min=0))
    limit = fields.Integer(required=True, validate=validate.Range(min=1, max=100))


class RequestDataSchema(Schema):
    filter_fields = fields.List(fields.Nested(_FilterFieldSchema), required=False)
    sort_fields = fields.List(fields.Nested(_SortFieldSchema), required=False)
    pagination = fields.Nested(_PaginationSchema, required=True)
