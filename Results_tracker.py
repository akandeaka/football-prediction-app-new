import json
from datetime import datetime

class ResultsTracker:
    def __init__(self, filename="predictions_log.json"):
        self.filename = filename
        self.predictions = self.load_predictions()
    
    def load_predictions(self):
        """Load existing predictions from file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_prediction(self, match_name, rule, market, odds, stake=10):
        """Save a new prediction"""
        prediction = {
            "id": len(self.predictions) + 1,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match": match_name,
            "rule": rule,
            "market": market,
            "odds": odds,
            "stake": stake,
            "status": "PENDING",  # PENDING, WIN, LOSS
            "result": None
        }
        self.predictions.append(prediction)
        self.save_to_file()
        print(f"✅ Prediction saved: {match_name} - {rule}")
        return prediction
    
    def update_result(self, prediction_id, result):
        """Update prediction with Win/Loss result"""
        for pred in self.predictions:
            if pred["id"] == prediction_id:
                pred["status"] = result  # WIN or LOSS
                pred["result"] = result
                if result == "WIN":
                    pred["profit"] = pred["stake"] * (pred["odds"] - 1)
                else:
                    pred["profit"] = -pred["stake"]
                self.save_to_file()
                print(f"✅ Updated prediction #{prediction_id}: {result}")
                return
        print(f"❌ Prediction #{prediction_id} not found")
    
    def save_to_file(self):
        """Save all predictions to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.predictions, f, indent=2)
    
    def get_statistics(self):
        """Calculate win rate and ROI"""
        total = len(self.predictions)
        completed = [p for p in self.predictions if p["status"] != "PENDING"]
        pending = [p for p in self.predictions if p["status"] == "PENDING"]
        wins = [p for p in completed if p["status"] == "WIN"]
        losses = [p for p in completed if p["status"] == "LOSS"]
        
        total_stake = sum(p["stake"] for p in completed)
        total_profit = sum(p.get("profit", 0) for p in completed)
        
        win_rate = (len(wins) / len(completed) * 100) if completed else 0
        roi = (total_profit / total_stake * 100) if total_stake > 0 else 0
        
        # Stats by rule
        rule_stats = {}
        for pred in completed:
            rule = pred["rule"]
            if rule not in rule_stats:
                rule_stats[rule] = {"wins": 0, "losses": 0, "profit": 0}
            if pred["status"] == "WIN":
                rule_stats[rule]["wins"] += 1
                rule_stats[rule]["profit"] += pred.get("profit", 0)
            else:
                rule_stats[rule]["losses"] += 1
                rule_stats[rule]["profit"] -= pred["stake"]
        
        return {
            "total_predictions": total,
            "completed": len(completed),
            "pending": len(pending),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": f"{win_rate:.1f}%",
            "roi": f"{roi:.1f}%",
            "total_profit": total_profit,
            "by_rule": rule_stats
        }
    
    def print_report(self):
        """Print statistics report"""
        stats = self.get_statistics()
        
        print("=" * 60)
        print("📊 PREDICTION PERFORMANCE REPORT")
        print("=" * 60)
        print(f"Total Predictions: {stats['total_predictions']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        print(f"Wins: {stats['wins']}")
        print(f"Losses: {stats['losses']}")
        print(f"Win Rate: {stats['win_rate']}")
        print(f"ROI: {stats['roi']}")
        print(f"Total Profit: ${stats['total_profit']:.2f}")
        
        if stats['by_rule']:
            print("\n📈 Performance by Rule:")
            for rule, data in stats['by_rule'].items():
                total = data['wins'] + data['losses']
                rate = (data['wins'] / total * 100) if total > 0 else 0
                print(f"   {rule}: {data['wins']}/{total} ({rate:.0f}%) - ${data['profit']:.2f}")
        
        print("=" * 60)

# Quick test
if __name__ == "__main__":
    tracker = ResultsTracker()
    tracker.print_report()
