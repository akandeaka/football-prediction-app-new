from prediction_engine import FootballPredictionEngine
from api_connector import FootballAPI
from datetime import datetime
import json

# ⚠️ REPLACE THIS WITH YOUR API KEY
API_KEY = "5fa07bc20ebdb76e4fb2833142a5c207"

def extract_odds(odds_data):
    """Extract home/draw/away odds from API response"""
    if not odds_data:
        return None
    
    bookmaker = odds_data[0].get('bookmakers', [{}])[0]
    bets = bookmaker.get('bets', [])
    
    for bet in bets:
        if bet.get('name') == 'Match Winner':
            values = {v['value']: v['odd'] for v in bet.get('values', [])}
            return {
                'home': float(values.get('Home', 0)),
                'draw': float(values.get('Draw', 0)),
                'away': float(values.get('Away', 0))
            }
    return None

def calculate_team_form(team_id, api):
    """Calculate over 1.5 goals in last 10 matches"""
    # This is a simplified version - you'd need to fetch actual match history
    # For now, return a placeholder
    return {'away_over_1_5_last_10': 5}

def calculate_h2h_stats(h2h_matches):
    """Calculate H2H statistics"""
    total = len(h2h_matches)
    if total == 0:
        return {'total_matches': 0, 'ht_under_1_5_count': 0}
    
    ht_under_1_5 = 0
    for match in h2h_matches:
        goals = match['goals']
        ht_goals = goals.get('halftime', 0)
        if isinstance(ht_goals, int) and ht_goals < 2:
            ht_under_1_5 += 1
    
    return {
        'total_matches': total,
        'ht_under_1_5_count': ht_under_1_5
    }

def run_daily_predictions():
    """Main function to run predictions"""
    print("=" * 50)
    print("FOOTBALL PREDICTION ENGINE - LIVE MODE")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ ERROR: Please add your API key in run_predictions.py")
        print("Get your key from: https://api-football.com")
        return
    
    # Initialize
    api = FootballAPI(API_KEY)
    engine = FootballPredictionEngine()
    
    # Get today's fixtures
    print("\n📅 Fetching upcoming matches...")
    fixtures = api.get_fixtures()
    
    if not fixtures:
        print("❌ No fixtures found or API error")
        return
    
    print(f"✅ Found {len(fixtures)} upcoming matches\n")
    
    predictions_count = 0
    
    # Process each match
    for fixture in fixtures[:20]:  # Limit to first 20 for testing
        match_name = f"{fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}"
        fixture_id = fixture['fixture']['id']
        
        print(f"Analyzing: {match_name}")
        
        # Get odds
        odds_data = api.get_odds(fixture_id)
        odds = extract_odds(odds_data)
        
        if not odds:
            print("  ⚠️  No odds available, skipping...")
            continue
        
        print(f"  Odds: H-{odds['home']} | D-{odds['draw']} | A-{odds['away']}")
        
        # Get team stats (simplified)
        team_stats = calculate_team_form(
            fixture['teams']['away']['id'], 
            api
        )
        
        # Get H2H stats
        h2h_matches = api.get_h2h(
            fixture['teams']['home']['id'],
            fixture['teams']['away']['id'],
            last=10
        )
        h2h_stats = calculate_h2h_stats(h2h_matches)
        
        # Prepare match data
        match_data = {
            'name': match_name,
            'odds': odds,
            'team_stats': team_stats,
            'h2h_stats': h2h_stats
        }
        
        # Run predictions
        predictions = engine.process_match(match_data)
        
        if predictions:
            print("  ✅ PREDICTIONS FOUND:")
            for p in predictions:
                print(f"     🎯 {p['rule']}: {p['market']} ({p['confidence']})")
            predictions_count += 1
        else:
            print("  ❌ No predictions matched")
        
        print("-" * 50)
    
    print("\n" + "=" * 50)
    print(f"SUMMARY: {predictions_count} predictions found from {len(fixtures[:20])} matches")
    print("=" * 50)

if __name__ == "__main__":
    run_daily_predictions()
