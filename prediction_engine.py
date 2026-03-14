class FootballPredictionEngine:
    def __init__(self):
        self.predictions = []

    def check_rule_1(self, match):
        """Rule 1: Home 1.20-1.29 (excl 1.25) vs Away >= 10.00"""
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        
        if 1.20 <= h_odd <= 1.29 and h_odd != 1.25 and a_odd >= 10.00:
            return {"status": "PASS", "rule": "Rule 1", "market": "Home Win", "confidence": "High"}
        return {"status": "FAIL"}

    def check_rule_2(self, match):
        """Rule 2: Home 1.30-1.35 vs Away >= 12.00"""
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        
        if 1.30 <= h_odd <= 1.35 and a_odd >= 12.00:
            return {"status": "PASS", "rule": "Rule 2", "market": "Home Win", "confidence": "High"}
        return {"status": "FAIL"}

    def check_rule_3(self, match):
        """Rule 3: Home 1.90-1.99"""
        h_odd = match['odds']['home']
        
        if 1.90 <= h_odd <= 1.99:
            return {"status": "PASS", "rule": "Rule 3", "market": "Home/Draw (1X)", "confidence": "Medium"}
        return {"status": "FAIL"}

    def check_rule_4(self, match, team_stats):
        """Rule 4: Draw ~3.5, Away < Home, Over 1.5 Goals in 8/10 matches"""
        d_odd = match['odds']['draw']
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        
        if 3.40 <= d_odd <= 3.60 and a_odd < h_odd:
            if team_stats['away_over_1_5_last_10'] >= 8:
                return {"status": "PASS", "rule": "Rule 4", "market": "Over 1.5 Goals", "confidence": "Medium"}
        return {"status": "FAIL"}

    def check_rule_5(self, match, h2h_stats):
        """Rule 5: H2H First Half Under 1.5 Goals probability 22% - 33%"""
        if h2h_stats['total_matches'] < 5:
            return {"status": "FAIL", "reason": "Insufficient H2H Data"}
            
        ht_under_1_5_count = h2h_stats['ht_under_1_5_count']
        total = h2h_stats['total_matches']
        probability = ht_under_1_5_count / total
        
        if 0.22 <= probability <= 0.33:
            return {"status": "PASS", "rule": "Rule 5", "market": "1st Half Under 1.5", "confidence": "Low-Medium"}
        return {"status": "FAIL"}

    def process_match(self, match_data):
        results = []
        r1 = self.check_rule_1(match_data)
        if r1['status'] == "PASS": results.append(r1)
            
        r2 = self.check_rule_2(match_data)
        if r2['status'] == "PASS": results.append(r2)
            
        r3 = self.check_rule_3(match_data)
        if r3['status'] == "PASS": results.append(r3)
            
        r4 = self.check_rule_4(match_data, match_data['team_stats'])
        if r4['status'] == "PASS": results.append(r4)
            
        r5 = self.check_rule_5(match_data, match_data['h2h_stats'])
        if r5['status'] == "PASS": results.append(r5)
        
        return results


if __name__ == "__main__":
    # Test matches
    match_1 = {
        "name": "Man City vs Luton",
        "odds": {"home": 1.22, "draw": 6.50, "away": 11.00},
        "team_stats": {"away_over_1_5_last_10": 5},
        "h2h_stats": {"total_matches": 5, "ht_under_1_5_count": 2}
    }

    match_2 = {
        "name": "Bayern vs Darmstadt",
        "odds": {"home": 1.32, "draw": 5.00, "away": 13.00},
        "team_stats": {"away_over_1_5_last_10": 4},
        "h2h_stats": {"total_matches": 2, "ht_under_1_5_count": 1}
    }

    match_3 = {
        "name": "Liverpool vs Chelsea",
        "odds": {"home": 1.95, "draw": 3.80, "away": 3.90},
        "team_stats": {"away_over_1_5_last_10": 7},
        "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 5}
    }

    match_4 = {
        "name": "Wolves vs Aston Villa",
        "odds": {"home": 2.10, "draw": 3.50, "away": 1.80},
        "team_stats": {"away_over_1_5_last_10": 9},
        "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}
    }

    match_5 = {
        "name": "Everton vs Fulham",
        "odds": {"home": 2.50, "draw": 3.20, "away": 2.80},
        "team_stats": {"away_over_1_5_last_10": 5},
        "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 3}
    }

    match_6 = {
        "name": "Arsenal vs Spurs",
        "odds": {"home": 1.50, "draw": 4.00, "away": 6.00},
        "team_stats": {"away_over_1_5_last_10": 5},
        "h2h_stats": {"total_matches": 10, "ht_under_1_5_count": 5}
    }

    engine = FootballPredictionEngine()
    all_matches = [match_1, match_2, match_3, match_4, match_5, match_6]

    print("--- STARTING PREDICTION TEST ---\n")

    for match in all_matches:
        print(f"Analyzing: {match['name']}")
        print(f"Odds: H-{match['odds']['home']} | D-{match['odds']['draw']} | A-{match['odds']['away']}")
        
        predictions = engine.process_match(match)
        
        if len(predictions) > 0:
            print("✅ PREDICTIONS FOUND:")
            for p in predictions:
                print(f"   - {p['rule']}: {p['market']} ({p['confidence']})")
        else:
            print("❌ No predictions matched for this game.")
        
        print("-" * 30)

    print("\n--- TEST COMPLETE ---")
