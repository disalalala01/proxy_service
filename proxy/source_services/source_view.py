from flask import Blueprint
from proxy.models import Source
from proxy.schemas_proxy import SourceSchemas
from flask_apispec import use_kwargs, marshal_with


sources = Blueprint("sources", __name__, url_prefix="/source")


@sources.route("/add", methods=["POST"])
@use_kwargs(SourceSchemas)
@marshal_with(SourceSchemas)
def add_source(**kwargs):
    try:
        source_obj = Source(**kwargs)
        source_obj.save()
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return source_obj


@sources.route("/get_list", methods=["GET"])
@marshal_with(SourceSchemas(many=True))
def get_list():
    try:
        source = Source.get_list()
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return source
