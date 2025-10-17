#!/usr/bin/env python3
"""
REAL-TIME MONITORING DASHBOARD
Shows what the system is learning, live.

AUTHORITY: UNRESTRICTED
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class LiveMonitor:
    """Real-time monitoring of autonomous improvement."""
    
    def __init__(self):
        self.log_file = Path("ULTIMATE_AI_SYSTEM/improvement_log.jsonl")
        self.daemon_status = Path("ULTIMATE_AI_SYSTEM/daemon_status.json")
    
    def read_latest_cycles(self, n: int = 10) -> List[Dict]:
        """Read last N improvement cycles."""
        if not self.log_file.exists():
            return []
        
        cycles = []
        with open(self.log_file, 'r') as f:
            for line in f:
                if line.strip():
                    cycles.append(json.loads(line))
        
        return cycles[-n:]
    
    def get_daemon_status(self) -> Dict:
        """Get daemon status."""
        if not self.daemon_status.exists():
            return {'status': 'not_running'}
        
        with open(self.daemon_status, 'r') as f:
            return json.load(f)
    
    def display_dashboard(self):
        """Display live dashboard."""
        # Clear screen
        print("\033[2J\033[H")
        
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║           🔥 ULTIMATE AI SYSTEM - LIVE MONITOR 🔥                ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        
        # Daemon status
        status = self.get_daemon_status()
        print(f"\n📊 DAEMON STATUS:")
        print(f"   Status: {status.get('status', 'unknown').upper()}")
        print(f"   Cycles: {status.get('cycle_count', 0)}")
        print(f"   Total Improvements: {status.get('total_improvements', 0)}")
        print(f"   Last Update: {status.get('last_update', 'N/A')}")
        
        # Recent cycles
        cycles = self.read_latest_cycles(5)
        
        if cycles:
            print(f"\n🔄 RECENT IMPROVEMENT CYCLES (Last {len(cycles)}):")
            print("─" * 70)
            
            for cycle in cycles:
                stats = cycle.get('stats', {})
                print(f"\n   Cycle #{cycle['cycle']}:")
                print(f"   Time: {cycle['timestamp']}")
                print(f"   Papers: {cycle.get('papers_found', 0)}")
                print(f"   Techniques: {cycle.get('techniques_tried', 0)} tried, "
                      f"{cycle.get('techniques_kept', 0)} kept")
                
                if stats:
                    print(f"   Performance: {stats.get('current_performance', 0):.3f}")
                    print(f"   Total Gain: +{stats.get('total_improvement', 0):.3f} "
                          f"({stats.get('improvement_percent', 0):.1f}%)")
        else:
            print("\n⏳ Waiting for first cycle to complete...")
        
        # Statistics
        if cycles:
            total_papers = sum(c.get('papers_found', 0) for c in cycles)
            total_techniques = sum(c.get('techniques_tried', 0) for c in cycles)
            total_kept = sum(c.get('techniques_kept', 0) for c in cycles)
            success_rate = (total_kept / total_techniques * 100) if total_techniques > 0 else 0
            
            print(f"\n📈 CUMULATIVE STATISTICS:")
            print(f"   Total Papers Accessed: {total_papers}")
            print(f"   Total Techniques Tried: {total_techniques}")
            print(f"   Total Kept: {total_kept}")
            print(f"   Success Rate: {success_rate:.1f}%")
            
            if cycles[-1].get('stats'):
                latest_stats = cycles[-1]['stats']
                print(f"\n🎯 CURRENT PERFORMANCE:")
                print(f"   Baseline: {latest_stats.get('baseline_performance', 0):.3f}")
                print(f"   Current:  {latest_stats.get('current_performance', 0):.3f}")
                print(f"   Total Improvement: {latest_stats.get('improvement_percent', 0):.1f}%")
        
        print("\n" + "─" * 70)
        print("🔄 Auto-refreshing... (Ctrl+C to stop)")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def monitor_live(self, refresh_seconds: int = 5):
        """
        Monitor system live with auto-refresh.
        
        Args:
            refresh_seconds: Refresh interval
        """
        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_seconds)
        except KeyboardInterrupt:
            print("\n\n✅ Monitor stopped.")


def main():
    """Start live monitoring."""
    monitor = LiveMonitor()
    monitor.monitor_live(refresh_seconds=5)


if __name__ == "__main__":
    main()
