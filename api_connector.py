import requests
import json
from datetime import datetime

class FootballAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "v3.football.api-sports.io"
        }
    
    def get_fixtures(self, date=None, league=None, season=2024):
        """Get upcoming matches"""
        url = f"{self.base_url}/fixtures"
        params = {}
        
        if date:
            params['date'] = date
        else:
            params['next'] = 50  # Get next 50 matches
        
        if league:
            params['league'] = league
            params['season'] = season
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', [])
        except Exception as e:
            print(f"Error fetching fixtures: {e}")
            return []
    
    def get_odds(self, fixture_id):
        """Get odds for a specific match"""
        url = f"{self.base_url}/odds"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', [])
        except Exception as e:
            print(f"Error fetching odds: {e}")
            return []
    
    def get_h2h(self, team1_id, team2_id, last=10):
        """Get head-to-head history"""
        url = f"{self.base_url}/teams/h2h"
        params = {
            'h2h': f"{team1_id}-{team2_id}",
            'last': last
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', [])
        except Exception as e:
            print(f"Error fetching H2H: {e}")
            return []
    
    def get_team_stats(self, team_id, season=2024, league=39):
        """Get team statistics"""
        url = f"{self.base_url}/teams/statistics"
        params = {
            'league': league,
            'season': season,
            'team': team_id
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', {})
        except Exception as e:
            print(f"Error fetching team stats: {e}")
            return {}

# Test the connection
if __name__ == "__main__":
    print("Testing API Connection...")
    print("Replace 'YOUR_API_KEY' with your actual API key from api-football.com")
    print("\nExample usage:")
    print("api = FootballAPI('your_api_key_here')")
    print("fixtures = api.get_fixtures()")
