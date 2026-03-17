import json

def load_predictions():
    try:
        with open('predictions_log.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ predictions_log.json not found. Run run_predictions.py first.")
        return []

def save_predictions(data):
    with open('predictions_log.json', 'w') as f:
        json.dump(data, f, indent=2)

def show_pending():
    data = load_predictions()
    pending = [p for p in data if p['status'] == 'PENDING']
    if not pending:
        print("✅ No pending predictions. All matches completed!")
        return
    
    print("\n" + "=" * 60)
    print("📋 PENDING PREDICTIONS")
    print("=" * 60)
    for p in pending:
        print(f"ID: {p['id']} | {p['match']} | {p['rule']} | Odds: {p['odds']}")
    print("=" * 60)

def update_result():
    show_pending()
    data = load_predictions()
    if not data:
        return
    
    try:
        pid = int(input("\nEnter Prediction ID to update (0 to cancel): "))
        if pid == 0:
            return
        
        for p in data:
            if p['id'] == pid:
                result = input(f"Mark ID {pid} as (W)in or (L)oss?: ").upper()
                if result == 'W':
                    p['status'] = 'WIN'
                    p['profit'] = p['stake'] * (p['odds'] - 1)
                    print(f"✅ Updated ID {pid} as WIN")
                elif result == 'L':
                    p['status'] = 'LOSS'
                    p['profit'] = -p['stake']
                    print(f"✅ Updated ID {pid} as LOSS")
                else:
                    print("❌ Invalid input.")
                    return
                
                save_predictions(data)
                return
        
        print("❌ ID not found.")
    except ValueError:
        print("❌ Please enter a valid number.")

if __name__ == "__main__":
    update_result()