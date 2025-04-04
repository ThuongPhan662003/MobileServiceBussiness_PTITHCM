from flask import Blueprint, request, jsonify
from app.services.subscription_service import SubscriptionService

subscription_bp = Blueprint("subscription", __name__, url_prefix="/subscriptions")


@subscription_bp.route("/", methods=["GET"])
def get_all_subscriptions():
    subscriptions = SubscriptionService.get_all_subscriptions()
    return jsonify(subscriptions), 200


@subscription_bp.route("/<int:subscription_id>", methods=["GET"])
def get_subscription_by_id(subscription_id):
    subscription = SubscriptionService.get_subscription_by_id(subscription_id)
    if subscription:
        return jsonify(subscription.to_dict()), 200
    return jsonify({"error": "Subscription not found"}), 404


@subscription_bp.route("/", methods=["POST"])
def create_subscription():
    data = request.get_json()
    result = SubscriptionService.create_subscription(data)
    if result.get("success"):
        return jsonify({"message": "Subscription created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@subscription_bp.route("/<int:subscription_id>", methods=["PUT"])
def update_subscription(subscription_id):
    data = request.get_json()
    result = SubscriptionService.update_subscription(subscription_id, data)
    if result.get("success"):
        return jsonify({"message": "Subscription updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@subscription_bp.route("/<int:subscription_id>", methods=["DELETE"])
def delete_subscription(subscription_id):
    result = SubscriptionService.delete_subscription(subscription_id)
    if result.get("success"):
        return jsonify({"message": "Subscription deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
