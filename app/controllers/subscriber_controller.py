from flask import Blueprint, request, jsonify
from app.services.subscriber_service import SubscriberService

subscriber_bp = Blueprint("subscriber", __name__, url_prefix="/subscribers")


@subscriber_bp.route("/", methods=["GET"])
def get_all_subscribers():
    subscribers = SubscriberService.get_all_subscribers()
    return jsonify(subscribers), 200


@subscriber_bp.route("/<int:subscriber_id>", methods=["GET"])
def get_subscriber_by_id(subscriber_id):
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    if subscriber:
        return jsonify(subscriber.to_dict()), 200
    return jsonify({"error": "Subscriber not found"}), 404


@subscriber_bp.route("/", methods=["POST"])
def create_subscriber():
    data = request.get_json()
    result = SubscriberService.create_subscriber(data)
    if result.get("success"):
        return jsonify({"message": "Subscriber created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@subscriber_bp.route("/<int:subscriber_id>", methods=["PUT"])
def update_subscriber(subscriber_id):
    data = request.get_json()
    result = SubscriberService.update_subscriber(subscriber_id, data)
    if result.get("success"):
        return jsonify({"message": "Subscriber updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@subscriber_bp.route("/<int:subscriber_id>", methods=["DELETE"])
def delete_subscriber(subscriber_id):
    result = SubscriberService.delete_subscriber(subscriber_id)
    if result.get("success"):
        return jsonify({"message": "Subscriber deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
