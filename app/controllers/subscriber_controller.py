from flask import Blueprint, request, jsonify, render_template
from app.services.subscriber_service import SubscriberService

subscriber_bp = Blueprint('subscriber_bp', __name__, url_prefix='/subscribers')

@subscriber_bp.route('/', methods=['GET'])
def get_all_subscribers():
    subscribers = SubscriberService.get_all_subscribers()
    return render_template("admin_home/subscribers.html", subscribers=subscribers)

@subscriber_bp.route('/<int:subscriber_id>', methods=['GET'])
def get_subscriber(subscriber_id):
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    if subscriber:
        return jsonify(subscriber.to_dict()), 200
    return jsonify({"error": "Subscriber not found"}), 404


@subscriber_bp.route('/', methods=['POST'])
def create_subscriber():
    try:
        data = request.get_json()
        result = SubscriberService.create_subscriber(data)
        if result.get('success'):
            return jsonify({'success': True, 'message': 'Thêm thuê bao thành công!'}), 201
        else:
            return jsonify({'success': False, 'message': result.get('message', 'Lỗi không xác định')}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Đã xảy ra lỗi: {str(e)}'}), 500

@subscriber_bp.route('/<int:subscriber_id>', methods=['PUT'])
def update_subscriber(subscriber_id):
    data = request.get_json()
    result = SubscriberService.update_subscriber(subscriber_id, data)
    if result.get("success"):
        return jsonify({"message": "Subscriber updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400

@subscriber_bp.route('/<int:subscriber_id>', methods=['DELETE'])
def delete_subscriber(subscriber_id):
    result = SubscriberService.delete_subscriber(subscriber_id)
    if result.get("success"):
        return jsonify({"message": "Subscriber deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
