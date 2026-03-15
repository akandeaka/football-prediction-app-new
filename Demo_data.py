cat > run_predictions.py << 'ENDOFFILE'
from prediction_engine import FootballPredictionEngine
from datetime import datetime

# 🎮 DEMO MODE - No API required!
USE_DEMO_MODE = True

# Demo match data (embedded so no external file needed)
def get_demo_fixtures():
    return [
        # Rule 1: Home 1.20-1.29 (excl 1.25) vs Away >= 10.00
        {"id": 101, "homeTeam": {"name": "Manchester City"}, "awayTeam": {"name": "Luton Town"}, 
         "utcDate": "2026-03-16T15:00:00Z", "odds": {"home": 1.22, "draw": 6.50, "away": 11.00},
         "competition": {"name": "Premier League"}},
        # Rule 2: Home 1.30-1.35 vs Away >= 12.00
        {"id": 102, "homeTeam": {"name": "Bayern Munich"}, "awayTeam": {"name": "Darmstadt"},
         "utcDate": "2026-03-16T17:30:00Z", "odds": {"home": 1.32, "draw": 5.20, "away": 13.00},
         "competition": {"name": "Bundesliga"}},
        # Rule 3: Home 1.90-1.99
        {"id": 103, "homeTeam": {"name": "Liverpool"}, "awayTeam": {"name": "Chelsea"},
         "utcDate": "2026-03-16T16:30:00Z", "odds": {"home": 1.95, "draw": 3.80, "away": 3.90},
         "competition": {"name": "Premier League"}},
        # Rule 4: Draw ~3.5, Away < Home, Over 1.5 stats
        {"id": 104, "homeTeam": {"name": "Wolves"}, "awayTeam": {"name": "Aston Villa"},
         "utcDate": "2026-03-16T14:00:00Z", "odds": {"home": 2.10, "draw": 3.50, "away": 1.80},
         "competition": {"name": "Premier League"}, "team_stats": {"away_over_1_5_last_10": 9}},
        # Rule 5: H2H probability 22%-33%
        {"id": 105, "homeTeam": {"name": "Everton"}, "awayTeam": {"name": "Fulham"},
         "utcDate": "2026-03-16T19:00:00Z", "odds": {"home": 2.50, "draw": 3.20, "away": 2.80},
         "competition": {"name": "Premier League"}, "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}},
        # Control: Should NOT match any rule
        {"id": 106, "homeTeam": {"name": "Arsenal"}, "awayTeam": {"name": "Tottenham"},
         "utcDate": "2026-03-17T16:30:00Z", "odds": {"home": 1.50, "draw": 4.20, "away": 6.00},
         "competition": {"name": "Premier League"}},
        # Extra: Rule 1 again
        {"id": 107, "homeTeam": {"name": "Real Madrid"}, "awayTeam": {"name": "Getafe"},
         "utcDate": "2026-03-16T20:00:00Z", "odds": {"home": 1.28, "draw": 5.50, "away": 10.50},
         "competition": {"name": "La Liga"}},
        # Extra: Rule 2 again
        {"id": 108, "homeTeam": {"name": "Inter Milan"}, "awayTeam": {"name": "Empoli"},
         "utcDate": "2026-03-16T19:45:00Z", "odds": {"home": 1.33, "draw": 5.00, "away": 12.00},
         "competition": {"name": "Serie A"}}
    ]

def get_default_team_stats():
    return {"away_over_1_5_last_10": 7}

def get_default_h2h():
    return {"total_matches": 10, "ht_under_1_5_count": 3}

def run_daily_predictions():
    print("=" * 60)
    print("⚽ FOOTBALL PREDICTION ENGINE")
    print("=" * 60)
    print(f"Mode: {'🎮 DEMO' if USE_DEMO_MODE else '🌐 LIVE API'}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    engine = FootballPredictionEngine()
    
    if USE_DEMO_MODE:
        print("\n📊 Loading demo matches...")
        fixtures = get_demo_fixtures()
    else:
        print("\n❌ API mode not configured yet")
        return
    
    if not fixtures:
        print("❌ No matches found")
        return
    
    print(f"✅ Found {len(fixtures)} matches\n")
    
    predictions_count = 0
    rule_stats = {}
    
    for match in fixtures:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        competition = match.get('competition', {}).get('name', 'Unknown')
        match_name = f"{home} vs {away}"
        
        print(f"🔍 Analyzing: {match_name}")
        print(f"   League: {competition}")
        
        odds = match.get('odds', {})
        if odds:
            print(f"   Odds: H-{odds['home']:.2f} | D-{odds['draw']:.2f} | A-{odds['away']:.2f}")
        
        team_stats = match.get('team_stats') or get_default_team_stats()
        h2h_stats = match.get('h2h_stats') or get_default_h2h()
        
        match_data = {
            'name': match_name,
            'odds': odds or {'home': 2.0, 'draw': 3.5, 'away': 3.5},
            'team_stats': team_stats,
            'h2h_stats': h2h_stats
        }
        
        predictions = engine.process_match(match_data)
        
        if predictions:
            print("   ✅ PREDICTIONS:")
            for p in predictions:
                rule = p['rule']
                rule_stats[rule] = rule_stats.get(rule, 0) + 1
                print(f"      🎯 {rule}: {p['market']} ({p['confidence']})")
            predictions_count += 1
        else:
            print("   ❌ No predictions matched")
        print("   " + "-" * 50)
    
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    print(f"Total matches analyzed: {len(fixtures)}")
    print(f"Predictions found: {predictions_count}")
    if fixtures:
        print(f"Match rate: {predictions_count/len(fixtures)*100:.1f}%")
    if rule_stats:
        print("\n📊 By Rule:")
        for rule, count in sorted(rule_stats.items()):
            print(f"   {rule}: {count} predictions")
    print("=" * 60)
    print("✅ Demo test complete!")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_predictions()
ENDOFFILE
