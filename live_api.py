import requests
import json
from datetime import datetime

class LiveAPI:
    def __init__(self, api_key=None):
        self.api_key = "3e8db2b7b5a34ca59a36653b924dd10b"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}
    
    def get_fixtures(self, days=7):
        """Get upcoming fixtures"""
        if self.api_key == "YOUR_API_KEY_HERE":
            print("⚠️  API key not configured. Using demo data.")
            return []
        
        url = f"{self.base_url}/matches"
        params = {"matchStatus": "SCHEDULED", "timeFrame": f"START{days}"}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('matches', [])
        except Exception as e:
            print(f"API Error: {e}")
            return []
    
    def format_for_engine(self, fixtures):
    """Convert API response to engine format"""
    formatted = []
    for match in fixtures:
        # Extract odds (simplified - API may not always have odds)
        odds = self._extract_odds(match)
        
        formatted.append({
            'name': f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}",
            'odds': odds,
            'team_stats': {
                'away_over_1_5_last_10': 7  # Default value (need historical data)
            },
            'h2h_stats': {
                'total_matches': 10,
                'ht_under_1_5_count': 3,
                'draw_count': 4
            },
            'league_info': {
                'is_low_scoring': False,
                'draw_probability': 45
            },
            'date': match.get('utcDate', ''),
            'league': match.get('competition', {}).get('name', 'Unknown')
        })
    return formatted
        
        
        
    
    def _extract_odds(self, match):
        """Extract odds from match data"""
        odds = match.get('odds', {})
        if not odds:
            return {"home": 2.0, "draw": 3.5, "away": 3.5}
        
        # Simplified odds extraction
        return {
            "home": 2.0,
            "draw": 3.5,
            "away": 3.5
        }
    
    def test_connection(self):
        """Test if API key works"""
        if self.api_key == "YOUR_API_KEY_HERE":
            return False, "API key not configured"
        
        try:
            response = requests.get(
                f"{self.base_url}/competitions",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                return True, "API connected successfully"
            return False, f"API error: {response.status_code}"
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    api = LiveAPI()
    success, message = api.test_connection()
    print(f"API Test: {'✅' if success else '❌'} {message}")
    
    if success:
        fixtures = api.get_fixtures(days=3)
        print(f"Found {len(fixtures)} upcoming matches")
