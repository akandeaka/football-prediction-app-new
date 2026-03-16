from prediction_engine import FootballPredictionEngine
from results_tracker import ResultsTracker
from datetime import datetime

def get_demo_fixtures():
    return [
        {"id": 101, "homeTeam": {"name": "Manchester City"}, "awayTeam": {"name": "Luton Town"}, 
         "odds": {"home": 1.22, "draw": 6.50, "away": 11.00}},
        {"id": 102, "homeTeam": {"name": "Bayern Munich"}, "awayTeam": {"name": "Darmstadt"},
         "odds": {"home": 1.32, "draw": 5.20, "away": 13.00}},
        {"id": 103, "homeTeam": {"name": "Liverpool"}, "awayTeam": {"name": "Chelsea"},
         "odds": {"home": 1.95, "draw": 3.80, "away": 3.90}},
        {"id": 104, "homeTeam": {"name": "Wolves"}, "awayTeam": {"name": "Aston Villa"},
         "odds": {"home": 2.10, "draw": 3.50, "away": 1.80},
         "team_stats": {"away_over_1_5_last_10": 9}},
        {"id": 105, "homeTeam": {"name": "Everton"}, "awayTeam": {"name": "Fulham"},
         "odds": {"home": 2.50, "draw": 3.20, "away": 2.80},
         "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}},
        {"id": 106, "homeTeam": {"name": "Arsenal"}, "awayTeam": {"name": "Tottenham"},
         "odds": {"home": 1.50, "draw": 4.20, "away": 6.00}}
    ]

def run_daily_predictions():
    print("=" * 60)
    print("FOOTBALL PREDICTION ENGINE")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    engine = FootballPredictionEngine()
    tracker = ResultsTracker()
    fixtures = get_demo_fixtures()
    
    print(f"\nFound {len(fixtures)} matches\n")
    
    predictions_count = 0
    
    for match in fixtures:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        match_name = f"{home} vs {away}"
        
        print(f"Analyzing: {match_name}")
        odds = match.get('odds', {})
        print(f"  Odds: H-{odds['home']} | D-{odds['draw']} | A-{odds['away']}")
        
        team_stats = match.get('team_stats', {'away_over_1_5_last_10': 7})
        h2h_stats = match.get('h2h_stats', {'total_matches': 10, 'ht_under_1_5_count': 3})
        
        match_data = {
            'name': match_name,
            'odds': odds,
            'team_stats': team_stats,
            'h2h_stats': h2h_stats
        }
        
        predictions = engine.process_match(match_data)
        
        if predictions:
            print("  PREDICTIONS FOUND:")
            for p in predictions:
                print(f"    - {p['rule']}: {p['market']}")
                # THIS LINE SAVES TO JSON - MAKE SURE IT EXISTS
                tracker.save_prediction(
                    match_name=match_name,
                    rule=p['rule'],
                    market=p['market'],
                    odds=odds.get('home', 2.0)
                )
            predictions_count += 1
        else:
            print("  No predictions matched")
        print("-" * 50)
    
    print(f"\nSUMMARY: {predictions_count}/{len(fixtures)} matches matched")
    tracker.print_report()

if __name__ == "__main__":
    run_daily_predictions()
