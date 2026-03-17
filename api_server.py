from flask import Flask, jsonify
from flask_cors import CORS
from final_engine import FinalPredictionEngine
from real_matches import get_real_fixtures
import json

app = Flask(__name__)
CORS(app)

engine = FinalPredictionEngine()

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get all predictions (for mobile app)"""
    fixtures = get_real_fixtures()
    all_predictions = []
    
    for f in fixtures:
        match_data = {
            'name': f"{f['home']} vs {f['away']}",
            'odds': f['odds'],
            'team_stats': f.get('team_stats', {}),
            'h2h_stats': f.get('h2h_stats', {}),
            'league_info': f.get('league_info', {})
        }
        predictions = engine.process_match(match_data)
        for p in predictions:
            p['match'] = match_data['name']
            p['date'] = f.get('date', '')
            p['league'] = f.get('league', '')
            all_predictions.append(p)
    
    return jsonify({
        "success": True,
        "count": len(all_predictions),
        "predictions": all_predictions
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get performance stats (for mobile app)"""
    try:
        with open('predictions_log.json', 'r') as f:
            data = json.load(f)
        
        completed = [p for p in data if p.get('status') == 'WIN' or p.get('status') == 'LOSS']
        wins = [p for p in completed if p.get('status') == 'WIN']
        
        return jsonify({
            "success": True,
            "total": len(data),
            "completed": len(completed),
            "wins": len(wins),
            "win_rate": (len(wins)/len(completed)*100) if completed else 0
        })
    except FileNotFoundError:
        return jsonify({"success": False, "error": "No data"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all 7 rules (for mobile app info screen)"""
    rules = [
        {"id": 1, "name": "Rule 1", "description": "Home 1.20-1.29 vs Away 10+", "market": "Home Win"},
        {"id": 2, "name": "Rule 2", "description": "Home 1.30-1.35 vs Away 12+", "market": "Home Win"},
        {"id": 3, "name": "Rule 3", "description": "Home 1.90-1.99", "market": "Home/Draw (1X)"},
        {"id": 4, "name": "Rule 4", "description": "Draw 3.4-3.6 + Away Over 1.5", "market": "Over 1.5 Goals"},
        {"id": 5, "name": "Rule 5", "description": "H2H HT Under 1.5 (25-38%)", "market": "1st Half Under 1.5"},
        {"id": 6, "name": "Rule 6", "description": "Draw 38-57% + Low Scoring + H2H", "market": "Draw / GG"},
        {"id": 7, "name": "Rule 7", "description": "Home 1.75 + Away Over 1.5 (7/10)", "market": "Over 1.5 Goals"}
    ]
    return jsonify({"success": True, "rules": rules})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "football-predictions-api"})

if __name__ == '__main__':
    print("🚀 Mobile API Server Running...")
    print("📱 Endpoints:")
    print("   GET /api/predictions - Get all predictions")
    print("   GET /api/stats - Get performance stats")
    print("   GET /api/rules - Get rule information")
    print("   GET /health - Health check")
    app.run(host='0.0.0.0', port=5000, debug=True)