import requests
import json
from datetime import datetime

class FootballAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    
    def get_fixtures(self, date=None, league=None, season=2024):
        url = f"{self.base_url}/fixtures"
        params = {}
        if date:
            params['date'] = date
        else:
            params['next'] = 50
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
        url = f"{self.base_url}/teams/h2h"
        params = {'h2h': f"{team1_id}-{team2_id}", 'last': last}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', [])
        except Exception as e:
            print(f"Error fetching H2H: {e}")
            return []
    
    def get_team_stats(self, team_id, season=2024, league=39):
        url = f"{self.base_url}/teams/statistics"
        params = {'league': league, 'season': season, 'team': team_id}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', {})
        except Exception as e:
            print(f"Error fetching team stats: {e}")
            return {}

if __name__ == "__main__":
    print("API Connector Loaded Successfully")
