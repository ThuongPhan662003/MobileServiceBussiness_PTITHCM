function showNotification(message, isSuccess = true) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${isSuccess ? 'bg-green-500' : 'bg-red-500'} text-white px-4 py-2 rounded shadow-lg transition-opacity duration-500`;
    notification.textContent = message;
    notification.setAttribute('role', 'alert');
    document.body.appendChild(notification);
  
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 500);
    }, 3000);
  }
  
  async function changePlan(subscriptionId, buttonElement) {
    if (!confirm('Bạn có chắc muốn đổi gói cước này không?')) return;
  
    try {
      const response = await fetch(`/subscriptions/${subscriptionId}/change`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
        }
      });
  
      const data = await response.json();
  
      if (data.success) {
        buttonElement.textContent = 'Đã đổi';
        buttonElement.classList.remove('text-red-600', 'hover:underline');
        buttonElement.classList.add('text-gray-500', 'cursor-not-allowed');
        buttonElement.disabled = true;
        showNotification(data.message || 'Đổi gói cước thành công!', true);
      } else {
        showNotification(data.message || 'Đổi gói cước thất bại!', false);
      }
    } catch (error) {
      console.error('Error:', error);
      showNotification('Đã xảy ra lỗi khi kết nối server.', false);
    }
  }