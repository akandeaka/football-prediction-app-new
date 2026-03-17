from flask import Flask, render_template_string, jsonify
import json
import requests
from datetime import datetime
from final_engine import FinalPredictionEngine

app = Flask(__name__)

# FREE API - Football-Data.org (no key needed for basic usage)
API_URL = "https://api.football-data.org/v4"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚽ Football Prediction Engine</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .header h1 { color: #1a73e8; font-size: 2.5em; margin-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2em; font-weight: bold; color: #1a73e8; }
        .stat-label { color: #666; font-size: 0.9em; margin-top: 5px; }
        .section-title { color: white; font-size: 1.6em; margin: 25px 0 15px; text-align: center; }
        .match-card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
        .match-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }
        .match-teams { font-size: 1.2em; font-weight: bold; color: #333; }
        .match-league { background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 15px; font-size: 0.85em; }
        .odds-display { display: flex; gap: 10px; margin-bottom: 15px; }
        .odd-box { flex: 1; background: #f8f9fa; padding: 10px; border-radius: 8px; text-align: center; }
        .odd-label { color: #666; font-size: 0.8em; margin-bottom: 3px; }
        .odd-value { font-size: 1.1em; font-weight: bold; color: #1a73e8; }
        .predictions-section { background: #f8f9fa; padding: 15px; border-radius: 8px; }
        .prediction-item { background: white; padding: 12px; margin: 8px 0; border-radius: 6px; border-left: 4px solid #34a853; display: flex; justify-content: space-between; align-items: center; }
        .prediction-rule { font-weight: 600; color: #1a73e8; }
        .prediction-odds { background: #e8f0fe; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 0.9em; }
        .rules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }
        .rule-card { background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #1a73e8; }
        .no-predictions { background: #fff3cd; padding: 15px; border-radius: 8px; text-align: center; color: #856404; }
        .loading { text-align: center; padding: 30px; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ Football Prediction Engine</h1>
            <p>AI-Powered Predictions Using 7 Custom Rules</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-value" id="totalMatches">0</div><div class="stat-label">Matches</div></div>
            <div class="stat-card"><div class="stat-value" id="totalPredictions">0</div><div class="stat-label">Predictions</div></div>
            <div class="stat-card"><div class="stat-value" id="winRate">0%</div><div class="stat-label">Win Rate</div></div>
            <div class="stat-card"><div class="stat-value" id="totalProfit">$0</div><div class="stat-label">Profit</div></div>
        </div>
        <h2 class="section-title">📅 TODAY'S MATCHES & PREDICTIONS</h2>
        <div id="matchesContainer"><div class="loading">Loading live matches...</div></div>
        <h2 class="section-title">📋 PREDICTION RULES</h2>
        <div class="rules-grid" id="rulesGrid"></div>
    </div>
    <script>
        async function loadData() {
            try {
                const [predRes, statsRes, rulesRes] = await Promise.all([
                    fetch('/api/predictions'),
                    fetch('/api/stats'),
                    fetch('/api/rules')
                ]);
                const predictions = await predRes.json();
                const stats = await statsRes.json();
                const rules = await rulesRes.json();
                
                document.getElementById('totalMatches').textContent = stats.total || 0;
                document.getElementById('totalPredictions').textContent = predictions.count || 0;
                document.getElementById('winRate').textContent = (stats.win_rate || 0).toFixed(1) + '%';
                
                let html = '';
                if (predictions.success && predictions.predictions.length > 0) {
                    const matches = {};
                    predictions.predictions.forEach(p => {
                        if (!matches[p.match]) matches[p.match] = { odds: p.odds, league: p.league, preds: [] };
                        matches[p.match].preds.push(p);
                    });
                    Object.entries(matches).forEach(([match, data]) => {
                        html += '<div class="match-card">';
                        html += '<div class="match-header"><div class="match-teams">' + match + '</div><div class="match-league">' + data.league + '</div></div>';
                        html += '<div class="odds-display">';
                        html += '<div class="odd-box"><div class="odd-label">Home</div><div class="odd-value">' + (data.odds.home || '-') + '</div></div>';
                        html += '<div class="odd-box"><div class="odd-label">Draw</div><div class="odd-value">' + (data.odds.draw || '-') + '</div></div>';
                        html += '<div class="odd-box"><div class="odd-label">Away</div><div class="odd-value">' + (data.odds.away || '-') + '</div></div>';
                        html += '</div>';
                        html += '<div class="predictions-section"><strong>🎯 Predictions (' + data.preds.length + '):</strong>';
                        data.preds.forEach(p => {
                            html += '<div class="prediction-item">';
                            html += '<div><div class="prediction-rule">' + p.rule + '</div><div style="color:#666;font-size:0.9em">' + p.market + '</div></div>';
                            html += '<div class="prediction-odds">' + p.odds + '</div>';
                            html += '</div>';
                        });
                        html += '</div></div>';
                    });
                } else {
                    html = '<div class="no-predictions">⚠️ No predictions found. Check back later or add matches manually.</div>';
                }
                document.getElementById('matchesContainer').innerHTML = html;
                
                document.getElementById('rulesGrid').innerHTML = rules.rules.map(r => 
                    '<div class="rule-card"><strong>' + r.name + '</strong><br><small>' + r.description + '</small><br><span style="color:#1a73e8">' + r.market + '</span></div>'
                ).join('');
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('matchesContainer').innerHTML = '<div class="no-predictions">Error loading data</div>';
            }
        }
        loadData();
        setInterval(loadData, 60000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get predictions from live API"""
    try:
        # Fetch today's matches from free API
        response = requests.get(f"{API_URL}/matches", params={"matchStatus": "SCHEDULED"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            fixtures = data.get('matches', [])[:10]  # Limit to 10 matches
            
            engine = FinalPredictionEngine()
            all_predictions = []
            
            for match in fixtures:
                try:
                    home = match['homeTeam']['name']
                    away = match['awayTeam']['name']
                    league = match.get('competition', {}).get('name', 'Unknown')
                    
                    # Get odds (API may not always have them)
                    odds_data = match.get('odds', {})
                    home_odds = 2.0
                    draw_odds = 3.5
                    away_odds = 3.5
                    
                    # Simple odds extraction if available
                    if odds_data and 'match' in odds_data:
                        for odd in odds_data['match']:
                            if odd.get('marketName') == 'Full Time Result':
                                for outcome in odd.get('selections', []):
                                    name = outcome.get('name', '')
                                    if 'Home' in name or home in name:
                                        home_odds = outcome.get('odds', 2.0)
                                    elif 'Draw' in name:
                                        draw_odds = outcome.get('odds', 3.5)
                                    elif 'Away' in name or away in name:
                                        away_odds = outcome.get('odds', 3.5)
                    
                    match_data = {
                        'name': f"{home} vs {away}",
                        'odds': {'home': home_odds, 'draw': draw_odds, 'away': away_odds},
                        'team_stats': {'away_over_1_5_last_10': 7},
                        'h2h_stats': {'total_matches': 10, 'ht_under_1_5_count': 3, 'draw_count': 4},
                        'league_info': {'is_low_scoring': False, 'draw_probability': 45},
                        'league': league
                    }
                    
                    predictions = engine.process_match(match_data)
                    for p in predictions:
                        p['match'] = match_data['name']
                        p['league'] = league
                        all_predictions.append(p)
                        
                except Exception as e:
                    continue
            
            return jsonify({"success": True, "count": len(all_predictions), "predictions": all_predictions})
    except Exception as e:
        pass
    
    # Fallback: Return empty if API fails
    return jsonify({"success": True, "count": 0, "predictions": []})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get performance stats"""
    try:
        with open('predictions_log.json', 'r') as f:
            data = json.load(f)
        completed = [p for p in data if p.get('status') in ['WIN', 'LOSS']]
        wins = [p for p in completed if p.get('status') == 'WIN']
        total_profit = sum(p.get('profit', 0) for p in completed)
        return jsonify({
            "success": True,
            "total": len(data),
            "completed": len(completed),
            "wins": len(wins),
            "win_rate": (len(wins)/len(completed)*100) if completed else 0,
            "total_profit": total_profit
        })
    except:
        return jsonify({"success": True, "total": 0, "completed": 0, "wins": 0, "win_rate": 0, "total_profit": 0})

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all 7 rules"""
    rules = [
        {"id": 1, "name": "Rule 1", "description": "Home 1.20-1.29 vs Away 10+", "market": "Home Win"},
        {"id": 2, "name": "Rule 2", "description": "Home 1.30-1.35 vs Away 12+", "market": "Home Win"},
        {"id": 3, "name": "Rule 3", "description": "Home 1.90-1.99", "market": "Home/Draw (1X)"},
        {"id": 4, "name": "Rule 4", "description": "Draw 3.4-3.6 + Away Over 1.5", "market": "Over 1.5 Goals"},
        {"id": 5, "name": "Rule 5", "description": "H2H HT Under 1.5 (25-38%)", "market": "1st Half Under 1.5"},
        {"id": 6, "name": "Rule 6", "description": "Draw 38-57% + Low Scoring", "market": "Draw / GG"},
        {"id": 7, "name": "Rule 7", "description": "Home 1.75 + Away Over 1.5", "market": "Over 1.5 Goals"}
    ]
    return jsonify({"success": True, "rules": rules})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("🚀 Running on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
