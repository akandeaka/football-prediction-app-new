from flask import Flask, render_template_string, jsonify
import json
from datetime import datetime
import traceback

# Assuming these exist in your project
from final_engine import FinalPredictionEngine
from real_matches import get_real_fixtures

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Football Prediction Engine</title>
<style>
    body{font-family:Arial,sans-serif;margin:0;padding:20px;background:linear-gradient(135deg,#1a73e8,#0d47a1);color:white}
    .container{max-width:1200px;margin:0 auto}
    .header{background:white;color:#1a73e8;padding:30px;border-radius:15px;text-align:center;margin-bottom:30px}
    .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;margin-bottom:30px}
    .stat{background:white;padding:20px;border-radius:12px;text-align:center;color:#1a73e8}
    .stat-val{font-size:2.5em;font-weight:bold}
    .stat-lbl{color:#666;font-size:0.9em;margin-top:5px}
    .section{font-size:1.6em;margin:25px 0 15px;text-align:center}
    .match{background:white;color:#333;border-radius:12px;padding:20px;margin-bottom:15px}
    .match-hdr{display:flex;justify-content:space-between;margin-bottom:15px;padding-bottom:10px;border-bottom:2px solid #f0f0f0}
    .teams{font-size:1.2em;font-weight:bold}
    .league{background:#e8f0fe;color:#1a73e8;padding:4px 12px;border-radius:15px}
    .odds{display:flex;gap:10px;margin-bottom:15px}
    .odd{flex:1;background:#f8f9fa;padding:10px;border-radius:8px;text-align:center}
    .odd-val{font-size:1.1em;font-weight:bold;color:#1a73e8}
    .preds{background:#f8f9fa;padding:15px;border-radius:8px}
    .pred{background:white;padding:12px;margin:8px 0;border-radius:6px;border-left:4px solid #34a853;display:flex;justify-content:space-between;align-items:center}
    .pred-rule{font-weight:600;color:#1a73e8}
    .pred-odds{background:#e8f0fe;padding:4px 10px;border-radius:12px;font-weight:600}
    .rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
    .rule{background:#f8f9fa;color:#333;padding:12px;border-radius:8px;border-left:4px solid #1a73e8}
    .none{background:#fff3cd;padding:15px;border-radius:8px;text-align:center;color:#856404}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Football Prediction Engine</h1>
        <p>AI-Powered Predictions Using 7 Custom Rules</p>
    </div>
    <div class="stats">
        <div class="stat"><div class="stat-val" id="tm">0</div><div class="stat-lbl">Matches</div></div>
        <div class="stat"><div class="stat-val" id="tp">0</div><div class="stat-lbl">Predictions</div></div>
        <div class="stat"><div class="stat-val" id="wr">0%</div><div class="stat-lbl">Win Rate</div></div>
        <div class="stat"><div class="stat-val" id="pr">$0</div><div class="stat-lbl">Profit</div></div>
    </div>
    <h2 class="section">TODAY'S MATCHES & PREDICTIONS</h2>
    <div id="mc">Loading...</div>
    <h2 class="section">PREDICTION RULES</h2>
    <div class="rules" id="rg"></div>
</div>

<script>
async function load() {
    try {
        const [p, s, r] = await Promise.all([
            fetch('/api/predictions').then(x => x.json()),
            fetch('/api/stats').then(x => x.json()),
            fetch('/api/rules').then(x => x.json())
        ]);

        document.getElementById('tm').textContent = s.total_matches || 0;
        document.getElementById('tp').textContent = s.total_predictions || 0;
        document.getElementById('wr').textContent = (s.win_rate || 0).toFixed(1) + '%';
        // Profit not really calculated properly yet → placeholder
        document.getElementById('pr').textContent = '$' + (s.total_profit || 0);

        let h = '';
        if (p.success && Array.isArray(p.predictions) && p.predictions.length > 0) {
            const matches = {};
            p.predictions.forEach(pred => {
                const key = pred.match;
                if (!matches[key]) {
                    matches[key] = {
                        odds: pred.odds || {home:'-',draw:'-',away:'-'},
                        league: pred.league || '—',
                        preds: []
                    };
                }
                matches[key].preds.push(pred);
            });

            Object.entries(matches).forEach(([match, data]) => {
                h += `<div class="match">
                    <div class="match-hdr">
                        <div class="teams">${match}</div>
                        <div class="league">${data.league}</div>
                    </div>
                    <div class="odds">
                        <div class="odd"><div style="color:#666;font-size:0.8em">Home</div><div class="odd-val">${data.odds.home}</div></div>
                        <div class="odd"><div style="color:#666;font-size:0.8em">Draw</div><div class="odd-val">${data.odds.draw}</div></div>
                        <div class="odd"><div style="color:#666;font-size:0.8em">Away</div><div class="odd-val">${data.odds.away}</div></div>
                    </div>
                    <div class="preds"><strong>Predictions (${data.preds.length}):</strong>`;
                data.preds.forEach(pred => {
                    h += `<div class="pred">
                        <div>
                            <div class="pred-rule">${pred.rule || '?'}</div>
                            <div style="color:#666;font-size:0.9em">${pred.market || '—'}</div>
                        </div>
                        <div class="pred-odds">${pred.odds || '—'}</div>
                    </div>`;
                });
                h += '</div></div>';
            });
        } else {
            h = '<div class="none">No predictions available for today</div>';
        }

        document.getElementById('mc').innerHTML = h;

        // Rules
        document.getElementById('rg').innerHTML = r.rules
            .map(rule => `
                <div class="rule">
                    <strong>${rule.name}</strong><br>
                    <small>${rule.description}</small><br>
                    <span style="color:#1a73e8">${rule.market}</span>
                </div>`)
            .join('');

    } catch (e) {
        console.error(e);
        document.getElementById('mc').innerHTML = '<div class="none">Error loading data</div>';
    }
}

load();
setInterval(load, 120000);  // 2 minutes
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    try:
        fixtures = get_real_fixtures() or []
        engine = FinalPredictionEngine()
        all_predictions = []

        for fixture in fixtures:
            # Defensive programming — protect against malformed data
            home = fixture.get('home', 'Unknown')
            away = fixture.get('away', 'Unknown')
            match_name = f"{home} vs {away}"

            match_data = {
                'name': match_name,
                'odds': fixture.get('odds', {'home': '-', 'draw': '-', 'away': '-'}),
                'team_stats': fixture.get('team_stats', {}),
                'h2h_stats': fixture.get('h2h_stats', {}),
                'league_info': fixture.get('league_info', {}),
                'league': fixture.get('league', 'Unknown League'),
                'date': fixture.get('date', datetime.now().strftime("%Y-%m-%d")),
            }

            try:
                predictions = engine.process_match(match_data) or []
                for pred in predictions:
                    pred_copy = dict(pred)  # avoid mutating original if any
                    pred_copy['match'] = match_name
                    pred_copy['date'] = match_data['date']
                    pred_copy['league'] = match_data['league']
                    all_predictions.append(pred_copy)
            except Exception as e:
                print(f"Error processing match {match_name}: {e}")
                continue

        return jsonify({
            "success": True,
            "count": len(all_predictions),
            "predictions": all_predictions
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "predictions": []
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    # Very naive version — improve when you have real logging
    try:
        with open('predictions_log.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    completed = [p for p in data if p.get('status') in ['WIN', 'LOSS', 'win', 'loss']]
    wins = [p for p in completed if p.get('status', '').upper() == 'WIN']

    total_matches = len(set(p.get('match') for p in data if p.get('match')))
    total_predictions = len(data)
    win_rate = (len(wins) / len(completed) * 100) if completed else 0
    # Real profit calculation requires stake size — placeholder
    total_profit = sum(float(p.get('profit', 0)) for p in completed)

    return jsonify({
        "success": True,
        "total_matches": total_matches,
        "total_predictions": total_predictions,
        "completed": len(completed),
        "wins": len(wins),
        "win_rate": round(win_rate, 1),
        "total_profit": round(total_profit, 2)
    })


@app.route('/api/rules', methods=['GET'])
def get_rules():
    rules = [
        {"name": "Rule 1", "description": "Home 1.20–1.29 vs Away odds 10+", "market": "Home Win"},
        {"name": "Rule 2", "description": "Home 1.30–1.35 vs Away odds 12+", "market": "Home Win"},
        {"name": "Rule 3", "description": "Home odds 1.90–1.99", "market": "Home/Draw (1X)"},
        {"name": "Rule 4", "description": "Draw 3.4–3.6 + Away team Over 1.5", "market": "Over 1.5 Goals"},
        {"name": "Rule 5", "description": "H2H HT Under 1.5 in 25–38% of matches", "market": "1st Half Under 1.5"},
        {"name": "Rule 6", "description": "Draw probability 38–57% + low scoring", "market": "Draw / GG"},
        {"name": "Rule 7", "description": "Home odds 1.75+ + Away Over 1.5", "market": "Over 1.5 Goals"}
    ]
    return jsonify({"success": True, "rules": rules})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    print("Starting server → http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
