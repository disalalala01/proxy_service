from marshmallow import Schema, validate, fields


class SourceSchemas(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=256)])
    url = fields.String(required=True, validate=[validate.Length(max=500)])
    message = fields.String(dump_only=True)


class ProxySchemas(Schema):
    id = fields.Integer(dump_only=True)
    ip = fields.String(required=True, validate=[validate.Length(max=256)])
    message = fields.String(dump_only=True)


class MonitoringSchemas(Schema):
    id = fields.Integer(load_only=True)
    city = fields.String(validate=[validate.Length(max=256)])
    shop_name = fields.String(required=True, validate=[validate.Length(max=256)])
    shop_type = fields.String(required=True, validate=[validate.Length(max=256)])
    shop_category = fields.String(required=True, validate=[validate.Length(max=256)])
    provider = fields.String(required=True, validate=[validate.Length(max=256)])
    product_name = fields.String(required=True, validate=[validate.Length(max=256)])
    product_unit = fields.String(required=True, validate=[validate.Length(max=256)])
    package = fields.String(required=True, validate=[validate.Length(max=256)])
    thermal_state = fields.String(required=True, validate=[validate.Length(max=256)])
    product_price = fields.Float()
    stationary_view = fields.String(required=True, validate=[validate.Length(max=256)])
    composition = fields.String(required=True, validate=[validate.Length(max=256)])
    channel = fields.String(required=True, validate=[validate.Length(max=256)])
    source_id = fields.Integer(required=True, load_only=True)
    message = fields.String(dump_only=True)


class JounalSchemas(Schema):
    id = fields.Integer(dump_only=True)
    created = fields.String(required=True, validate=[validate.Length(max=256)])
    source_id = fields.String(required=True, validate=[validate.Length(max=256)])
    status = fields.String(required=True, validate=[validate.Length(max=5)])
    message = fields.String(dump_only=True)
