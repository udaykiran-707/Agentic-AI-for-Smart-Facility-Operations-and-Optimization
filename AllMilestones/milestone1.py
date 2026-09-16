import time
import random
from datetime import datetime

class EnergyIntelligenceEngine:
    def __init__(self):
        self.current_load = 450.0  # kW
        self.cumulative_usage = 3200.0  # kWh
        self.monthly_cost = 450000.0  # INR
        self.efficiency_score = 86
        self.history = [400 + random.randint(0, 80) for _ in range(20)]
        self.alerts = []

    def log_alert(self, msg: str, severity: str):
        if not any(a["msg"] == msg for a in self.alerts):
            alert = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "severity": severity,
                "msg": msg
            }
            self.alerts.append(alert)
            print(f"\n[ALERT - {severity.upper()}] {alert['timestamp']}: {msg}")

    def simulate_tick(self):
        # Fluctuate real-time load
        delta = (random.random() - 0.48) * 16.0
        self.current_load = max(150.0, min(800.0, self.current_load + delta))
        self.cumulative_usage += (self.current_load / 3600.0) * 2.0
        
        self.history.append(round(self.current_load, 1))
        if len(self.history) > 20:
            self.history.pop(0)

        # Autonomous Anomaly Detection
        if self.current_load > 520.0:
            self.log_alert("Peak power demand threshold breached (>520 kW).", "High")
            self.efficiency_score = max(60, self.efficiency_score - 1)
        else:
            self.efficiency_score = min(95, self.efficiency_score + 1)

    def apply_recommendation(self, action_name: str, savings: float):
        print(f"\n>>> Autonomous Policy Applied: {action_name}")
        print(f">>> Projected Monthly Savings: ₹{savings:,.2f}")
        self.current_load = max(200.0, self.current_load - 35.0)

    def render_dashboard(self):
        print("\033[H\033[J", end="")  # Clear screen in POSIX terminals
        print("=" * 65)
        print(" ⚡ FACILITYOPS AI - MILESTONE 1: ENERGY INTELLIGENCE")
        print("=" * 65)
        print(f" Live Demand Load     : {self.current_load:.1f} kW")
        print(f" Cumulative Energy    : {self.cumulative_usage:.2f} kWh")
        print(f" Projected Cost       : ₹{self.monthly_cost:,.2f}")
        print(f" Efficiency Index     : {self.efficiency_score} / 100")
        print("-" * 65)
        
        # ASCII Line Trend Visualization
        min_v, max_v = min(self.history), max(self.history)
        range_v = max_v - min_v if max_v != min_v else 1.0
        print(" Telemetry Trend (last 20 readings):")
        trend_line = "".join(" ▂▃▄▅▆▇█"[min(7, int((v - min_v) / range_v * 7))] for v in self.history)
        print(f" [{trend_line}]  (Min: {min_v:.0f} kW | Max: {max_v:.0f} kW)")
        print("-" * 65)

        print(f" Active Alerts: {len(self.alerts)}")
        for a in self.alerts[-3:]:
            print(f"  • [{a['severity']}] {a['timestamp']} - {a['msg']}")
        print("=" * 65)
        print("Press Ctrl+C to exit.")

if __name__ == "__main__":
    engine = EnergyIntelligenceEngine()
    try:
        step = 0
        while True:
            engine.simulate_tick()
            engine.render_dashboard()
            
            step += 1
            if step == 5:
                engine.apply_recommendation("Increase Night HVAC Setpoint by +1.5°C", 22000.0)

            time.sleep(2)
    except KeyboardInterrupt:
        print("\nEnergy Intelligence Engine stopped.")