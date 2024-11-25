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
    try:
        data = request.json
        logger.info(f"Received vision submission: {data}")
        
        if not data or 'description' not in data:
            logger.error("Missing vision description in request")
            return jsonify({
                "error": "Please provide a vision description",
                "status": "error"
            }), 400
        
        # Create new vision entry
        new_vision = Vision(
            title=data.get('title', 'Untitled Vision'),
            description=data['description'],
            context=data.get('context', '')
        )
        
        # Analyze the vision
        try:
            analysis = vision_analyzer.analyze_vision(
                description=new_vision.description,
                context=new_vision.context
            )
            logger.info("Vision analysis completed successfully")
            
            # Convert analysis to string format if it's a dict
            if isinstance(analysis, dict):
                interpretation_text = f"""
Pattern Insights:
{chr(8226)} {chr(10).join(analysis.get('pattern_insights', ['No specific patterns identified']))}

Biblical Commentary:
Major Themes Identified:
{chr(8226)} {chr(10).join(analysis.get('themes', ['No specific themes identified']))}

Scripture References for Meditation:
{chr(8226)} {chr(10).join([f"{ref}: {text}" for ref, text in analysis.get('scripture_references', [('No specific references', 'Please seek guidance')])])}

Application Points:
{chr(8226)} {chr(10).join(analysis.get('application_points', ['Continue in prayer and meditation']))}

Prayer Points:
{chr(8226)} {chr(10).join(analysis.get('prayer_points', ['Seek divine guidance']))}
"""
            else:
                interpretation_text = str(analysis)
            
            new_vision.interpretation = interpretation_text
            logger.info("Interpretation text generated successfully")
            
        except Exception as e:
            logger.error(f"Error during vision analysis: {str(e)}")
            return jsonify({
                "error": "An error occurred while analyzing your vision. Please try again.",
                "status": "error",
                "details": str(e)
            }), 500
        
        # Save to database
        try:
            db.session.add(new_vision)
            db.session.commit()
            logger.info("Vision saved to database successfully")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.session.rollback()
            return jsonify({
                "error": "Database error occurred",
                "status": "error",
                "details": str(e)
            }), 500
        
        return jsonify({
            "interpretation": new_vision.interpretation,
            "status": "success"
        })
        
    except Exception as e:
        error_msg = f"Error processing vision: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            "error": "An unexpected error occurred. Please try again.",
            "status": "error",
            "details": str(e)
        }), 500

@app.route('/symbols')
def get_symbols():
    """Return biblical symbols organized by category"""
    from biblical_symbols import BIBLICAL_SYMBOLS
    
    # Organize symbols by category
    symbols_by_category = {}
    for symbol in BIBLICAL_SYMBOLS:
        category = symbol['category']
        if category not in symbols_by_category:
            symbols_by_category[category] = []
        symbols_by_category[category].append(symbol)
    
    return jsonify(symbols_by_category)

@app.route('/symbols_by_category')
def get_symbols_by_category():
    symbols = BiblicalSymbol.query.all()
    symbols_by_category = {}
    for symbol in symbols:
        category = symbol.category
        if category not in symbols_by_category:
            symbols_by_category[category] = []
        symbols_by_category[category].append({
            'symbol': symbol.symbol,
            'meaning': symbol.meaning,
            'references': symbol.scripture_references
        })
    return jsonify(symbols_by_category)

@app.route('/init_database', methods=['GET'])
def initialize_database():
    """Initialize the database with biblical symbols"""
    try:
        with app.app_context():
            # Drop all tables first
            logger.info("Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            logger.info("Creating new tables...")
            db.create_all()
            
            # Initialize the database with biblical symbols
            logger.info("Populating biblical symbols...")
            try:
                # Clear existing symbols first
                BiblicalSymbol.query.delete()
                db.session.commit()
                logger.info("Cleared existing symbols")
                
                # Add new symbols
                for symbol_data in BIBLICAL_SYMBOLS:
                    symbol = BiblicalSymbol(
                        symbol=symbol_data['symbol'],
                        meaning=symbol_data['meaning'],
                        scripture_references=symbol_data.get('scripture_references', ''),
                        category=symbol_data.get('category', 'General')
                    )
                    db.session.add(symbol)
                
                # Commit new symbols
                db.session.commit()
                logger.info(f"Added {len(BIBLICAL_SYMBOLS)} symbols to database")
                
                return jsonify({
                    "status": "success",
                    "message": "Database initialized successfully",
                    "details": f"Added {len(BIBLICAL_SYMBOLS)} biblical symbols"
                }), 200
                
            except Exception as e:
                db.session.rollback()
                error_msg = f"Error populating symbols: {str(e)}"
                logger.error(error_msg)
                return jsonify({"error": error_msg}), 500
                
    except Exception as e:
        error_msg = f"Error initializing database: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500

@app.route('/db_status')
def database_status():
    """Check database status and symbol count"""
    try:
        with app.app_context():
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Count symbols
            symbol_count = BiblicalSymbol.query.count()
            
            # Get sample symbols
            sample_symbols = BiblicalSymbol.query.limit(3).all()
            sample_data = [
                {
                    "symbol": s.symbol,
                    "meaning": s.meaning[:100] + "..." if len(s.meaning) > 100 else s.meaning
                }
                for s in sample_symbols
            ]
            
            return jsonify({
                "status": "success",
                "database_url": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else 'sqlite',
                "tables": tables,
                "symbol_count": symbol_count,
                "sample_symbols": sample_data
            }), 200
            
    except Exception as e:
        error_msg = f"Error checking database status: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            "status": "error",
            "error": error_msg,
            "database_url": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else 'sqlite'
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
            logger.info("Database tables created successfully")
            
            # Initialize biblical symbols in the database
            try:
                populate_database(db)
                logger.info("Biblical symbols populated successfully")
            except Exception as e:
                logger.error(f"Error populating biblical symbols: {str(e)}")
            
            # Test the vision analyzer
            test_vision = "Test vision"
            try:
                result = vision_analyzer.analyze_vision(test_vision)
                logger.info("Vision analyzer test successful")
            except Exception as e:
                logger.error(f"Vision analyzer test failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            raise
    
    # Run the app with debug mode for development
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True)
    else:
        # Production settings
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
