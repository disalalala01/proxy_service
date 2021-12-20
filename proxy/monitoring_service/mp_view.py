from flask import Blueprint, request
from proxy.models import MonitoringPrice
from proxy.schemas_proxy import MonitoringSchemas
from flask_apispec import use_kwargs, marshal_with


mp = Blueprint("monitoring", __name__, url_prefix="/mp")


@mp.route("/add", methods=["POST"])
@use_kwargs(MonitoringSchemas)
@marshal_with(MonitoringSchemas)
def add_mp(**kwargs):
    try:
        mp_obj = MonitoringPrice(**kwargs)
        mp_obj.save()
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return mp_obj


@mp.route("/get", methods=["GET"])
@marshal_with(MonitoringSchemas)
def get_mp():
    try:
        source_id = request.args.get("source_id")
        mp_obj = MonitoringPrice.get(source_id=source_id)
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return mp_obj
