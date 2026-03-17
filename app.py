from flask import Flask, render_template_string, jsonify
import json
from datetime import datetime
from final_engine import FinalPredictionEngine
from real_matches import get_real_fixtures

app = Flask(__name__)

# ===== BEAUTIFUL HTML TEMPLATE =====
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Football Prediction Engine</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Header */
        .header { 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .header h1 { 
            color: #1a73e8; 
            font-size: 2.5em; 
            margin-bottom: 10px;
        }
        .header p { color: #666; font-size: 1.1em; }
        .date { 
            background: #e8f0fe; 
            display: inline-block; 
            padding: 8px 20px; 
            border-radius: 20px; 
            margin-top: 15px;
            color: #1a73e8;
            font-weight: 600;
        }
        
        /* Stats Cards */
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: white; 
            padding: 25px; 
            border-radius: 15px; 
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .stat-value { 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #1a73e8;
            margin-bottom: 5px;
        }
        .stat-label { color: #666; font-size: 0.9em; }
        
        /* Matches Section */
        .section-title { 
            color: white; 
            font-size: 1.8em; 
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .match-card { 
            background: white; 
            border-radius: 15px; 
            padding: 25px; 
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }
        .match-card:hover { transform: translateY(-5px); }
        
        .match-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .match-teams { 
            font-size: 1.4em; 
            font-weight: bold; 
            color: #333;
        }
        .match-league { 
            background: #e8f0fe; 
            color: #1a73e8; 
            padding: 5px 15px; 
            border-radius: 20px; 
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .odds-display { 
            display: flex; 
            gap: 15px; 
            margin-bottom: 20px;
        }
        .odd-box { 
            flex: 1; 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center;
        }
        .odd-label { color: #666; font-size: 0.85em; margin-bottom: 5px; }
        .odd-value { 
            font-size: 1.3em; 
            font-weight: bold; 
            color: #1a73e8;
        }
        
        .predictions-section { 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 10px;
        }
        .predictions-title { 
            font-size: 1.1em; 
            font-weight: 600; 
            color: #333; 
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .predictions-title::before { 
            content: "🎯"; 
            font-size: 1.3em;
        }
        
        .prediction-item { 
            background: white; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 10px;
            border-left: 4px solid #34a853;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .prediction-item.high-confidence { border-left-color: #34a853; }
        .prediction-item.medium-confidence { border-left-color: #f9a825; }
        .prediction-item.low-confidence { border-left-color: #ea4335; }
        
        .prediction-info { flex: 1; }
        .prediction-rule { 
            font-weight: 600; 
            color: #1a73e8; 
            margin-bottom: 5px;
        }
        .prediction-market { color: #666; font-size: 0.95em; }
        
        .prediction-odds { 
            background: #e8f0fe; 
            padding: 8px 15px; 
            border-radius: 20px; 
            font-weight: 600;
            color: #1a73e8;
        }
        .prediction-confidence { 
            padding: 5px 12px; 
            border-radius: 15px; 
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }
        .confidence-high { background: #e6f4ea; color: #34a853; }
        .confidence-medium { background: #fef7e0; color: #f9a825; }
        .confidence-low { background: #fce8e6; color: #ea4335; }
        
        .no-predictions { 
            background: #fff3cd; 
            padding: 15px; 
            border-radius: 8px; 
            color: #856404;
            text-align: center;
        }
        
        /* Rules Info Section */
        .rules-section { 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            margin-top: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .rules-title { 
            font-size: 1.5em; 
            color: #333; 
            margin-bottom: 20px;
            text-align: center;
        }
        .rules-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 15px;
        }
        .rule-card { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px;
            border-left: 4px solid #1a73e8;
        }
        .rule-name { 
            font-weight: 600; 
            color: #1a73e8; 
            margin-bottom: 5px;
        }
        .rule-desc { color: #666; font-size: 0.9em; }
        .rule-market { 
            background: #e8f0fe; 
            display: inline-block; 
            padding: 3px 10px; 
            border-radius: 10px; 
            font-size: 0.85em;
            color: #1a73e8;
            margin-top: 8px;
        }
        
        /* Footer */
        .footer { 
            text-align: center; 
            color: white; 
            margin-top: 40px; 
            padding: 20px;
            opacity: 0.9;
        }
        .footer a { color: white; text-decoration: underline; }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header h1 { font-size: 1.8em; }
            .match-teams { font-size: 1.1em; }
            .odds-display { flex-direction: column; }
            .prediction-item { flex-direction: column; gap: 10px; text-align: center; }
        }
        
        /* Loading Animation */
        .loading { 
            text-align: center; 
            padding: 50px; 
            color: white; 
            font-size: 1.2em;
        }
        .spinner { 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #1a73e8; 
            border-radius: 50%; 
            width: 40px; 
            height: 40px; 
            animation: spin 1s linear infinite; 
            margin: 20px auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>⚽ Football Prediction Engine</h1>
            <p>AI-Powered Match Predictions Using 7 Custom Rules</p>
            <div class="date" id="currentDate"></div>
        </div>
        
        <!-- Stats Cards -->
        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-value" id="totalMatches">0</div>
                <div class="stat-label">Total Matches</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalPredictions">0</div>
                <div class="stat-label">Predictions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="winRate">0%</div>
                <div class="stat-label">Win Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalProfit">$0</div>
                <div class="stat-label">Total Profit</div>
            </div>
        </div>
        
        <!-- Matches Section -->
        <h2 class="section-title">📅 Today's Matches & Predictions</h2>
        <div id="matchesContainer">
            <div class="loading">
                <div class="spinner"></div>
                Loading predictions...
            </div>
        </div>
        
        <!-- Rules Info Section -->
        <div class="rules-section">
            <h2 class="rules-title">📋 Our 7 Prediction Rules</h2>
            <div class="rules-grid" id="rulesGrid"></div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>⚠️ <strong>Disclaimer:</strong> This is a prediction tool, not a guarantee. Football matches are unpredictable.</p>
            <p>Always bet responsibly. Never bet more than you can afford to lose.</p>
            <p style="margin-top: 15px;">Powered by <strong>Football Prediction Engine</strong> | <a href="/api/predictions">API</a></p>
        </div>
    </div>
    
    <script>
        // Set current date
        document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
        });
        
        // Load data from API
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
                
                // Update stats
                if (stats.success) {
                    document.getElementById('totalMatches').textContent = stats.total || 0;
                    document.getElementById('totalPredictions').textContent = predictions.count || 0;
                    document.getElementById('winRate').textContent = (stats.win_rate || 0).toFixed(1) + '%';
                    document.getElementById('totalProfit').textContent = '$' + (stats.total_profit || 0).toFixed(2);
                }
                
                // Display matches with predictions
                displayMatches(predictions);
                
                // Display rules
                displayRules(rules);
                
            } catch (error) {
                console.error('Error loading data:', error);
                document.getElementById('matchesContainer').innerHTML = `
                    <div class="no-predictions">
                        ⚠️ Error loading predictions. Please try again later.
                    </div>
                `;
            }
        }
        
        function displayMatches(data) {
            const container = document.getElementById('matchesContainer');
            
            if (!data.success || !data.predictions || data.predictions.length === 0) {
                container.innerHTML = `
                    <div class="no-predictions">
                        📭 No predictions available at the moment. Check back later!
                    </div>
                `;
                return;
            }
            
            // Group predictions by match
            const matchGroups = {};
            data.predictions.forEach(p => {
                if (!matchGroups[p.match]) {
                    matchGroups[p.match] = {
                        match: p.match,
                        league: p.league || 'League',
                        odds: p.odds || {},
                        predictions: []
                    };
                }
                matchGroups[p.match].predictions.push(p);
            });
            
            let html = '';
            Object.values(matchGroups).forEach(match => {
                html += `
                    <div class="match-card">
                        <div class="match-header">
                            <div class="match-teams">${match.match}</div>
                            <div class="match-league">${match.league}</div>
                        </div>
                        
                        <div class="odds-display">
                            <div class="odd-box">
                                <div class="odd-label">Home Win</div>
                                <div class="odd-value">${match.odds.home || '-'}</div>
                            </div>
                            <div class="odd-box">
                                <div class="odd-label">Draw</div>
                                <div class="odd-value">${match.odds.draw || '-'}</div>
                            </div>
                            <div class="odd-box">
                                <div class="odd-label">Away Win</div>
                                <div class="odd-value">${match.odds.away || '-'}</div>
                            </div>
                        </div>
                        
                        <div class="predictions-section">
                            <div class="predictions-title">Predictions (${match.predictions.length})</div>
                            ${match.predictions.map(p => `
                                <div class="prediction-item ${p.confidence === 'High' ? 'high-confidence' : p.confidence === 'Medium' ? 'medium-confidence' : 'low-confidence'}">
                                    <div class="prediction-info">
                                        <div class="prediction-rule">${p.rule}</div>
                                        <div class="prediction-market">${p.market}</div>
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 10px;">
                                        <div class="prediction-odds">${p.odds}</div>
                                        <div class="prediction-confidence confidence-${p.confidence === 'High' ? 'high' : p.confidence === 'Medium' ? 'medium' : 'low'}">
                                            ${p.confidence}
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        function displayRules(data) {
            const container = document.getElementById('rulesGrid');
            
            if (!data.success || !data.rules) return;
            
            container.innerHTML = data.rules.map(rule => `
                <div class="rule-card">
                    <div class="rule-name">${rule.name}</div>
                    <div class="rule-desc">${rule.description}</div>
                    <div class="rule-market">${rule.market}</div>
                </div>
            `).join('');
        }
        
        // Load data on page load
        loadData();
        
        // Auto-refresh every 60 seconds
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
    """Get all predictions"""
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
    
    return jsonify({
        "success": True,
        "count": len(all_predictions),
        "predictions": all_predictions
    })

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
    except FileNotFoundError:
        return jsonify({"success": True, "total": 0, "completed": 0, "wins": 0, "win_rate": 0, "total_profit": 0})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all 7 rules"""
    rules = [
        {"id": 1, "name": "Rule 1", "description": "Home 1.20-1.29 (excl 1.25) vs Away 10+", "market": "Home Win"},
        {"id": 2, "name": "Rule 2", "description": "Home 1.30-1.35 vs Away 12+", "market": "Home Win"},
        {"id": 3, "name": "Rule 3", "description": "Home 1.90-1.99", "market": "Home/Draw (1X)"},
        {"id": 4, "name": "Rule 4", "description": "Draw 3.4-3.6 + Away Over 1.5 (8/10)", "market": "Over 1.5 Goals"},
        {"id": 5, "name": "Rule 5", "description": "H2H HT Under 1.5 (25-38% probability)", "market": "1st Half Under 1.5"},
        {"id": 6, "name": "Rule 6", "description": "Draw 38-57% + Low Scoring + H2H Draws", "market": "Draw / GG"},
        {"id": 7, "name": "Rule 7", "description": "Home 1.75 + Away Over 1.5 (7/10)", "market": "Over 1.5 Goals"}
    ]
    return jsonify({"success": True, "rules": rules})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "football-predictions"})

if __name__ == '__main__':
    print("🚀 Football Prediction Website Running...")
    print("🌐 Open: http://localhost:8000")
    print("📱 API: http://localhost:8000/api/predictions")
    app.run(host='0.0.0.0', port=8000, debug=True)
