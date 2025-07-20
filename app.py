import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from dotenv import load_dotenv
from travel_planner import TravelPlanner
from models import TripPreferences

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask Application
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize the travel planner
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("❌ GROQ_API_KEY not found in environment variables")
    logger.error("Please create a .env file with GROQ_API_KEY=your_key_here")
    logger.error("Or set the environment variable: export GROQ_API_KEY=your_key_here")
    exit(1)

try:
    planner = TravelPlanner(GROQ_API_KEY)
    logger.info("✅ Travel planner initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize travel planner: {e}")
    exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/plan-trip', methods=['POST'])
def plan_trip():
    try:
        data = request.get_json()
        logger.info(f"🌍 Received trip planning request for: {data.get('destination')}")
        
        # Create trip preferences object
        trip_prefs = TripPreferences(
            destination=data.get("destination", ""),
            duration=data.get("duration", ""),
            budget=data.get("budget", "mid-range"),
            travel_style=data.get("travelStyle", "cultural"),
            interests=data.get("interests", []),
            special_requests=data.get("specialRequests", ""),
            group_size=data.get("groupSize", 1)
        )
        
        # Validate required fields
        if not trip_prefs.destination or not trip_prefs.duration:
            return jsonify({"error": "Destination and duration are required"}), 400
        
        result = planner.plan_trip(trip_prefs)
        
        if "error" in result:
            return jsonify(result), 400
        
        logger.info(f"✅ Successfully planned trip for {trip_prefs.destination}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ API error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "groq_configured": bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    logger.info("🚀 Starting Travel Planner Application...")
    app.run(debug=True, host='0.0.0.0', port=5000)