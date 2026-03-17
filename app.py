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
<title>Football Prediction Engine</title>
<style>
body{font-family:Arial,sans-serif;margin:0;padding:20px;background:linear-gradient(135deg,#1a73e8,#0d47a1);color:white}
.container{max-width:1200px;margin:0 auto}
.header{background:white;color:#1a73e8;padding:30px;border-radius:15px;text-align:center;margin-bottom:30px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:30px}
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
<div class="header"><h1>Football Prediction Engine</h1><p>AI-Powered Predictions Using 7 Custom Rules</p></div>
<div class="stats">
<div class="stat"><div class="stat-val" id="tm">0</div><div class="stat-lbl">Matches</div></div>
<div class="stat"><div class="stat-val" id="tp">0</div><div class="stat-lbl">Predictions</div></div>
<div class="stat"><div class="stat-val" id="wr">0%</div><div class="stat-lbl">Win Rate</div></div>
<div class="stat"><div class="stat-val" id="pr">$0</div><div class="stat-lbl">Profit</div></div>
</div>
<h2 class="section">TODAYS MATCHES & PREDICTIONS</h2>
<div id="mc">Loading...</div>
<h2 class="section">PREDICTION RULES</h2>
<div class="rules" id="rg"></div>
</div>
<script>
async function load(){
try{
const[p,s,r]=await Promise.all([fetch('/api/predictions'),fetch('/api/stats'),fetch('/api/rules')].map(f=>f.then(x=>x.json())));
document.getElementById('tm').textContent=s.total||0;
document.getElementById('tp').textContent=p.count||0;
document.getElementById('wr').textContent=(s.win_rate||0).toFixed(1)+'%';
let h='';
if(p.success&&p.predictions.length>0){
const m={};
p.predictions.forEach(x=>{if(!m[x.match])m[x.match]={odds:x.odds,league:x.league,preds:[]};m[x.match].preds.push(x);});
Object.entries(m).forEach(([match,d])=>{
h+='<div class="match"><div class="match-hdr"><div class="teams">'+match+'</div><div class="league">'+d.league+'</div></div>';
h+='<div class="odds"><div class="odd"><div style="color:#666;font-size:0.8em">Home</div><div class="odd-val">'+(d.odds.home||'-')+'</div></div>';
h+='<div class="odd"><div style="color:#666;font-size:0.8em">Draw</div><div class="odd-val">'+(d.odds.draw||'-')+'</div></div>';
h+='<div class="odd"><div style="color:#666;font-size:0.8em">Away</div><div class="odd-val">'+(d.odds.away||'-')+'</div></div></div>';
h+='<div class="preds"><strong>Predictions ('+d.preds.length+'):</strong>';
d.preds.forEach(x=>{h+='<div class="pred"><div><div class="pred-rule">'+x.rule+'</div><div style="color:#666;font-size:0.9em">'+x.market+'</div></div><div class="pred-odds">'+x.odds+'</div></div>';});
h+='</div></div>';});
}else{h='<div class="none">No predictions found</div>';}
document.getElementById('mc').innerHTML=h;
document.getElementById('rg').innerHTML=r.rules.map(x=>'<div class="rule"><strong>'+x.name+'</strong><br><small>'+x.description+'</small><br><span style="color:#1a73e8">'+x.market+'</span></div>').join('');
}catch(e){console.error(e);document.getElementById('mc').innerHTML='<div class="none">Error loading data</div>';}
}
load();
setInterval(load,60000);
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
        "success": True,
        "count": total,
        "matches": matches,
        "total_predictions": total_predictions,
        "wins": wins,
        "win_rate": win_rate
    })

if __name__ == '__main__':
    print("Running on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
