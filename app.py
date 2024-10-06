from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for parts
class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partNumber = db.Column(db.String(50), nullable=False)
    partName = db.Column(db.String(100), nullable=False)
    oemNumber = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    minStock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.String(200), nullable=True)

# Create the database and the table
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/api/parts', methods=['GET'])
def get_parts():
    parts = Part.query.all()
    result = []
    for part in parts:
        result.append({
            'id': part.id,
            'partNumber': part.partNumber,
            'partName': part.partName,
            'oemNumber': part.oemNumber,
            'description': part.description,
            'manufacturer': part.manufacturer,
            'quantity': part.quantity,
            'minStock': part.minStock,
            'price': part.price,
            'location': part.location,
            'notes': part.notes
        })
    return jsonify(result)

@app.route('/api/parts', methods=['POST'])
def add_part():
    data = request.json
    new_part = Part(
        partNumber=data['partNumber'],
        partName=data['partName'],
        oemNumber=data['oemNumber'],
        description=data.get('description', ''),
        manufacturer=data.get('manufacturer', ''),
        quantity=data['quantity'],
        minStock=data['minStock'],
        price=data['price'],
        location=data.get('location', ''),
        notes=data.get('notes', '')
    )
    db.session.add(new_part)
    db.session.commit()
    return jsonify({'id': new_part.id}), 201

@app.route('/api/parts/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = Part.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)