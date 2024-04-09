from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import jwt
from datetime import datetime, timedelta



app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secretkey'

DB_URI = 'postgresql://avnadmin:AVNS_PWrbvZPiqMp8rihRXrX@wordle-app-sriharsha07.a.aivencloud.com:13443/defaultdb?sslmode=require'  # Update with your database credentials
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

# Create database tables
Base.metadata.create_all(engine)

# Load a list of words from a file or define it directly
words = ["crane", "lives", "brink", "sight", "grape", "stage", "about", "flock"]
daily_word = random.choice(words).upper()
print(daily_word)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"error": "Invalid credentials."}), 401

    token = jwt.encode({
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time (1 day)
    }, app.config['SECRET_KEY'])

    return jsonify({"token": token}), 200

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if not username or not password or not email or not firstname or not lastname:
        return jsonify({"error": "All fields are required."}), 400

    session = Session()

    # Check if the username or email already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists."}), 400

    existing_email = session.query(User).filter_by(email=email).first()
    if existing_email:
        return jsonify({"error": "Email already exists."}), 400

    # Create a new user
    new_user = User(username=username, password=password, email=email, firstname=firstname, lastname=lastname)
    session.add(new_user)
    session.commit()

    return jsonify({"message": "User created successfully."}), 201

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.get_json()
    print(data)
    guess = data['guess'].upper()
    
    if len(guess) != 5:
        return jsonify({"error": "Each guess must be exactly 5 letters."}), 400
    
    result = []
    for i, letter in enumerate(guess):
        if letter == daily_word[i]:
            result.append('correct')
        elif letter in daily_word:
            result.append('present')
        else:
            result.append('absent')
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
