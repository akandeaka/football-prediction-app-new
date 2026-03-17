from datetime import datetime, timedelta

def get_real_fixtures():
    """
    TODAY'S REAL MATCHES - Update this daily
    Get odds from: https://www.oddsportal.com or your bookmaker
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # ============================================
    # UPDATE THIS SECTION DAILY WITH REAL MATCHES
    # ============================================
    return [
        # Example: Update with today's actual matches
        {
            "id": 1,
            "home": "Manchester City",
            "away": "Luton Town",
            "odds": {"home": 1.22, "draw": 6.50, "away": 11.00},
            "date": f"{today}T15:00:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 9},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3, "draw_count": 4},
            "league_info": {"is_low_scoring": False, "draw_probability": 45}
        },
        {
            "id": 2,
            "home": "Liverpool",
            "away": "Chelsea",
            "odds": {"home": 1.95, "draw": 3.80, "away": 3.90},
            "date": f"{today}T16:30:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 8},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3, "draw_count": 5},
            "league_info": {"is_low_scoring": False, "draw_probability": 48}
        },
        {
            "id": 3,
            "home": "Arsenal",
            "away": "Tottenham",
            "odds": {"home": 1.85, "draw": 3.70, "away": 4.20},
            "date": f"{today}T14:00:00Z",
            "league": "Premier League",
            "team_stats": {"away_over_1_5_last_10": 7},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 2, "draw_count": 3},
            "league_info": {"is_low_scoring": False, "draw_probability": 42}
        },
        {
            "id": 4,
            "home": "Bayern Munich",
            "away": "Darmstadt",
            "odds": {"home": 1.32, "draw": 5.20, "away": 13.00},
            "date": f"{today}T17:30:00Z",
            "league": "Bundesliga",
            "team_stats": {"away_over_1_5_last_10": 8},
            "h2h_stats": {"total_matches": 8, "ht_under_1_5_count": 2, "draw_count": 2},
            "league_info": {"is_low_scoring": False, "draw_probability": 40}
        },
        # Add more matches as needed...
        # Copy the template above and fill in real match details
    ]

def get_previous_matches():
    """
    PREVIOUS MATCHES - Add completed matches here for tracking
    Include actual results (home_goals, away_goals, result)
    """
    return [
        # Example previous matches
        {
            "id": 101,
            "home": "Manchester City",
            "away": "Everton",
            "odds": {"home": 1.25, "draw": 6.00, "away": 10.00},
            "date": "2026-03-10T15:00:00Z",
            "league": "Premier League",
            "home_goals": 3,
            "away_goals": 1,
            "result": "1",  # 1=Home Win, X=Draw, 2=Away Win
            "predictions": [
                {"rule": "Rule 1", "market": "Home Win", "odds": 1.25, "status": "WIN"},
                {"rule": "Rule 5", "market": "1st Half Under 1.5", "odds": 1.25, "status": "WIN"}
            ]
        },
        {
            "id": 102,
            "home": "Liverpool",
            "away": "Brighton",
            "odds": {"home": 1.65, "draw": 4.00, "away": 5.00},
            "date": "2026-03-09T16:30:00Z",
            "league": "Premier League",
            "home_goals": 2,
            "away_goals": 1,
            "result": "1",
            "predictions": [
                {"rule": "Rule 3", "market": "Home/Draw (1X)", "odds": 1.65, "status": "WIN"}
            ]
        },
        # Add more previous matches as needed...
    ]

if __name__ == "__main__":
    print("Today's Fixtures:")
    for f in get_real_fixtures():
        print(f"  {f['home']} vs {f['away']} ({f['league']})")
    
    print("\nPrevious Matches:")
    for m in get_previous_matches():
        print(f"  {m['home']} {m['home_goals']}-{m['away_goals']} {m['away']} ({m['result']})")