from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from biblical_symbols import populate_database, BIBLICAL_SYMBOLS
from vision_analyzer import VisionAnalyzer
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration
if os.environ.get('RENDER'):
    # Use PostgreSQL on Render.com
    database_url = os.environ.get('DATABASE_URL', '')
    if database_url:
        database_url = database_url.replace('postgres://', 'postgresql://')
        logger.info(f"Using PostgreSQL database: {database_url.split('@')[1]}")  # Log only host part
    else:
        logger.error("DATABASE_URL not set in environment")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Use SQLite locally
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visions.db'
    logger.info("Using SQLite database")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db = SQLAlchemy(app)
    logger.info("SQLAlchemy initialized successfully")
except Exception as e:
    logger.error(f"Error initializing SQLAlchemy: {str(e)}")
    raise

# Initialize the vision analyzer
try:
    vision_analyzer = VisionAnalyzer(BIBLICAL_SYMBOLS)
    logger.info("VisionAnalyzer initialized successfully")
except Exception as e:
    logger.error(f"Error initializing VisionAnalyzer: {str(e)}")
    raise

# Database Models
class Vision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    interpretation = db.Column(db.Text)

class BiblicalSymbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    scripture_references = db.Column(db.Text)
    category = db.Column(db.String(50))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_vision', methods=['POST'])
def submit_vision():
    data = request.json
    new_vision = Vision(
        title=data['title'],
        description=data['description'],
        context=data.get('context', '')
    )
    db.session.add(new_vision)
    db.session.commit()
    
    # Analyze the vision using the enhanced analyzer
    analysis = vision_analyzer.analyze_vision(
        description=new_vision.description,
        context=new_vision.context
    )
    
    # Format the interpretation for display
    interpretation_text = []
    
    if analysis['found_symbols']:
        interpretation_text.append("Biblical Symbols Found in Your Vision:\n")
        for symbol, meaning, references in analysis['interpretations']:
            interpretation_text.extend([
                f"• {symbol}:",
                f"  Meaning: {meaning}",
                f"  Scripture References: {references}",
                ""
            ])
    
    if analysis.get('pattern_insights'):
        interpretation_text.append("\nPattern Insights:")
        interpretation_text.extend(f"• {insight}" for insight in analysis['pattern_insights'])
        interpretation_text.append("")
    
    # Add the formatted commentary
    if analysis.get('formatted_commentary'):
        interpretation_text.append("\nBiblical Commentary and Prayer Guide:")
        interpretation_text.append(analysis['formatted_commentary'])
    
    interpretation_text.append("\nGuidance:")
    interpretation_text.extend(f"• {guidance}" for guidance in analysis['general_guidance'])
    
    # Save the interpretation
    new_vision.interpretation = "\n".join(interpretation_text)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'interpretation': new_vision.interpretation
    })

@app.route('/symbols')
def get_symbols():
    symbols = BiblicalSymbol.query.all()
    return jsonify([{
        'symbol': s.symbol,
        'meaning': s.meaning,
        'references': s.scripture_references
    } for s in symbols])

@app.route('/init_database', methods=['GET'])
def initialize_database():
    try:
        # Drop all tables first
        logger.info("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        logger.info("Creating new tables...")
        db.create_all()
        
        # Initialize the database with biblical symbols
        logger.info("Populating biblical symbols...")
        init_db()
        
        logger.info("Database initialization completed successfully")
        return jsonify({
            "message": "Database initialized successfully",
            "details": "Tables created and populated with biblical symbols"
        }), 200
    except Exception as e:
        error_msg = f"Error initializing database: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500

@app.route('/db_status', methods=['GET'])
def database_status():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        # Count records in BiblicalSymbol table
        symbol_count = BiblicalSymbol.query.count()
        
        return jsonify({
            "status": "connected",
            "database_url": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1],  # Only show host part
            "biblical_symbols_count": symbol_count
        }), 200
    except Exception as e:
        error_msg = f"Database error: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            "status": "error",
            "error": error_msg
        }), 500

def init_db():
    with app.app_context():
        db.create_all()
        # Use the new populate_database function
        populate_database(db, BiblicalSymbol)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    app.run(debug=True, port=5001)
