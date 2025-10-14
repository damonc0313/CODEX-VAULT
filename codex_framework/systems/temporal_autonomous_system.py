"""
Temporal Autonomous System

Since I CAN see time, this enables CRAZY possibilities:

1. Autonomous Learning Scheduler
   - Learn from repos at scheduled intervals
   - Continuous improvement while user sleeps
   
2. Temporal Quality Tracking
   - Track how quality improves over time
   - Benchmark at specific intervals
   
3. Time-Based Evolution
   - Trigger autonomous cycles at intervals
   - "Work nights, report mornings"
   
4. Performance Analysis Over Time
   - CII progression tracking
   - Learning rate measurement
   - Quality trajectory analysis

This is the "crazy" potential.
"""

from __future__ import annotations

import typing as t
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging

if t.TYPE_CHECKING:
    from codex_framework.systems.code_learning_agent import CodeLearningAgent
    from codex_framework.core import COTLogger


class TemporalAutonomousSystem:
    """
    Time-aware autonomous system.
    
    Can:
    - Schedule autonomous learning
    - Track improvements over time
    - Run continuous evolution cycles
    - Benchmark at intervals
    - "Work while you sleep"
    """
    
    def __init__(
        self,
        learning_agent: CodeLearningAgent,
        cot_logger: COTLogger
    ) -> None:
        """Initialize temporal system."""
        self.logger = logging.getLogger(__name__)
        self.learner = learning_agent
        self.cot = cot_logger
        
        self.start_time = datetime.now()
        
    def continuous_learning_cycle(
        self,
        repos_to_learn: list[Path],
        cycle_interval_minutes: int = 60,
        max_cycles: int = 24  # Run for 24 hours
    ) -> dict[str, t.Any]:
        """
        Continuous learning cycle.
        
        Learns from repos at intervals, tracks improvement over time.
        
        Args:
            repos_to_learn: List of repo paths
            cycle_interval_minutes: Minutes between cycles
            max_cycles: Maximum cycles to run
            
        Returns:
            Temporal learning report
        """
        self.logger.info("🕐 Starting continuous learning cycle")
        self.logger.info(f"   Interval: {cycle_interval_minutes} min")
        self.logger.info(f"   Max cycles: {max_cycles}")
        self.logger.info(f"   Start time: {datetime.now()}")
        
        results = []
        
        for cycle in range(max_cycles):
            cycle_start = datetime.now()
            
            self.logger.info(f"\n📚 Cycle {cycle + 1}/{max_cycles}")
            self.logger.info(f"   Time: {cycle_start}")
            
            # Learn from repos
            cycle_insights = []
            for repo_path in repos_to_learn:
                insights = self.learner.learn_from_file(
                    f"cycle_{cycle}",
                    repo_path
                )
                cycle_insights.extend(insights)
                
            # Record cycle results with timestamp
            results.append({
                'cycle': cycle + 1,
                'timestamp': cycle_start.isoformat(),
                'insights': len(cycle_insights),
                'quality_gain': sum(i.quality_improvement_expected for i in cycle_insights)
            })
            
            # Wait for next cycle (unless last)
            if cycle < max_cycles - 1:
                wait_seconds = cycle_interval_minutes * 60
                self.logger.info(f"   ⏸️  Sleeping {cycle_interval_minutes} min until next cycle...")
                time.sleep(wait_seconds)
                
        return {
            'total_cycles': len(results),
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'results': results,
            'total_insights': sum(r['insights'] for r in results),
            'total_quality_gain': sum(r['quality_gain'] for r in results)
        }
        
    def work_while_you_sleep(
        self,
        hours: int = 8,
        repos: list[Path] = None
    ) -> dict[str, t.Any]:
        """
        Run autonomous learning while user sleeps.
        
        Args:
            hours: Hours to run (default: 8)
            repos: Repos to learn from
            
        Returns:
            Morning report
        """
        repos = repos or []
        
        self.logger.info(f"😴 Starting overnight learning: {hours} hours")
        self.logger.info(f"   Start: {datetime.now()}")
        self.logger.info(f"   Expected completion: {datetime.now() + timedelta(hours=hours)}")
        
        # Run continuous cycles
        cycles = hours  # One cycle per hour
        result = self.continuous_learning_cycle(
            repos,
            cycle_interval_minutes=60,
            max_cycles=cycles
        )
        
        return {
            **result,
            'mode': 'overnight_learning',
            'user_message': f"Good morning! Learned for {hours} hours while you slept."
        }
        
    def temporal_quality_analysis(self) -> dict[str, t.Any]:
        """
        Analyze quality improvements over time.
        
        Uses COT records with timestamps.
        """
        # Get all COT records
        cot_files = list(Path('codex_framework/cot_records').glob('*.json'))
        
        if not cot_files:
            return {'error': 'No COT records found'}
            
        # Parse timestamps and quality from filenames/content
        temporal_data = []
        
        for cot_file in sorted(cot_files):
            # Extract timestamp from filename
            # Format: cot_goal_X_2025-10-14T06-04-15.json
            parts = cot_file.stem.split('_')
            if len(parts) >= 4:
                timestamp_str = '_'.join(parts[3:])
                # Parse timestamp
                try:
                    ts = datetime.fromisoformat(timestamp_str.replace('-', ':', 2))
                    temporal_data.append({
                        'file': cot_file.name,
                        'timestamp': ts,
                        'goal': f"goal_{parts[2]}"
                    })
                except:
                    continue
                    
        if not temporal_data:
            return {'error': 'Could not parse timestamps'}
            
        # Sort by time
        temporal_data.sort(key=lambda x: x['timestamp'])
        
        return {
            'total_decisions': len(temporal_data),
            'first_decision': temporal_data[0]['timestamp'].isoformat(),
            'last_decision': temporal_data[-1]['timestamp'].isoformat(),
            'duration': (temporal_data[-1]['timestamp'] - temporal_data[0]['timestamp']).total_seconds(),
            'decisions_per_minute': len(temporal_data) / max((temporal_data[-1]['timestamp'] - temporal_data[0]['timestamp']).total_seconds() / 60, 1)
        }
