from prediction_engine import FootballPredictionEngine
from demo_data import get_demo_fixtures, get_demo_team_stats, get_demo_h2h
from datetime import datetime

# Set to True to use demo data, False to use real API
USE_DEMO_MODE = True

# ⚠️ API Key (only used if USE_DEMO_MODE = False)
API_KEY = "YOUR_API_KEY_HERE"

def extract_odds(match):
    """Extract odds from match object"""
    if 'odds' in match and match['odds']:
        return match['odds']
    return None

def run_daily_predictions():
    """Main function to run predictions"""
    print("=" * 60)
    print("⚽ FOOTBALL PREDICTION ENGINE")
    print("=" * 60)
    print(f"Mode: {'🎮 DEMO' if USE_DEMO_MODE else '🌐 LIVE API'}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    engine = FootballPredictionEngine()
    
    # Get fixtures
    if USE_DEMO_MODE:
        print("\n📊 Loading demo matches...")
        fixtures = get_demo_fixtures()
    else:
        print("\n🌐 Fetching from API...")
        # API code would go here
        fixtures = []
    
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
        
        # Get odds
        odds = extract_odds(match)
        if odds:
            print(f"   Odds: H-{odds['home']:.2f} | D-{odds['draw']:.2f} | A-{odds['away']:.2f}")
        
        # Get stats (demo mode)
        team_stats = match.get('team_stats') or get_demo_team_stats(match['awayTeam']['id'])
        h2h_stats = match.get('h2h_stats') or get_demo_h2h(match['homeTeam']['id'], match['awayTeam']['id'])
        
        # Prepare match data
        match_data = {
            'name': match_name,
            'odds': odds or {'home': 2.0, 'draw': 3.5, 'away': 3.5},
            'team_stats': team_stats,
            'h2h_stats': h2h_stats
        }
        
        # Run prediction engine
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
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    print(f"Total matches analyzed: {len(fixtures)}")
    print(f"Predictions found: {predictions_count}")
    print(f"Match rate: {predictions_count/len(fixtures)*100:.1f}%")
    
    if rule_stats:
        print("\n📊 By Rule:")
        for rule, count in sorted(rule_stats.items()):
            print(f"   {rule}: {count} predictions")
    
    print("=" * 60)
    print("✅ Demo test complete!")
    print("💡 Tip: Set USE_DEMO_MODE = False to connect real API later")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_predictions()
