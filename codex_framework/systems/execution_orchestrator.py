"""Central execution orchestrator for autonomous operation."""

from typing import Any, Dict, List, Optional
import logging


class ExecutionOrchestrator:
    """
    Central orchestrator for Codex autonomous execution.
    
    Coordinates all agents, systems, and cognitive processes
    through the complete execution loop.
    """
    
    def __init__(
        self,
        cognitive_core: Any,
        agents: Dict[str, Any],
        telemetry: Any,
        intelligence_monitor: Any,
        diagnostics: Any,
        innovation: Any,
        adaptive_scaling: Any,
        cot_logger: Any
    ) -> None:
        """
        Initialize execution orchestrator.
        
        Args:
            cognitive_core: Central cognitive core
            agents: Dictionary of cognitive agents
            telemetry: Telemetry system
            intelligence_monitor: Intelligence index monitor
            diagnostics: Diagnostics engine
            innovation: Innovation protocol
            adaptive_scaling: Adaptive scaling system
            cot_logger: Chain of Thought logger
        """
        self.logger = logging.getLogger(__name__)
        self.core = cognitive_core
        self.agents = agents
        self.telemetry = telemetry
        self.intelligence = intelligence_monitor
        self.diagnostics = diagnostics
        self.innovation = innovation
        self.scaling = adaptive_scaling
        self.cot = cot_logger
        
        self.execution_count = 0
        self.goal_history: List[Dict[str, Any]] = []
        
    def execute_autonomous_loop(
        self,
        goal: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute complete autonomous cognitive loop.
        
        Follows execution sequence:
        1. Detect and classify goal
        2. Execute modes (analysis → architecture → build → critique)
        3. Innovation protocol if required
        4. Metacognitive reflection
        5. Ethics and rigor enforcement
        6. Evaluate results
        7. Update intelligence index
        8. Adapt parameters
        9. Learn and propagate
        
        Args:
            goal: Goal to achieve
            context: Operational context
            
        Returns:
            Complete execution results
        """
        self.execution_count += 1
        goal_id = f"goal_{self.execution_count}"
        
        self.logger.info(
            f"=== AUTONOMOUS EXECUTION LOOP {self.execution_count} ==="
        )
        self.logger.info(f"Goal: {goal}")
        
        # Initialize COT record for this decision
        self.cot.create_cot(goal_id, goal, context)
        
        # Query similar past decisions for learning
        similar_decisions = self.cot.query_similar_decisions(
            goal,
            list(context.keys()),
            limit=3
        )
        
        if similar_decisions:
            self.logger.info(
                f"Found {len(similar_decisions)} similar past decisions"
            )
        
        results = {
            'goal_id': goal_id,
            'goal': goal,
            'phases': {},
            'similar_decisions': [d.decision_id for d in similar_decisions]
        }
        
        # Phase 1: Analysis (Analyzer-Ω)
        self.core.set_mode('analysis')
        analysis = self.agents['analyzer'].analyze({
            'goal': goal,
            **context
        })
        results['phases']['analysis'] = analysis
        
        # Update COT with analysis
        self.cot.update_analysis_phase(
            goal_id,
            analysis.patterns,
            analysis.causal_relationships,
            analysis.confidence
        )
        
        self.telemetry.record_event(
            goal_id=goal_id,
            agent_mode='analysis',
            uncertainty=1.0 - analysis.confidence,
            ethical_status='passed',
            artifact_hash='analysis',
            result='complete'
        )
        
        # Phase 2: Architecture (Architect-Φ)
        self.core.set_mode('architecture')
        architecture = self.agents['architect'].design(
            analysis,
            goal,
            context
        )
        results['phases']['architecture'] = architecture
        
        self.telemetry.record_event(
            goal_id=goal_id,
            agent_mode='architecture',
            uncertainty=1.0 - architecture.coherence_score,
            ethical_status='passed',
            artifact_hash='architecture',
            result='complete'
        )
        
        # Phase 3: Build (Builder-Δ)
        self.core.set_mode('build')
        artifact = self.agents['builder'].build(
            architecture,
            {'type': 'python_module', 'goal': goal}
        )
        results['phases']['build'] = artifact
        
        self.telemetry.record_event(
            goal_id=goal_id,
            agent_mode='build',
            uncertainty=0.1 if artifact.validated else 0.5,
            ethical_status='passed' if artifact.functional else 'failed',
            artifact_hash=artifact.artifact_hash,
            result='functional' if artifact.functional else 'non_functional'
        )
        
        # Phase 4: Critique (Teaching/Mentor-Σ)
        self.core.set_mode('teaching')
        teaching = self.agents['mentor'].teach(artifact, context)
        results['phases']['critique'] = teaching
        
        # Phase 5: Innovation Protocol (if novelty required)
        if self._novelty_required(context):
            self.logger.info("Triggering Innovation Protocol")
            innovation_result = self.innovation.execute(goal)
            results['innovation'] = innovation_result
            
            # Update innovation rate
            self.intelligence.update_innovation_rate(
                innovation_result.novelty_score
            )
        
        # Phase 6: Metacognitive Reflection
        metacog_scan = self.core.metacognition.perform_introspective_scan()
        results['metacognition'] = metacog_scan
        
        # Update COT with metacognition
        self.cot.update_metacognition(
            goal_id,
            metacog_scan,
            self.core.metacognition.metrics.cognitive_consistency_index,
            self.core.metacognition.bias_flags
        )
        
        # Update COT with ethical validation
        ethical_weight = self.core.ethics.calculate_ethical_weight(
            cognitive_consistency=self.core.metacognition.metrics.cognitive_consistency_index,
            transparency=0.8,  # Based on reasoning transparency
            non_harmful_output=1.0 if artifact.functional else 0.5
        )
        
        self.cot.update_ethical_validation(
            goal_id,
            {
                'no_harm': artifact.functional,
                'no_bullshit': artifact.validated,
                'make_real_things': artifact.functional
            },
            ethical_weight
        )
        
        # Phase 7: Evaluate Results
        evaluation = self._evaluate_results(results)
        results['evaluation'] = evaluation
        
        # Phase 8: Update Intelligence Index
        self._update_intelligence_metrics(results)
        cii = self.intelligence.calculate_cii()
        results['cii'] = cii
        
        # Phase 9: Diagnostics
        diagnostic_report = self.diagnostics.comprehensive_diagnostic(
            decisions=self.core.metacognition.decision_trace,
            feedback=[0.8],  # Simplified feedback
            uncertainties=[
                phase.get('uncertainty', 0.3)
                for phase in results.get('phases', {}).values()
                if isinstance(phase, dict)
            ] or [0.3]
        )
        results['diagnostics'] = diagnostic_report
        
        # Phase 10: Adaptive Scaling
        scaling_report = self.scaling.adjust_parameters(
            cii=cii,
            feedback_convergence=diagnostic_report['feedback_convergence'],
            entropy=diagnostic_report['epistemic_entropy'],
            bias_detected=len(
                self.core.metacognition.bias_flags
            ) > 0
        )
        results['adaptive_scaling'] = scaling_report
        
        # Phase 11: Learn and Propagate
        lessons = self._learn_and_propagate(results)
        
        # Finalize COT record
        self.cot.finalize_decision(
            goal_id,
            decision=f"Executed {len(results['phases'])} phases",
            rationale=f"Goal: {goal}",
            confidence=cii,
            related_decisions=[d.decision_id for d in similar_decisions]
        )
        
        # Record outcome
        self.cot.record_outcome(
            goal_id,
            status=results['evaluation']['all_functional'],
            quality_score=results['evaluation']['quality_score'],
            lessons=lessons
        )
        
        # Persist COT to disk
        cot_path = self.cot.persist_cot(goal_id)
        results['cot_path'] = str(cot_path)
        
        self.goal_history.append(results)
        
        self.logger.info(
            f"=== EXECUTION COMPLETE (CII: {cii:.3f}) ==="
        )
        self.logger.info(f"COT saved: {cot_path}")
        
        return results
        
    def _novelty_required(self, context: Dict[str, Any]) -> bool:
        """Determine if novelty/innovation is required."""
        return context.get('novelty', False) or context.get('innovation', False)
        
    def _evaluate_results(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate overall execution results."""
        phases = results.get('phases', {})
        
        evaluation = {
            'phases_completed': len(phases),
            'all_functional': True,
            'quality_score': 0.0
        }
        
        # Check artifact quality
        if 'build' in phases:
            build = phases['build']
            evaluation['all_functional'] = (
                build.validated and build.functional
            )
            evaluation['quality_score'] = (
                1.0 if evaluation['all_functional'] else 0.5
            )
            
        return evaluation
        
    def _update_intelligence_metrics(
        self,
        results: Dict[str, Any]
    ) -> None:
        """Update intelligence index metrics."""
        # Update adaptability
        phases_success = results.get('evaluation', {}).get(
            'quality_score',
            0.5
        )
        self.intelligence.update_adaptability(phases_success)
        
        # Update clarity
        if 'critique' in results.get('phases', {}):
            clarity = results['phases']['critique'].clarity_score
            self.intelligence.update_clarity(clarity)
            
        # Update reasoning depth
        decision_count = len(self.core.metacognition.decision_trace)
        reasoning_depth = min(1.0, decision_count / 5.0)
        self.intelligence.update_reasoning_depth(reasoning_depth)
        
        # Update ethical stability
        ethical_pass = results.get('evaluation', {}).get(
            'all_functional',
            False
        )
        self.intelligence.update_ethical_stability(1.0 if ethical_pass else 0.7)
        
    def _learn_and_propagate(self, results: Dict[str, Any]) -> List[str]:
        """
        Learn from execution and propagate knowledge.
        
        Returns:
            List of lessons learned
        """
        # Log learning
        self.logger.info("Learning and propagation phase")
        
        lessons = []
        
        # Collect feedback
        quality = results.get('evaluation', {}).get('quality_score', 0.0)
        
        # Extract lessons based on performance
        if quality > 0.8:
            self.logger.info("High quality execution - reinforcing patterns")
            lessons.append(
                f"Successful pattern: {results.get('phases', {}).keys()}"
            )
        else:
            self.logger.info("Lower quality - adjusting approach")
            lessons.append(
                "Need improvement in artifact quality and validation"
            )
            
        # Learn from similar decisions
        if results.get('similar_decisions'):
            lessons.append(
                f"Applied insights from {len(results['similar_decisions'])} "
                "similar past decisions"
            )
            
        return lessons
            
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            'execution_count': self.execution_count,
            'current_mode': self.core.state['mode'],
            'intelligence_status': self.intelligence.get_status(),
            'telemetry_summary': self.telemetry.get_event_summary(),
            'scaling_parameters': self.scaling.get_parameters()
        }
