from final_engine import FinalPredictionEngine
import json
import random

# Generate 500 matches with data for all 7 rules
SAMPLE_DATA = []
teams = [
    ("Man City", 1.25, 6.0, 10.0, 0.78), ("Bayern", 1.32, 5.5, 11.0, 0.75),
    ("Liverpool", 1.95, 3.8, 4.0, 0.58), ("Real Madrid", 1.40, 4.8, 7.5, 0.70),
    ("Arsenal", 2.10, 3.4, 3.3, 0.50), ("Chelsea", 2.30, 3.3, 3.0, 0.47),
    ("Luton", 8.0, 4.5, 1.40, 0.12), ("Darmstadt", 9.0, 5.0, 1.35, 0.10),
    ("Wolves", 2.40, 3.5, 2.9, 0.44), ("Aston Villa", 2.0, 3.5, 3.6, 0.52),
    ("Everton", 2.6, 3.2, 2.7, 0.42), ("Fulham", 2.5, 3.3, 2.8, 0.43),
    ("Tottenham", 2.2, 3.4, 3.1, 0.48), ("Newcastle", 1.75, 3.6, 4.0, 0.54)
]

random.seed(42)

for i in range(500):
    home, h_odd, d_odd, a_odd, home_win_prob = random.choice(teams)
    away, _, _, _, _ = random.choice(teams)
    while away == home:
        away, _, _, _, _ = random.choice(teams)
    
    h_odd = round(h_odd + random.uniform(-0.10, 0.10), 2)
    d_odd = round(d_odd + random.uniform(-0.20, 0.20), 2)
    a_odd = round(a_odd + random.uniform(-0.15, 0.15), 2)
    
    result = random.choices([1, 'X', 2], weights=[home_win_prob, 0.28, 1-home_win_prob-0.28])[0]
    goals = random.choices([0,1,2,3,4,5], weights=[0.08,0.15,0.30,0.25,0.14,0.08])[0]
    ht_goals = random.choices([0,1,2], weights=[0.35,0.45,0.20])[0]
    btts = 1 if random.random() < 0.52 else 0
    
    h2h_total = random.choice([5, 8, 10, 12])
    h2h_draws = int(h2h_total * random.uniform(0.30, 0.60))  # For Rule 6
    h2h_under = int(h2h_total * random.uniform(0.20, 0.35))  # For Rule 5
    
    # League info for Rule 6
    is_low_scoring = random.choice([True, False])
    draw_probability = random.randint(35, 60)  # Forebet probability
    
    SAMPLE_DATA.append({
        "id": i+1, "home": home, "away": away,
        "odds": {"home": h_odd, "draw": d_odd, "away": a_odd},
        "result": result, "goals": goals, "ht_goals": ht_goals, "btts": btts,
        "team_stats": {
            "away_over_1_5_last_10": random.randint(5, 10)
        },
        "h2h_stats": {
            "total_matches": h2h_total,
            "ht_under_1_5_count": h2h_under,
            "draw_count": h2h_draws
        },
        "league_info": {
            "is_low_scoring": is_low_scoring,
            "draw_probability": draw_probability
        }
    })

def run_backtest():
    print("=" * 70)
    print("⚽ YOUR 7 RULES - COMPLETE BACKTEST (500 Matches)")
    print("=" * 70)
    
    engine = FinalPredictionEngine()
    rule_stats = {}
    all_predictions = []
    
    for match in SAMPLE_DATA:
        match_name = f"{match['home']} vs {match['away']}"
        match_data = {
            'name': match_name,
            'odds': match['odds'],
            'team_stats': match['team_stats'],
            'h2h_stats': match['h2h_stats'],
            'league_info': match['league_info']
        }
        
        predictions = engine.process_match(match_data)
        
        for p in predictions:
            rule = p['rule']
            market = p['market']
            
            won = False
            if market == "Home Win" and match['result'] == 1: won = True
            elif market == "Home/Draw (1X)" and match['result'] in [1, 'X']: won = True
            elif market == "Over 1.5 Goals" and match['goals'] >= 2: won = True
            elif market == "1st Half Under 1.5" and match['ht_goals'] <= 1: won = True
            elif market == "Draw / GG" and match['result'] == 'X': won = True
            elif market == "Draw / GG" and match['btts'] == 1: won = True
            
            if rule not in rule_stats:
                rule_stats[rule] = {"total": 0, "wins": 0, "profit": 0, "market": market}
            
            rule_stats[rule]["total"] += 1
            stake = 10
            odds = match['odds']['home']
            if won:
                rule_stats[rule]["wins"] += 1
                rule_stats[rule]["profit"] += stake * (odds - 1)
            else:
                rule_stats[rule]["profit"] -= stake
            
            all_predictions.append({
                "match": match_name, "rule": rule, "market": market,
                "odds": odds, "result": "WIN" if won else "LOSS",
                "profit": stake * (odds - 1) if won else -stake
            })
    
    total_predictions = len(all_predictions)
    total_wins = sum(1 for p in all_predictions if p['result'] == 'WIN')
    total_profit = sum(p['profit'] for p in all_predictions)
    win_rate = (total_wins / total_predictions * 100) if total_predictions > 0 else 0
    
    print(f"\n📊 YOUR 7 RULES - BACKTEST RESULTS")
    print(f"Matches Analyzed: {len(SAMPLE_DATA)}")
    print(f"Predictions Generated: {total_predictions}")
    print(f"Overall Win Rate: {win_rate:.1f}%")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"ROI: {(total_profit / (total_predictions * 10) * 100):.1f}%")
    
    print(f"\n📈 Performance by YOUR 7 Rules:")
    for rule, stats in sorted(rule_stats.items()):
        rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
        roi = (stats['profit'] / (stats['total'] * 10) * 100)
        emoji = "✅" if roi > 0 else "⚠️"
        print(f"  {rule} ({stats['market']}): {stats['wins']}/{stats['total']} ({rate:.0f}%) | ROI: {roi:+.1f}% | ${stats['profit']:.2f} {emoji}")
    
    with open('seven_rules_report.json', 'w') as f:
        json.dump({"rule_stats": rule_stats, "win_rate": win_rate, "total_profit": total_profit}, f, indent=2)
    
    print(f"\n✅ Report saved to: seven_rules_report.json")
    print("=" * 70)

if __name__ == "__main__":
    run_backtest()