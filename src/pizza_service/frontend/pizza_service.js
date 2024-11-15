// Make additional request to get order_bonus
function getOrderBonus() {
	document.getElementById('see-order-button').addEventListener('click', function () {
	const orderId = document.getElementById('order-id-input').value;
	htmx.ajax('GET', `http://0.0.0.0:8000/order_bonus/${orderId}`, {
		target: '#response-see-bonus-container'
		});
	});
}

getOrderBonus()
