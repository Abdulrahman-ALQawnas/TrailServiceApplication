from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

# Initialize Flask app and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://AAlqawnas:EnwQ975+@@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_AAlqawnas' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Authenticator API endpoint
AUTHENTICATOR_API = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Models
class Author(db.Model):
    __tablename__ = 'Author'
    authorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Trail(db.Model):
    __tablename__ = 'Trail'
    trailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(500), nullable=True)
    distance = db.Column(db.Float, nullable=True)
    complexity = db.Column(db.String(50), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    authorID = db.Column(db.Integer, db.ForeignKey('Author.authorID'), nullable=False)

class Waypoint(db.Model):
    __tablename__ = 'Waypoint'
    waypointID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailID = db.Column(db.Integer, db.ForeignKey('Trail.trailID'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class TrailLog(db.Model):
    __tablename__ = 'TrailLog'
    logID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trailID = db.Column(db.Integer, db.ForeignKey('Trail.trailID'), nullable=False)
    authorID = db.Column(db.Integer, db.ForeignKey('Author.authorID'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Authentication Helper
def authenticate_user(email, password):
    """Authenticate user via the external Authenticator API."""
    response = requests.post(AUTHENTICATOR_API, json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()
    return None

# API Endpoints
@app.route('/trails', methods=['GET'])
def get_trails():
    """Fetch all trails or filter by specific criteria."""
    trails = Trail.query.all()
    result = [
        {
            "trailID": trail.trailID,
            "title": trail.title,
            "overview": trail.overview,
            "distance": trail.distance,
            "complexity": trail.complexity,
            "dateCreated": trail.dateCreated,
            "authorID": trail.authorID,
        } for trail in trails
    ]
    return jsonify(result), 200

@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    """Fetch details of a specific trail by ID."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"message": "Trail not found"}, 404
    return jsonify({
        "trailID": trail.trailID,
        "title": trail.title,
        "overview": trail.overview,
        "distance": trail.distance,
        "complexity": trail.complexity,
        "dateCreated": trail.dateCreated,
        "authorID": trail.authorID,
    }), 200

@app.route('/trails', methods=['POST'])
def create_trail():
    """Create a new trail."""
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if not user:
        return {"message": "Authentication failed"}, 401

    new_trail = Trail(
        title=data['title'],
        overview=data.get('overview', ''),
        distance=data.get('distance', 0.0),
        complexity=data['complexity'],
        authorID=user['userID']
    )
    db.session.add(new_trail)
    db.session.commit()
    return {"message": "Trail created", "trailID": new_trail.trailID}, 201

@app.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    """Update an existing trail."""
    data = request.get_json()
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"message": "Trail not found"}, 404

    trail.title = data.get('title', trail.title)
    trail.overview = data.get('overview', trail.overview)
    trail.distance = data.get('distance', trail.distance)
    trail.complexity = data.get('complexity', trail.complexity)
    db.session.commit()
    return {"message": "Trail updated successfully"}, 200

@app.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    """Delete a trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"message": "Trail not found"}, 404
    db.session.delete(trail)
    db.session.commit()
    return {"message": "Trail deleted successfully"}, 200

@app.route('/waypoints/<int:trail_id>', methods=['GET'])
def get_waypoints(trail_id):
    """Fetch waypoints for a specific trail."""
    waypoints = Waypoint.query.filter_by(trailID=trail_id).all()
    result = [
        {
            "waypointID": waypoint.waypointID,
            "latitude": waypoint.latitude,
            "longitude": waypoint.longitude,
        } for waypoint in waypoints
    ]
    return jsonify(result), 200

# Main entry point
if __name__ == '__main__':
    db.create_all()  # Ensure all tables are created in the database
    app.run(debug=True, host='0.0.0.0', port=5000)

