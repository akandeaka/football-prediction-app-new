from prediction_engine import FootballPredictionEngine
import json
import random
from datetime import datetime, timedelta

# 📊 SAMPLE HISTORICAL DATASET (50 realistic matches)
# Format: match result = 1=Home Win, X=Draw, 2=Away Win, goals = total goals
SAMPLE_DATA = []

# Generate 50 realistic demo matches
teams = [
    ("Man City", 1.25, 6.0, 10.0), ("Bayern", 1.30, 5.5, 11.0),
    ("Liverpool", 1.80, 3.8, 4.2), ("Real Madrid", 1.40, 4.8, 7.5),
    ("Arsenal", 2.10, 3.4, 3.3), ("Chelsea", 2.30, 3.3, 3.0),
    ("Luton", 8.0, 4.5, 1.40), ("Darmstadt", 9.0, 5.0, 1.35),
    ("Wolves", 2.40, 3.2, 2.9), ("Aston Villa", 2.0, 3.5, 3.6),
    ("Everton", 2.6, 3.2, 2.7), ("Fulham", 2.5, 3.3, 2.8),
    ("Tottenham", 2.2, 3.4, 3.1), ("Newcastle", 1.9, 3.6, 4.0)
]

random.seed(42)  # For reproducible results

for i in range(50):
    home, h_odd, d_odd, a_odd = random.choice(teams)
    away, _, _, _ = random.choice(teams)
    while away == home:
        away, _, _, _ = random.choice(teams)
    
    # Simulate realistic odds variation
    h_odd = round(h_odd + random.uniform(-0.15, 0.15), 2)
    d_odd = round(d_odd + random.uniform(-0.3, 0.3), 2)
    a_odd = round(a_odd + random.uniform(-0.2, 0.2), 2)
    
    # Simulate realistic result based on odds (favorite wins more often)
    if h_odd < 1.5:
        result = random.choices([1, 'X', 2], weights=[0.75, 0.15, 0.10])[0]
        goals = random.choices([2, 3, 4, 1], weights=[0.4, 0.3, 0.2, 0.1])[0]
    elif h_odd < 2.0:
        result = random.choices([1, 'X', 2], weights=[0.50, 0.25, 0.25])[0]
        goals = random.choices([2, 3, 1, 4], weights=[0.35, 0.3, 0.25, 0.1])[0]
    else:
        result = random.choices([1, 'X', 2], weights=[0.35, 0.30, 0.35])[0]
        goals = random.choices([2, 1, 3, 0], weights=[0.3, 0.3, 0.25, 0.15])[0]
    
    # H2H stats for Rule 5 (30% chance to match criteria)
    h2h_total = random.choice([10, 12, 15])
    h2h_under = int(h2h_total * random.uniform(0.20, 0.35)) if random.random() < 0.3 else random.randint(0, h2h_total)
    
    SAMPLE_DATA.append({
        "id": i+1,
        "home": home, "away": away,
        "odds": {"home": h_odd, "draw": d_odd, "away": a_odd},
        "result": result,  # 1, X, or 2
        "goals": goals,
        "ht_goals": random.randint(0, 2),  # For Rule 5
        "team_stats": {"away_over_1_5_last_10": random.randint(5, 10)},
        "h2h_stats": {"total_matches": h2h_total, "ht_under_1_5_count": h2h_under}
    })

def run_backtest():
    print("=" * 70)
    print("⚽ FOOTBALL PREDICTION - BACKTESTING SYSTEM")
    print("=" * 70)
    print(f"Dataset: {len(SAMPLE_DATA)} historical matches (simulated)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    engine = FootballPredictionEngine()
    
    # Track results
    all_predictions = []
    rule_stats = {}
    
    for match in SAMPLE_DATA:
        match_name = f"{match['home']} vs {match['away']}"
        odds = match['odds']
        
        match_data = {
            'name': match_name,
            'odds': odds,
            'team_stats': match['team_stats'],
            'h2h_stats': match['h2h_stats']
        }
        
        predictions = engine.process_match(match_data)
        
        for p in predictions:
            rule = p['rule']
            market = p['market']
            
            # Determine if prediction won
            won = False
            if market == "Home Win" and match['result'] == 1:
                won = True
            elif market == "Home/Draw (1X)" and match['result'] in [1, 'X']:
                won = True
            elif market == "Over 1.5 Goals" and match['goals'] >= 2:
                won = True
            elif market == "1st Half Under 1.5" and match['ht_goals'] <= 1:
                won = True
            
            # Track stats
            if rule not in rule_stats:
                rule_stats[rule] = {"total": 0, "wins": 0, "profit": 0}
            
            rule_stats[rule]["total"] += 1
            stake = 10
            if won:
                rule_stats[rule]["wins"] += 1
                rule_stats[rule]["profit"] += stake * (odds['home'] - 1)
            else:
                rule_stats[rule]["profit"] -= stake
            
            all_predictions.append({
                "match": match_name,
                "rule": rule,
                "market": market,
                "odds": odds['home'],
                "result": "WIN" if won else "LOSS",
                "profit": stake * (odds['home'] - 1) if won else -stake
            })
    
    # Generate Report
    total_predictions = len(all_predictions)
    total_wins = sum(1 for p in all_predictions if p['result'] == 'WIN')
    total_profit = sum(p['profit'] for p in all_predictions)
    win_rate = (total_wins / total_predictions * 100) if total_predictions > 0 else 0
    
    print(f"\n📊 BACKTEST RESULTS")
    print(f"Total Matches Analyzed: {len(SAMPLE_DATA)}")
    print(f"Predictions Generated: {total_predictions}")
    print(f"Win Rate: {win_rate:.1f}%")
    print(f"Total Profit (per $10 stake): ${total_profit:.2f}")
    print(f"ROI: {(total_profit / (total_predictions * 10) * 100):.1f}%")
    
    print(f"\n📈 Performance by Rule:")
    for rule, stats in sorted(rule_stats.items()):
        rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
        roi = (stats['profit'] / (stats['total'] * 10) * 100)
        print(f"  {rule}: {stats['wins']}/{stats['total']} ({rate:.0f}%) | ROI: {roi:+.1f}% | Profit: ${stats['profit']:.2f}")
    
    # Save to file
    report = {
        "date": datetime.now().isoformat(),
        "total_matches": len(SAMPLE_DATA),
        "total_predictions": total_predictions,
        "win_rate": win_rate,
        "total_profit": total_profit,
        "roi": (total_profit / (total_predictions * 10) * 100) if total_predictions > 0 else 0,
        "by_rule": rule_stats,
        "predictions": all_predictions
    }
    
    with open('backtest_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved to: backtest_report.json")
    print("=" * 70)

if __name__ == "__main__":
    run_backtest()