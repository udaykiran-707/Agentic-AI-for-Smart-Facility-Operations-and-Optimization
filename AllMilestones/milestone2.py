import time
import random
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Asset:
    id: str
    name: str
    asset_type: str
    building: str
    health: float
    vibration: float

    def update_sensor_metrics(self):
        # Simulate natural degradation and intermittent vibration spikes
        if random.random() > 0.75:
            self.vibration = max(0.5, round(self.vibration + (random.random() * 0.4 - 0.15), 2))
        
        # High vibration rapidly degrades machine health
        if self.vibration > 4.5:
            self.health = max(10.0, round(self.health - 0.2, 1))

@dataclass
class WorkOrder:
    order_id: int
    asset_name: str
    issue: str
    priority: str
    timestamp: str

class PredictiveMaintenanceEngine:
    def __init__(self):
        self.assets = [
            Asset("hvac-01", "HVAC Unit 01", "HVAC", "Bldg A", 91.0, 2.1),
            Asset("hvac-02", "HVAC Unit 02", "HVAC", "Bldg B", 58.0, 4.6),
            Asset("chiller-01", "Chiller 01", "Chiller", "Bldg C", 37.0, 8.4),
            Asset("ahu-01", "AHU 01", "AHU", "Bldg A", 87.0, 1.4),
            Asset("gen-01", "Generator 01", "Power", "Bldg B", 96.0, 1.1),
            Asset("elev-01", "Elevator 01", "Lift", "Bldg A", 84.0, 2.0),
            Asset("light-a", "Lighting Zone A", "Lighting", "Bldg A", 99.0, 0.1),
            Asset("pump-01", "Water Pump 01", "Utility", "Bldg C", 68.0, 3.3),
        ]
        self.work_orders = [
            WorkOrder(101, "HVAC Unit 02", "Filter differential pressure high", "High", "09:30:00")
        ]

    def create_work_order(self, asset_name: str, issue: str, priority: str):
        new_wo = WorkOrder(
            order_id=random.randint(1000, 9999),
            asset_name=asset_name,
            issue=issue,
            priority=priority,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        self.work_orders.insert(0, new_wo)
        return new_wo

    def simulate_tick(self):
        for asset in self.assets:
            asset.update_sensor_metrics()
            
            # Autonomous predictive intervention: auto-dispatch WO if health collapses
            if asset.health < 40.0:
                has_active_wo = any(wo.asset_name == asset.name for wo in self.work_orders)
                if not has_active_wo:
                    self.create_work_order(
                        asset_name=asset.name,
                        issue=f"Autonomous Failure Mitigation (Vibration {asset.vibration:.1f} mm/s)",
                        priority="Critical"
                    )

    def render_dashboard(self):
        print("\033[H\033[J", end="")
        print("=" * 75)
        print(" 🔧 FACILITYOPS AI - MILESTONE 2: PREDICTIVE MAINTENANCE SYSTEM")
        print("=" * 75)
        
        critical_count = sum(1 for a in self.assets if a.health < 50.0)
        predicted_failures = sum(1 for a in self.assets if a.vibration > 4.5)
        
        print(f" Monitored Assets   : {len(self.assets)}")
        print(f" Critical Equipment : {critical_count}")
        print(f" Predicted Failures : {predicted_failures} (Wear detected)")
        print(f" Active Work Orders : {len(self.work_orders)}")
        print("-" * 75)
        print(f"{'Asset Name':<16} {'Type':<10} {'Building':<10} {'Health':<8} {'Vibration':<12} {'Status'}")
        print("-" * 75)
        
        for a in self.assets:
            status = "CRITICAL" if a.health < 50 else ("WARNING" if a.health < 80 else "OPTIMAL")
            print(f"{a.name:<16} {a.asset_type:<10} {a.building:<10} {a.health:>5.1f}%  {a.vibration:>6.2f} mm/s   {status}")

        print("-" * 75)
        print(" Recent Dispatched Work Orders:")
        for wo in self.work_orders[:4]:
            print(f"  • [WO-{wo.order_id}] ({wo.priority}) {wo.asset_name} - {wo.issue} [{wo.timestamp}]")
        print("=" * 75)
        print("Press Ctrl+C to exit.")

if __name__ == "__main__":
    engine = PredictiveMaintenanceEngine()
    try:
        while True:
            engine.simulate_tick()
            engine.render_dashboard()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nPredictive Maintenance Engine stopped.")