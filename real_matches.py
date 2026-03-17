"""
Add YOUR Real Upcoming Matches Here
Edit this file before each matchday
"""

def get_real_fixtures():
    """
    Add real upcoming matches with actual odds
    Format: home, away, home_odds, draw_odds, away_odds
    """
    return [
        # Example: Edit these with REAL upcoming matches
        {
            "id": 1,
            "home": "Manchester City",
            "away": "Luton Town",
            "odds": {"home": 1.22, "draw": 6.50, "away": 11.00},
            "date": "2026-03-17T15:00:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 9},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3, "draw_count": 4},
            "league_info": {"is_low_scoring": False, "draw_probability": 45}
        },
        {
            "id": 2,
            "home": "Bayern Munich",
            "away": "Darmstadt",
            "odds": {"home": 1.32, "draw": 5.20, "away": 13.00},
            "date": "2026-03-17T17:30:00Z",
            "league": "Bundesliga",
            "team_stats": {"away_over_1_5_last_10": 8},
            "h2h_stats": {"total_matches": 8, "ht_under_1_5_count": 2, "draw_count": 2},
            "league_info": {"is_low_scoring": False, "draw_probability": 40}
        },
        {
            "id": 3,
            "home": "Liverpool",
            "away": "Chelsea",
            "odds": {"home": 1.95, "draw": 3.80, "away": 3.90},
            "date": "2026-03-17T16:30:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 8},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3, "draw_count": 5},
            "league_info": {"is_low_scoring": False, "draw_probability": 48}
        },
        {
            "id": 4,
            "home": "Newcastle",
            "away": "Wolves",
            "odds": {"home": 1.75, "draw": 3.60, "away": 4.50},
            "date": "2026-03-17T14:00:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 7},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 4, "draw_count": 3},
            "league_info": {"is_low_scoring": False, "draw_probability": 42}
        },
        {
            "id": 5,
            "home": "Everton",
            "away": "Fulham",
            "odds": {"home": 2.50, "draw": 3.20, "away": 2.80},
            "date": "2026-03-17T19:00:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 6},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3, "draw_count": 6},
            "league_info": {"is_low_scoring": True, "draw_probability": 52}
        },
        # ADD MORE MATCHES HERE
    ]

if __name__ == "__main__":
    fixtures = get_real_fixtures()
    print(f"Real fixtures loaded: {len(fixtures)} matches")
    for f in fixtures:
        print(f"  {f['home']} vs {f['away']} ({f['league']})")