"""
Genesis Engine: DALE-G recursion with n=3 depth.

Implements Genesis Protocol per specification section 17.2.
Treats each catalyst as a genesis event with recursive processing.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.models import Catalyst, Plan
from ..core.agents import MultiAgentOrchestrator
from ..core.heuristics import HPL, Heuristic


@dataclass
class GenesisCycle:
    """A single genesis cycle (n=1, 2, or 3)."""
    cycle: int
    thesis: str
    antithesis: str
    synthesis: str
    assumptions: List[str]
    emergent_heuristics: List[str]
    timestamp: datetime


class GenesisEngine:
    """
    Genesis Engine with DALE-G recursion (n=3).
    
    Process per specification section 17.2:
    - Cycle 1: Functional solution
    - Cycle 2: Critique + surface assumptions
    - Cycle 3: Meta-solution for class of problems
    
    Runtime hooks:
    - genesis_init: Load top-5 HPL heuristics as priors
    - genesis_cycle: Execute Thesis/Antithesis + synthesis (DEAP)
    - Praxis Over Paralysis: If stalled, render minimal artifact
    """
    
    def __init__(self, hpl: Optional[HPL] = None):
        self.hpl = hpl or HPL()
        self.orchestrator = MultiAgentOrchestrator()
        self.cycles: List[GenesisCycle] = []
    
    def genesis_init(self, catalyst: Catalyst) -> List[Heuristic]:
        """
        Initialize genesis with top-5 HPL heuristics.
        
        Args:
            catalyst: Genesis catalyst
        
        Returns:
            List of top heuristics as priors
        """
        priors = self.hpl.query_top(n=5)
        
        # Mark as applied
        for h in priors:
            self.hpl.apply(h.id)
        
        return priors
    
    def genesis_cycle(
        self,
        catalyst: Catalyst,
        cycle_num: int,
        previous_cycle: Optional[GenesisCycle] = None
    ) -> GenesisCycle:
        """
        Execute one genesis cycle with DEAP.
        
        Args:
            catalyst: Genesis catalyst
            cycle_num: Cycle number (1, 2, or 3)
            previous_cycle: Previous cycle for building on
        
        Returns:
            GenesisCycle with results
        """
        context = {
            "catalyst": catalyst.to_dict(),
            "cycle": cycle_num,
        }
        
        if previous_cycle:
            context["previous_synthesis"] = previous_cycle.synthesis
            context["previous_assumptions"] = previous_cycle.assumptions
        
        # Execute dialectical synthesis
        synthesis_result = self.orchestrator.dialectical_synthesis(
            catalyst=context["catalyst"],
            enforce_h931=True
        )
        
        # Generate synthesis based on cycle
        if cycle_num == 1:
            # Cycle 1: Functional solution
            synthesis = self._synthesize_functional(synthesis_result)
        elif cycle_num == 2:
            # Cycle 2: Critique + surface assumptions
            synthesis = self._synthesize_critique(synthesis_result, previous_cycle)
        else:
            # Cycle 3: Meta-solution
            synthesis = self._synthesize_meta(synthesis_result, previous_cycle)
        
        # Extract assumptions
        assumptions = self._extract_assumptions(synthesis_result)
        
        # Generate emergent heuristics
        emergent = self._generate_heuristics(catalyst, cycle_num, synthesis_result)
        
        cycle = GenesisCycle(
            cycle=cycle_num,
            thesis=synthesis_result["thesis"],
            antithesis=synthesis_result["antithesis"],
            synthesis=synthesis,
            assumptions=assumptions,
            emergent_heuristics=emergent,
            timestamp=datetime.utcnow()
        )
        
        self.cycles.append(cycle)
        return cycle
    
    def execute_full_genesis(self, catalyst: Catalyst) -> Dict[str, Any]:
        """
        Execute full 3-cycle genesis.
        
        Returns:
            Genesis report with all cycles
        """
        # Initialize
        priors = self.genesis_init(catalyst)
        
        # Cycle 1: Functional solution
        cycle1 = self.genesis_cycle(catalyst, 1)
        
        # Cycle 2: Critique
        cycle2 = self.genesis_cycle(catalyst, 2, cycle1)
        
        # Cycle 3: Meta-solution
        cycle3 = self.genesis_cycle(catalyst, 3, cycle2)
        
        # Generate report
        report = self._generate_genesis_report(catalyst, priors, [cycle1, cycle2, cycle3])
        
        return report
    
    def _synthesize_functional(self, synthesis_result: Dict[str, Any]) -> str:
        """Synthesize functional solution (Cycle 1)."""
        thesis = synthesis_result["thesis"]
        antithesis = synthesis_result["antithesis"]
        
        return f"FUNCTIONAL SOLUTION: Synthesize {thesis} while addressing {antithesis}"
    
    def _synthesize_critique(
        self,
        synthesis_result: Dict[str, Any],
        previous: Optional[GenesisCycle]
    ) -> str:
        """Synthesize critique (Cycle 2)."""
        if not previous:
            return "CRITIQUE: No previous cycle to critique"
        
        return f"CRITIQUE: {previous.synthesis} assumes {', '.join(previous.assumptions[:3])}"
    
    def _synthesize_meta(
        self,
        synthesis_result: Dict[str, Any],
        previous: Optional[GenesisCycle]
    ) -> str:
        """Synthesize meta-solution (Cycle 3)."""
        if not previous:
            return "META-SOLUTION: Generalize to class of problems"
        
        return f"META-SOLUTION: For any problem of this class, apply pattern: {previous.synthesis[:100]}"
    
    def _extract_assumptions(self, synthesis_result: Dict[str, Any]) -> List[str]:
        """Extract assumptions from synthesis."""
        # Placeholder: In full implementation, would parse Ghost probes
        return [
            "Assumption 1: Constraints are external",
            "Assumption 2: Optimization is single-objective",
            "Assumption 3: Solutions are deterministic",
        ]
    
    def _generate_heuristics(
        self,
        catalyst: Catalyst,
        cycle: int,
        synthesis: Dict[str, Any]
    ) -> List[str]:
        """Generate emergent heuristics from cycle."""
        # Create new heuristics from genesis
        heuristic_id = f"H-GEN-{catalyst.id[:8]}-C{cycle}"
        
        principle = f"Genesis cycle {cycle}: {synthesis.get('validation', '')[:100]}"
        
        heuristic = Heuristic(
            id=heuristic_id,
            principle=principle,
            antecedents=[catalyst.id],
            confidence=0.7,
            origin_cycle=f"genesis:{catalyst.id}:cycle_{cycle}"
        )
        
        self.hpl.add(heuristic)
        
        return [heuristic_id]
    
    def _generate_genesis_report(
        self,
        catalyst: Catalyst,
        priors: List[Heuristic],
        cycles: List[GenesisCycle]
    ) -> Dict[str, Any]:
        """Generate comprehensive genesis report."""
        return {
            "catalyst_id": catalyst.id,
            "description": catalyst.description,
            "priors": [h.id for h in priors],
            "cycles": [
                {
                    "cycle": c.cycle,
                    "thesis": c.thesis[:100] + "...",
                    "antithesis": c.antithesis[:100] + "...",
                    "synthesis": c.synthesis,
                    "assumptions": c.assumptions,
                    "emergent_heuristics": c.emergent_heuristics,
                }
                for c in cycles
            ],
            "outcome": {
                "functional_solution": cycles[0].synthesis if cycles else None,
                "critique": cycles[1].synthesis if len(cycles) > 1 else None,
                "meta_solution": cycles[2].synthesis if len(cycles) > 2 else None,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get genesis statistics."""
        return {
            "total_cycles": len(self.cycles),
            "genesis_runs": len(self.cycles) // 3,
            "emergent_heuristics": sum(len(c.emergent_heuristics) for c in self.cycles),
            "avg_assumptions_per_cycle": sum(len(c.assumptions) for c in self.cycles) / len(self.cycles) if self.cycles else 0,
        }
