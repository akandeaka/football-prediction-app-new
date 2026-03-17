from flask import Flask, render_template_string, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# HTML Template (embedded for simplicity)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚽ Football Prediction App</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { background: #1a73e8; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .prediction { border-left: 4px solid #34a853; padding-left: 15px; margin: 10px 0; }
        .prediction.loss { border-left-color: #ea4335; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
        .stat { background: #e8f0fe; padding: 15px; border-radius: 6px; text-align: center; }
        .stat-value { font-size: 24px; font-weight: bold; color: #1a73e8; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; }
        .win { color: #34a853; font-weight: bold; }
        .loss { color: #ea4335; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚽ Football Prediction Engine</h1>
        <p>Rule-based AI predictions with backtesting</p>
    </div>
    
    <div class="card">
        <h2>📊 Live Statistics</h2>
        <div class="stats" id="stats"></div>
    </div>
    
    <div class="card">
        <h2>🎯 Recent Predictions</h2>
        <table>
            <thead><tr><th>Match</th><th>Rule</th><th>Market</th><th>Odds</th><th>Result</th></tr></thead>
            <tbody id="predictions"></tbody>
        </table>
    </div>
    
    <div class="card">
        <h2>📈 Rule Performance</h2>
        <table>
            <thead><tr><th>Rule</th><th>Win Rate</th><th>ROI</th><th>Profit</th></tr></thead>
            <tbody id="rules"></tbody>
        </table>
    </div>

    <script>
        fetch('/api/data')
            .then(r => r.json())
            .then(data => {
                // Stats
                document.getElementById('stats').innerHTML = `
                    <div class="stat"><div class="stat-value">${data.total_predictions}</div><div>Predictions</div></div>
                    <div class="stat"><div class="stat-value">${data.win_rate}%</div><div>Win Rate</div></div>
                    <div class="stat"><div class="stat-value">$${data.total_profit.toFixed(2)}</div><div>Profit</div></div>
                    <div class="stat"><div class="stat-value">${data.roi}%</div><div>ROI</div></div>
                `;
                
                // Predictions table
                const preds = data.predictions.slice(-10).reverse();
                document.getElementById('predictions').innerHTML = preds.map(p => `
                    <tr>
                        <td>${p.match}</td>
                        <td>${p.rule}</td>
                        <td>${p.market}</td>
                        <td>${p.odds}</td>
                        <td class="${p.result.toLowerCase()}">${p.result}</td>
                    </tr>
                `).join('');
                
                // Rules table
                document.getElementById('rules').innerHTML = Object.entries(data.by_rule).map(([rule, stats]) => {
                    const rate = (stats.wins / stats.total * 100).toFixed(0);
                    const roi = (stats.profit / (stats.total * 10) * 100).toFixed(1);
                    return `<tr>
                        <td>${rule}</td>
                        <td>${stats.wins}/${stats.total} (${rate}%)</td>
                        <td>${roi}%</td>
                        <td class="${stats.profit >= 0 ? 'win' : 'loss'}">$${stats.profit.toFixed(2)}</td>
                    </tr>`;
                }).join('');
            });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    # Try to load backtest report, fallback to predictions_log
    try:
        with open('backtest_report.json', 'r') as f:
            report = json.load(f)
        return jsonify(report)
    except FileNotFoundError:
        try:
            with open('predictions_log.json', 'r') as f:
                data = json.load(f)
            # Convert to report format
            completed = [p for p in data if p['status'] != 'PENDING']
            wins = [p for p in completed if p['status'] == 'WIN']
            total_profit = sum(p.get('profit', 0) for p in completed)
            return jsonify({
                "total_predictions": len(data),
                "win_rate": (len(wins)/len(completed)*100) if completed else 0,
                "total_profit": total_profit,
                "roi": (total_profit/(len(completed)*10)*100) if completed else 0,
                "by_rule": {},
                "predictions": data
            })
        except:
            return jsonify({"error": "No data found. Run backtest.py or run_predictions.py first."})

if __name__ == '__main__':
    print("🚀 Starting web server...")
    print("🌐 Open: https://YOUR-CODESPACE-URL-8000.githubpreview.dev")
    app.run(host='0.0.0.0', port=8000, debug=True)