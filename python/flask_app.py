"""
Flask Application Template

Basic structure for a Flask web application.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint to fetch data."""
    data = {
        'message': 'Hello from the API',
        'status': 'success'
    }
    return jsonify(data)


@app.route('/api/data', methods=['POST'])
def post_data():
    """API endpoint to receive data."""
    received_data = request.get_json()
    # Process the data
    return jsonify({
        'message': 'Data received',
        'received': received_data
    }), 201


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
