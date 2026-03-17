from flask import Flask, render_template_string, jsonify
import json
from datetime import datetime
from final_engine import FinalPredictionEngine
from real_matches import get_real_fixtures

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚽ Football Prediction Engine</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
        .header h1 { color: #1a73e8; font-size: 2.5em; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 25px; border-radius: 15px; text-align: center; }
        .stat-value { font-size: 2.5em; font-weight: bold; color: #1a73e8; }
        .stat-label { color: #666; margin-top: 5px; }
        .section-title { color: white; font-size: 1.8em; margin: 30px 0 20px; text-align: center; }
        .match-card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
        .match-header { display: flex; justify-content: space-between; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f0f0f0; }
        .match-teams { font-size: 1.4em; font-weight: bold; }
        .match-league { background: #e8f0fe; color: #1a73e8; padding: 5px 15px; border-radius: 20px; }
        .odds-display { display: flex; gap: 15px; margin-bottom: 20px; }
        .odd-box { flex: 1; background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; }
        .odd-value { font-size: 1.3em; font-weight: bold; color: #1a73e8; }
        .predictions-section { background: #f8f9fa; padding: 20px; border-radius: 10px; }
        .prediction-item { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #34a853; display: flex; justify-content: space-between; align-items: center; }
        .prediction-rule { font-weight: 600; color: #1a73e8; }
        .prediction-odds { background: #e8f0fe; padding: 5px 12px; border-radius: 15px; font-weight: 600; }
        .rules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .rule-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #1a73e8; }
        .no-predictions { background: #fff3cd; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ Football Prediction Engine</h1>
            <p>AI-Powered Match Predictions Using 7 Custom Rules</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-value" id="totalMatches">0</div><div class="stat-label">Total Matches</div></div>
            <div class="stat-card"><div class="stat-value" id="totalPredictions">0</div><div class="stat-label">Predictions</div></div>
            <div class="stat-card"><div class="stat-value" id="winRate">0%</div><div class="stat-label">Win Rate</div></div>
            <div class="stat-card"><div class="stat-value" id="totalProfit">$0</div><div class="stat-label">Total Profit</div></div>
        </div>
        <h2 class="section-title">📅 Today's Matches & Predictions</h2>
        <div id="matchesContainer">Loading...</div>
        <h2 class="section-title">📊 Previous Matches</h2>
        <div id="previousMatchesContainer">Loading...</div>
        <div class="section-title" style="margin-top:30px">📋 Our 7 Prediction Rules</div>
        <div class="rules-grid" id="rulesGrid"></div>
    </div>
    <script>
        async function loadData() {
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
                    html += '<div class="match-card"><div class="match-header"><div class="match-teams">' + match + '</div><div class="match-league">' + data.league + '</div></div>';
                    html += '<div class="odds-display"><div class="odd-box">Home: ' + (data.odds.home||'-') + '</div><div class="odd-box">Draw: ' + (data.odds.draw||'-') + '</div><div class="odd-box">Away: ' + (data.odds.away||'-') + '</div></div>';
                    html += '<div class="predictions-section"><strong>Predictions:</strong>';
                    data.preds.forEach(p => {
                        html += '<div class="prediction-item"><div><div class="prediction-rule">' + p.rule + '</div><div>' + p.market + '</div></div><div class="prediction-odds">' + p.odds + '</div></div>';
                    });
                    html += '</div></div>';
                });
            } else {
                html = '<div class="no-predictions">No predictions available. Add matches to real_matches.py</div>';
            }
            document.getElementById('matchesContainer').innerHTML = html;
            
            document.getElementById('rulesGrid').innerHTML = rules.rules.map(r => 
                '<div class="rule-card"><strong>' + r.name + '</strong><br>' + r.description + '<br><small>' + r.market + '</small></div>'
            ).join('');
        }
        
        async function loadPrevious() {
            const res = await fetch('/api/previous-matches');
            const data = await res.json();
            let html = '';
            if (data.success && data.matches.length > 0) {
                data.matches.forEach(m => {
                    html += '<div class="match-card"><div class="match-header"><div class="match-teams">' + m.home + ' ' + (m.home_goals||0) + '-' + (m.away_goals||0) + ' ' + m.away + '</div><div class="match-league">' + m.league + '</div></div>';
                    if (m.predictions) {
                        m.predictions.forEach(p => {
                            html += '<div class="prediction-item" style="border-left-color:' + (p.status==='WIN'?'#34a853':'#ea4335') + '"><div><div class="prediction-rule">' + p.rule + '</div><div>' + p.market + '</div></div><div>' + (p.status==='WIN'?'✅':'❌') + '</div></div>';
                        });
                    }
                    html += '</div>';
                });
            } else {
                html = '<div class="no-predictions">No previous matches recorded</div>';
            }
            document.getElementById('previousMatchesContainer').innerHTML = html;
        }
        
        loadData();
        loadPrevious();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    fixtures = get_real_fixtures()
    engine = FinalPredictionEngine()
    all_predictions = []
    for f in fixtures:
        match_data = {
            'name': f"{f['home']} vs {f['away']}",
            'odds': f['odds'],
            'team_stats': f.get('team_stats', {}),
            'h2h_stats': f.get('h2h_stats', {}),
            'league_info': f.get('league_info', {}),
            'league': f.get('league', 'Unknown League')
        }
        predictions = engine.process_match(match_data)
        for p in predictions:
            p['match'] = match_data['name']
            p['date'] = f.get('date', '')
            p['league'] = match_data['league']
            all_predictions.append(p)
    return jsonify({"success": True, "count": len(all_predictions), "predictions": all_predictions})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        with open('predictions_log.json', 'r') as f:
            data = json.load(f)
        completed = [p for p in data if p.get('status') in ['WIN', 'LOSS']]
        wins = [p for p in completed if p.get('status') == 'WIN']
        total_profit = sum(p.get('profit', 0) for p in completed)
        return jsonify({
            "success": True, "total": len(data), "completed": len(completed),
            "wins": len(wins), "win_rate": (len(wins)/len(completed)*100) if completed else 0,
            "total_profit": total_profit
        })
    except:
        return jsonify({"success": True, "total": 0, "completed": 0, "wins": 0, "win_rate": 0, "total_profit": 0})

@app.route('/api/rules', methods=['GET'])
def get_rules():
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

@app.route('/api/previous-matches', methods=['GET'])
def get_previous_matches():
    from real_matches import get_previous_matches
    matches = get_previous_matches()
    total = len(matches)
    total_predictions = sum(len(m.get('predictions', [])) for m in matches)
    wins = sum(1 for m in matches for p in m.get('predictions', []) if p.get('status') == 'WIN')
    win_rate = (wins / total_predictions * 100) if total_predictions > 0 else 0
    return jsonify({
        "success": True, "count": total, "matches": matches,
        "total_predictions": total_predictions, "wins": wins, "win_rate": win_rate
    })

if __name__ == '__main__':
    print("🚀 Running on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)