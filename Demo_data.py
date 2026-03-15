"""
Demo data for testing prediction engine without external API
Realistic upcoming matches with odds for your 5 rules
"""

def get_demo_fixtures():
    """Return list of demo matches with realistic odds"""
    return [
        # Rule 1: Home 1.20-1.29 (excl 1.25) vs Away >= 10.00
        {
            "id": 101,
            "homeTeam": {"name": "Manchester City", "id": 65},
            "awayTeam": {"name": "Luton Town", "id": 389},
            "utcDate": "2026-03-16T15:00:00Z",
            "odds": {
                "home": 1.22,
                "draw": 6.50,
                "away": 11.00
            },
            "competition": {"name": "Premier League"}
        },
        # Rule 2: Home 1.30-1.35 vs Away >= 12.00
        {
            "id": 102,
            "homeTeam": {"name": "Bayern Munich", "id": 5},
            "awayTeam": {"name": "Darmstadt", "id": 55},
            "utcDate": "2026-03-16T17:30:00Z",
            "odds": {
                "home": 1.32,
                "draw": 5.20,
                "away": 13.00
            },
            "competition": {"name": "Bundesliga"}
        },
        # Rule 3: Home 1.90-1.99
        {
            "id": 103,
            "homeTeam": {"name": "Liverpool", "id": 64},
            "awayTeam": {"name": "Chelsea", "id": 61},
            "utcDate": "2026-03-16T16:30:00Z",
            "odds": {
                "home": 1.95,
                "draw": 3.80,
                "away": 3.90
            },
            "competition": {"name": "Premier League"}
        },
        # Rule 4: Draw ~3.5, Away < Home, Over 1.5 stats
        {
            "id": 104,
            "homeTeam": {"name": "Wolves", "id": 76},
            "awayTeam": {"name": "Aston Villa", "id": 58},
            "utcDate": "2026-03-16T14:00:00Z",
            "odds": {
                "home": 2.10,
                "draw": 3.50,
                "away": 1.80
            },
            "competition": {"name": "Premier League"},
            "team_stats": {"away_over_1_5_last_10": 9}
        },
        # Rule 5: H2H probability 22%-33%
        {
            "id": 105,
            "homeTeam": {"name": "Everton", "id": 62},
            "awayTeam": {"name": "Fulham", "id": 63},
            "utcDate": "2026-03-16T19:00:00Z",
            "odds": {
                "home": 2.50,
                "draw": 3.20,
                "away": 2.80
            },
            "competition": {"name": "Premier League"},
            "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}
        },
        # Control: Should NOT match any rule
        {
            "id": 106,
            "homeTeam": {"name": "Arsenal", "id": 57},
            "awayTeam": {"name": "Tottenham", "id": 73},
            "utcDate": "2026-03-17T16:30:00Z",
            "odds": {
                "home": 1.50,
                "draw": 4.20,
                "away": 6.00
            },
            "competition": {"name": "Premier League"}
        },
        # Extra matches for variety
        {
            "id": 107,
            "homeTeam": {"name": "Real Madrid", "id": 86},
            "awayTeam": {"name": "Getafe", "id": 94},
            "utcDate": "2026-03-16T20:00:00Z",
            "odds": {
                "home": 1.28,
                "draw": 5.50,
                "away": 10.50
            },
            "competition": {"name": "La Liga"}
        },
        {
            "id": 108,
            "homeTeam": {"name": "Inter Milan", "id": 108},
            "awayTeam": {"name": "Empoli", "id": 115},
            "utcDate": "2026-03-16T19:45:00Z",
            "odds": {
                "home": 1.33,
                "draw": 5.00,
                "away": 12.00
            },
            "competition": {"name": "Serie A"}
        }
    ]

def get_demo_team_stats(team_id):
    """Return demo team statistics"""
    return {
        "away_over_1_5_last_10": 7,  # Default: 7/10 matches over 1.5 goals
        "form": "W-W-D-W-L",
        "goals_scored_avg": 1.8,
        "goals_conceded_avg": 1.1
    }

def get_demo_h2h(team1_id, team2_id):
    """Return demo head-to-head stats"""
    return {
        "total_matches": 10,
        "ht_under_1_5_count": 3,  # 30% probability
        "last_5_results": ["H", "A", "D", "H", "A"]
    }

if __name__ == "__main__":
    print("Demo Data Loaded")
    fixtures = get_demo_fixtures()
    print(f"Available demo matches: {len(fixtures)}")
    for f in fixtures:
        print(f"- {f['homeTeam']['name']} vs {f['awayTeam']['name']}")
