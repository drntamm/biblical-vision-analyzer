from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from biblical_symbols import populate_database, BIBLICAL_SYMBOLS
from vision_analyzer import VisionAnalyzer
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration
if os.environ.get('RENDER'):
    # Use PostgreSQL on Render.com
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
else:
    # Use SQLite locally
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visions.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize the vision analyzer
vision_analyzer = VisionAnalyzer(BIBLICAL_SYMBOLS)

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

def init_db():
    with app.app_context():
        db.create_all()
        # Use the new populate_database function
        populate_database(db, BiblicalSymbol)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
