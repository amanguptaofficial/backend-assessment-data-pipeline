from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))

def load_customers():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')
    with open(json_path, 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = load_customers()
    
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    paginated_customers = customers[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_customers,
        "total": len(customers),
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    customers = load_customers()
    
    for customer in customers:
        if customer['customer_id'] == customer_id:
            return jsonify(customer)
    
    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
