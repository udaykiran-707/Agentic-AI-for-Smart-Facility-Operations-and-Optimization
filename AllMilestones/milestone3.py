import time
import random
from datetime import datetime

class OccupancySecurityEngine:
    def __init__(self):
        self.capacity = 600
        self.current_occupancy = 340
        self.bldg_a = 140
        self.bldg_b = 95
        self.bldg_c = 105
        self.unauthorized_events = 2
        self.security_score = 88
        
        # 32-zone spatial sensor grid representing room density (0.0 to 1.0)
        self.sensor_grid = [round(random.random(), 2) for _ in range(32)]
        self.access_logs = [
            {"time": "10:45 AM", "user": "Visitor #019", "portal": "Bldg B Lobby", "status": "Granted"},
            {"time": "10:41 AM", "user": "Unknown Card", "portal": "Server Bay A", "status": "Denied"},
            {"time": "10:38 AM", "user": "Staff #881", "portal": "Building A Gate", "status": "Granted"},
            {"time": "10:32 AM", "user": "Contractor #14", "portal": "Service Bay", "status": "Granted"}
        ]

    def simulate_tick(self):
        # People movement simulation
        delta = random.randint(-4, 5)
        self.current_occupancy = max(80, min(self.capacity, self.current_occupancy + delta))
        
        self.bldg_a = int(self.current_occupancy * 0.42)
        self.bldg_b = int(self.current_occupancy * 0.28)
        self.bldg_c = self.current_occupancy - self.bldg_a - self.bldg_b

        # Simulate access control & security gate
        if random.random() > 0.85:
            timestamp = datetime.now().strftime("%I:%M %p")
            is_authorized = random.random() > 0.12
            
            log_entry = {
                "time": timestamp,
                "user": f"Badge #{random.randint(100, 999)}" if is_authorized else "Unrecognized Chip",
                "portal": random.choice(["Main Gate", "Server Vault", "Lab 04", "Loading Dock"]),
                "status": "Granted" if is_authorized else "Denied"
            }
            self.access_logs.insert(0, log_entry)
            if not is_authorized:
                self.unauthorized_events += 1
                self.security_score = max(50, self.security_score - 2)

        # Update 32-zone spatial density values
        self.sensor_grid = [round(random.random(), 2) for _ in range(32)]

    def render_dashboard(self):
        print("\033[H\033[J", end="")
        print("=" * 68)
        print(" 👥 FACILITYOPS AI - MILESTONE 3: OCCUPANCY & SECURITY SYSTEM")
        print("=" * 68)
        
        occupancy_pct = (self.current_occupancy / self.capacity) * 100
        print(f" Campus Headcount     : {self.current_occupancy} / {self.capacity} ({occupancy_pct:.1f}%)")
        print(f" Security Health Score: {self.security_score} / 100")
        print(f" Unauthorized Breaches: {self.unauthorized_events}")
        print("-" * 68)
        print(" Building Headcount Distribution:")
        print(f"  • Building A : {self.bldg_a:<4} [{'#' * (self.bldg_a // 10):<16}]")
        print(f"  • Building B : {self.bldg_b:<4} [{'#' * (self.bldg_b // 10):<16}]")
        print(f"  • Building C : {self.bldg_c:<4} [{'#' * (self.bldg_c // 10):<16}]")
        print("-" * 68)
        
        # Render Heatmap Grid (8 columns x 4 rows)
        print(" 32-Zone Spatial Density Heatmap ([.] Low, [*] Moderate, [!] Critical):")
        for row in range(4):
            line = "  "
            for col in range(8):
                val = self.sensor_grid[row * 8 + col]
                symbol = "[!]" if val > 0.80 else ("[*]" if val > 0.40 else "[.]")
                line += f"{symbol} "
            print(line)
        print("-" * 68)

        print(" Live Gate Swipe Feed:")
        for log in self.access_logs[:4]:
            status_display = f"\033[92m{log['status']}\033[0m" if log['status'] == "Granted" else f"\033[91m{log['status']}\033[0m"
            print(f"  [{log['time']}] {log['user']:<18} @ {log['portal']:<14} -> {status_display}")
        print("=" * 68)
        print("Press Ctrl+C to exit.")

if __name__ == "__main__":
    engine = OccupancySecurityEngine()
    try:
        while True:
            engine.simulate_tick()
            engine.render_dashboard()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nOccupancy & Security Engine stopped.")