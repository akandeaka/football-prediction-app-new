import json

def show_dashboard():
    try:
        with open('predictions_log.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ No predictions found yet.")
        return
    
    total = len(data)
    completed = [p for p in data if p['status'] != 'PENDING']
    wins = [p for p in completed if p['status'] == 'WIN']
    losses = [p for p in completed if p['status'] == 'LOSS']
    
    total_profit = sum(p.get('profit', 0) for p in completed)
    win_rate = (len(wins) / len(completed) * 100) if completed else 0
    
    print("\n" + "=" * 60)
    print("📊 FOOTBALL PREDICTION DASHBOARD")
    print("=" * 60)
    print(f"Total Predictions: {total}")
    print(f"Completed Matches: {len(completed)}")
    print(f"Pending Matches:   {total - len(completed)}")
    print("-" * 60)
    print(f"Wins:              {len(wins)}")
    print(f"Losses:            {len(losses)}")
    print(f"Win Rate:          {win_rate:.1f}%")
    print(f"Total Profit:      ${total_profit:.2f}")
    print("=" * 60)
    
    if completed:
        print("\n📈 Recent Results:")
        for p in completed[-5:]:
            status = "✅ WIN" if p['status'] == 'WIN' else "❌ LOSS"
            print(f"  {p['match']}: {status} (${p.get('profit', 0):.2f})")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    show_dashboard()