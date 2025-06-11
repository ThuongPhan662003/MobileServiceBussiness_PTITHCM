from flask import Blueprint, request, jsonify, render_template
from app.services.subscriber_service import SubscriberService
from flask_login import login_required
from app.utils.decorator import required


subscriber_bp = Blueprint("subscriber_bp", __name__, url_prefix="/subscribers")


@login_required
@subscriber_bp.route("/", methods=["GET"])
@required
def get_all_subscribers():
    subscribers = SubscriberService.get_all_subscribers()
    return render_template("admin_home/subscribers.html", subscribers=subscribers)


@login_required
@subscriber_bp.route("/<int:subscriber_id>", methods=["GET"])
@required
def get_subscriber(subscriber_id):
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    if subscriber:
        return jsonify(subscriber.to_dict()), 200
    return jsonify({"error": "Subscriber not found"}), 404


@login_required
@subscriber_bp.route("/", methods=["POST"])
@required
def create_subscriber():
    data = request.get_json()
    print("Received data:", data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    result = SubscriberService.create_subscriber(data)
    if result.get("success"):
        return jsonify({"message": "Subscriber created successfully"}), 201
    return jsonify({"error": result.get("error", "Unknown error")}), 400


@login_required
@subscriber_bp.route("/<int:subscriber_id>", methods=["PUT"])
@required
def update_subscriber(subscriber_id):
    data = request.get_json()
    result = SubscriberService.update_subscriber(subscriber_id, data)
    if result.get("success"):
        return jsonify({"message": "Subscriber updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@subscriber_bp.route("/<int:subscriber_id>", methods=["DELETE"])
@required
def delete_subscriber(subscriber_id):
    result = SubscriberService.delete_subscriber(subscriber_id)
    if result.get("success"):
        return jsonify({"message": "Subscriber deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
