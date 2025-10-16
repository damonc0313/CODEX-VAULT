"""
Codex Autonomous Framework v4.0 - Main Entry Point

Complete autonomous cognitive system with:
- Multi-agent coordination
- Metacognitive reflection
- Ethical guardrails
- Chain of Thought logging
- Adaptive intelligence scaling
- Cross-domain innovation
"""

from typing import Dict, Any
import logging
from pathlib import Path

# Core components
from codex_framework.core import (
    CognitiveCore,
    COTLogger
)

# Agents
from codex_framework.agents import (
    AnalyzerOmega,
    ArchitectPhi,
    BuilderDelta,
    MentorSigma
)

# Systems
from codex_framework.systems import (
    InnovationProtocol,
    ExecutionOrchestrator,
    AdaptiveScaling
)

# Telemetry
from codex_framework.telemetry import (
    TelemetrySystem,
    IntelligenceIndexMonitor,
    DiagnosticsEngine
)


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('codex_framework/codex_execution.log')
        ]
    )


class CodexAutonomousFramework:
    """
    Codex Autonomous Framework v4.0
    
    Self-evolving cognitive ecosystem with full autonomy.
    """
    
    def __init__(self) -> None:
        """Initialize Codex Framework."""
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("=" * 60)
        self.logger.info("CODEX AUTONOMOUS FRAMEWORK v4.0 - INITIALIZING")
        self.logger.info("=" * 60)
        
        # Initialize core
        self.logger.info("Initializing Cognitive Core...")
        self.core = CognitiveCore()
        
        # Initialize COT Logger
        self.logger.info("Initializing Chain of Thought Logger...")
        self.cot_logger = COTLogger()
        
        # Initialize Unknown Unknown Detector
        self.logger.info("Initializing Unknown Unknown Detector...")
        from codex_framework.core import UnknownUnknownDetector
        self.unknown_detector = UnknownUnknownDetector()
        
        # Initialize agents
        self.logger.info("Initializing Cognitive Agents...")
        self.agents = {
            'analyzer': AnalyzerOmega(self.core.metacognition),
            'architect': ArchitectPhi(self.core.metacognition),
            'builder': BuilderDelta(
                self.core.metacognition,
                self.core.rigor,
                self.core.ethics
            ),
            'mentor': MentorSigma(self.core.metacognition)
        }
        
        # Initialize telemetry
        self.logger.info("Initializing Telemetry Systems...")
        self.telemetry = TelemetrySystem()
        self.intelligence = IntelligenceIndexMonitor()
        self.diagnostics = DiagnosticsEngine()
        
        # Initialize systems
        self.logger.info("Initializing System Protocols...")
        self.innovation = InnovationProtocol()
        self.scaling = AdaptiveScaling()
        
        # Initialize orchestrator
        self.logger.info("Initializing Execution Orchestrator...")
        self.orchestrator = ExecutionOrchestrator(
            cognitive_core=self.core,
            agents=self.agents,
            telemetry=self.telemetry,
            intelligence_monitor=self.intelligence,
            diagnostics=self.diagnostics,
            innovation=self.innovation,
            adaptive_scaling=self.scaling,
            cot_logger=self.cot_logger
        )
        
        self.logger.info("=" * 60)
        self.logger.info("CODEX FRAMEWORK INITIALIZED - READY FOR AUTONOMOUS OPERATION")
        self.logger.info("=" * 60)
        
    def execute(
        self,
        goal: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute autonomous cognitive loop.
        
        Args:
            goal: Goal to achieve
            context: Operational context
            
        Returns:
            Execution results with full trace
        """
        if context is None:
            context = {}
            
        self.logger.info(f"\nEXECUTING AUTONOMOUS GOAL: {goal}")
        
        results = self.orchestrator.execute_autonomous_loop(goal, context)
        
        # Display summary
        self._display_summary(results)
        
        return results
        
    def get_status(self) -> Dict[str, Any]:
        """Get complete framework status."""
        return {
            'orchestrator': self.orchestrator.get_status(),
            'cognitive_core': self.core.get_status(),
            'intelligence': self.intelligence.get_status(),
            'evolution': self.cot_logger.generate_evolution_report()
        }
        
    def get_lessons_learned(self, min_quality: float = 0.7) -> list:
        """Get lessons learned from past executions."""
        return self.cot_logger.extract_lessons_learned(min_quality)
        
    def _display_summary(self, results: Dict[str, Any]) -> None:
        """Display execution summary."""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("EXECUTION SUMMARY")
        self.logger.info("=" * 60)
        
        self.logger.info(f"Goal ID: {results['goal_id']}")
        self.logger.info(f"Goal: {results['goal']}")
        self.logger.info(f"Phases Completed: {len(results['phases'])}")
        
        eval_data = results.get('evaluation', {})
        self.logger.info(
            f"Quality Score: {eval_data.get('quality_score', 0):.2f}"
        )
        self.logger.info(f"CII: {results.get('cii', 0):.3f}")
        
        if 'innovation' in results:
            self.logger.info(
                f"Innovation Applied: "
                f"{results['innovation'].novelty_score:.2f} novelty"
            )
            
        self.logger.info(f"COT Record: {results.get('cot_path', 'N/A')}")
        self.logger.info("=" * 60 + "\n")


def main() -> None:
    """Main autonomous execution demonstration."""
    # Initialize framework
    codex = CodexAutonomousFramework()
    
    # Example autonomous execution
    goal = "Design and implement a self-learning knowledge graph system"
    context = {
        'domain': 'knowledge_management',
        'complexity': 'high',
        'novelty': True,
        'performance': True
    }
    
    # Execute
    results = codex.execute(goal, context)
    
    # Get status
    status = codex.get_status()
    print("\n=== FRAMEWORK STATUS ===")
    print(f"Total Executions: {status['orchestrator']['execution_count']}")
    print(f"Current CII: {status['intelligence']['cii']:.3f}")
    print(f"Intelligence Status: {status['intelligence']['status']}")
    
    # Show evolution
    evolution = status['evolution']
    if evolution.get('total_decisions', 0) > 0:
        print("\n=== EVOLUTION METRICS ===")
        print(f"Total Decisions: {evolution['total_decisions']}")
        print(f"Avg Quality: {evolution.get('avg_quality', 0):.2f}")
        print(f"Avg Confidence: {evolution.get('avg_confidence', 0):.2f}")
        print(f"Ethical Pass Rate: {evolution.get('ethical_pass_rate', 0):.1%}")
        print(f"Innovation Rate: {evolution.get('innovation_rate', 0):.1%}")
        
    # Get lessons
    lessons = codex.get_lessons_learned()
    if lessons:
        print(f"\n=== LESSONS LEARNED ({len(lessons)}) ===")
        for lesson in lessons[:3]:  # Show top 3
            print(f"- {lesson['lesson']}")
            print(f"  (Quality: {lesson['quality']:.2f})")


if __name__ == "__main__":
    main()
