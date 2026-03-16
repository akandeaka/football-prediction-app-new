import json
from datetime import datetime

class ResultsTracker:
    def __init__(self, filename="predictions_log.json"):
        self.filename = filename
        self.predictions = self.load_predictions()
    
    def load_predictions(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_prediction(self, match_name, rule, market, odds, stake=10):
        prediction = {
            "id": len(self.predictions) + 1,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match": match_name,
            "rule": rule,
            "market": market,
            "odds": odds,
            "stake": stake,
            "status": "PENDING",
            "result": None
        }
        self.predictions.append(prediction)
        self.save_to_file()
        print(f"  ✅ Prediction saved: {match_name} - {rule}")
        return prediction
    
    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.predictions, f, indent=2)
    
    def get_statistics(self):
        total = len(self.predictions)
        completed = [p for p in self.predictions if p["status"] != "PENDING"]
        pending = [p for p in self.predictions if p["status"] == "PENDING"]
        wins = [p for p in completed if p["status"] == "WIN"]
        losses = [p for p in completed if p["status"] == "LOSS"]
        
        total_stake = sum(p["stake"] for p in completed)
        total_profit = sum(p.get("profit", 0) for p in completed)
        
        win_rate = (len(wins) / len(completed) * 100) if completed else 0
        roi = (total_profit / total_stake * 100) if total_stake > 0 else 0
        
        return {
            "total_predictions": total,
            "completed": len(completed),
            "pending": len(pending),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": f"{win_rate:.1f}%",
            "roi": f"{roi:.1f}%",
            "total_profit": total_profit
        }
    
    def print_report(self):
        stats = self.get_statistics()
        print("\n" + "=" * 60)
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
        print("=" * 60)

if __name__ == "__main__":
    tracker = ResultsTracker()
    tracker.print_report()
