from flask import Blueprint, request
from proxy.models import Journal
from proxy.schemas_proxy import JounalSchemas
from flask_apispec import use_kwargs, marshal_with


journal = Blueprint("journal", __name__, url_prefix="/journal")


@journal.route("/get", methods=["GET"])
@marshal_with(JounalSchemas)
def get_today_journal():
    try:
        date = request.args.get("date")
        source_id = request.args.get("source_id")
        jour = Journal.get(date=date, source_id=source_id)
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return jour


@journal.route("/add", methods=["POST"])
@use_kwargs(JounalSchemas)
@marshal_with(JounalSchemas)
def add_journal(**kwargs):
    try:
        jour = Journal(**kwargs)
        jour.save()
    except Exception as e:
        print(e)
        return {"message": str(e)}, 400
    return jour
