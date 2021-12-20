from flask import Blueprint, request, jsonify
from proxy.models import SourceProxy, Proxy
from proxy.schemas_proxy import ProxySchemas
from flask_apispec import use_kwargs, marshal_with


proxies = Blueprint("proxies", __name__, url_prefix="/proxy")


@proxies.route("/get", methods=["GET"])
def get_proxy():
    try:
        source_id = request.args.get("id")
        return jsonify(SourceProxy.get(source_id=source_id)), 200
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400


@proxies.route("/get_list", methods=["GET"])
@marshal_with(ProxySchemas(many=True))
def get_list():
    try:
        proxy = Proxy.get_list()
        return proxy
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400


@proxies.route("/add", methods=["POST"])
@use_kwargs(ProxySchemas)
@marshal_with(ProxySchemas)
def add_source(**kwargs):
    try:
        source_obj = Proxy(**kwargs)
        source_obj.save()
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return source_obj
