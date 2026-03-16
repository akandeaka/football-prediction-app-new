class FootballPredictionEngine:
    def __init__(self):
        self.predictions = []

    def check_rule_1(self, match):
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        if 1.20 <= h_odd <= 1.29 and h_odd != 1.25 and a_odd >= 10.00:
            return {"status": "PASS", "rule": "Rule 1", "market": "Home Win", "confidence": "High"}
        return {"status": "FAIL"}

    def check_rule_2(self, match):
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        if 1.30 <= h_odd <= 1.35 and a_odd >= 12.00:
            return {"status": "PASS", "rule": "Rule 2", "market": "Home Win", "confidence": "High"}
        return {"status": "FAIL"}

    def check_rule_3(self, match):
        h_odd = match['odds']['home']
        if 1.90 <= h_odd <= 1.99:
            return {"status": "PASS", "rule": "Rule 3", "market": "Home/Draw (1X)", "confidence": "Medium"}
        return {"status": "FAIL"}

    def check_rule_4(self, match, team_stats):
        d_odd = match['odds']['draw']
        h_odd = match['odds']['home']
        a_odd = match['odds']['away']
        if 3.40 <= d_odd <= 3.60 and a_odd < h_odd:
            if team_stats['away_over_1_5_last_10'] >= 8:
                return {"status": "PASS", "rule": "Rule 4", "market": "Over 1.5 Goals", "confidence": "Medium"}
        return {"status": "FAIL"}

    def check_rule_5(self, match, h2h_stats):
        if h2h_stats['total_matches'] < 10:
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
        if r1['status'] == "PASS":
            results.append(r1)
        r2 = self.check_rule_2(match_data)
        if r2['status'] == "PASS":
            results.append(r2)
        r3 = self.check_rule_3(match_data)
        if r3['status'] == "PASS":
            results.append(r3)
        r4 = self.check_rule_4(match_data, match_data['team_stats'])
        if r4['status'] == "PASS":
            results.append(r4)
        r5 = self.check_rule_5(match_data, match_data['h2h_stats'])
        if r5['status'] == "PASS":
            results.append(r5)
        return results
