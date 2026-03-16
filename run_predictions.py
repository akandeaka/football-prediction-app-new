from prediction_engine import FootballPredictionEngine
from results_tracker import ResultsTracker
from datetime import datetime

USE_DEMO_MODE = True

def get_demo_fixtures():
    return [
        {"id": 101, "homeTeam": {"name": "Manchester City"}, "awayTeam": {"name": "Luton Town"}, 
         "utcDate": "2026-03-16T15:00:00Z", "odds": {"home": 1.22, "draw": 6.50, "away": 11.00},
         "competition": {"name": "Premier League"}},
        {"id": 102, "homeTeam": {"name": "Bayern Munich"}, "awayTeam": {"name": "Darmstadt"},
         "utcDate": "2026-03-16T17:30:00Z", "odds": {"home": 1.32, "draw": 5.20, "away": 13.00},
         "competition": {"name": "Bundesliga"}},
        {"id": 103, "homeTeam": {"name": "Liverpool"}, "awayTeam": {"name": "Chelsea"},
         "utcDate": "2026-03-16T16:30:00Z", "odds": {"home": 1.95, "draw": 3.80, "away": 3.90},
         "competition": {"name": "Premier League"}},
        {"id": 104, "homeTeam": {"name": "Wolves"}, "awayTeam": {"name": "Aston Villa"},
         "utcDate": "2026-03-16T14:00:00Z", "odds": {"home": 2.10, "draw": 3.50, "away": 1.80},
         "competition": {"name": "Premier League"}, "team_stats": {"away_over_1_5_last_10": 9}},
        {"id": 105, "homeTeam": {"name": "Everton"}, "awayTeam": {"name": "Fulham"},
         "utcDate": "2026-03-16T19:00:00Z", "odds": {"home": 2.50, "draw": 3.20, "away": 2.80},
         "competition": {"name": "Premier League"}, "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}},
        {"id": 106, "homeTeam": {"name": "Arsenal"}, "awayTeam": {"name": "Tottenham"},
         "utcDate": "2026-03-17T16:30:00Z", "odds": {"home": 1.50, "draw": 4.20, "away": 6.00},
         "competition": {"name": "Premier League"}}
    ]

def run_daily_predictions():
    print("=" * 60)
    print("FOOTBALL PREDICTION ENGINE")
    print("=" * 60)
    print(f"Mode: DEMO")
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
                # Save to tracker
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
    print("=" * 60)
    
    # Show tracker report
    tracker.print_report()

if __name__ == "__main__":
    run_daily_predictions()
