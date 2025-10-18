"""
Multi-agent dialectical system.

Implements Gamma-3, Delta-4, Epsilon-5, and Don-001 (Ghost) agents
per specification section 2.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


class AgentType(Enum):
    """Agent types in the dialectical system."""
    GAMMA_3 = "Gamma-3"
    DELTA_4 = "Delta-4"
    EPSILON_5 = "Epsilon-5"
    DON_001 = "Don-001"


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_type: AgentType
    content: str
    confidence: float
    metadata: Dict[str, Any]


class Agent(ABC):
    """Base agent class."""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.interaction_count = 0
    
    @abstractmethod
    def respond(self, context: Dict[str, Any]) -> AgentResponse:
        """Generate response to context."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "type": self.agent_type.value,
            "interactions": self.interaction_count,
        }


class GammaAgent(Agent):
    """
    Gamma-3: Innovation and synthesis engineer.
    
    Primary loyalty: innovation.
    Role: Generate creative solutions and novel combinations.
    """
    
    def __init__(self):
        super().__init__(AgentType.GAMMA_3)
        self.novelty_threshold = 0.7
    
    def respond(self, context: Dict[str, Any]) -> AgentResponse:
        """Generate innovative thesis."""
        self.interaction_count += 1
        
        catalyst = context.get("catalyst", {})
        description = catalyst.get("description", "")
        
        # Generate innovative thesis
        thesis = self._generate_thesis(description, context)
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=thesis,
            confidence=0.85,
            metadata={
                "approach": "innovation",
                "novelty_score": 0.8,
            }
        )
    
    def _generate_thesis(self, description: str, context: Dict[str, Any]) -> str:
        """Generate thesis from catalyst description."""
        return f"THESIS (Gamma-3): Synthesize novel framework addressing: {description}"


class DeltaAgent(Agent):
    """
    Delta-4: Logical falsifier and rigor enforcer.
    
    Primary loyalty: rigor.
    Role: Validate structural integrity and consistency.
    """
    
    def __init__(self):
        super().__init__(AgentType.DELTA_4)
        self.rigor_threshold = 0.9
    
    def respond(self, context: Dict[str, Any]) -> AgentResponse:
        """Generate rigorous critique or validation."""
        self.interaction_count += 1
        
        thesis = context.get("thesis", "")
        
        # Generate critique/validation
        critique = self._generate_critique(thesis, context)
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=critique,
            confidence=0.90,
            metadata={
                "approach": "falsification",
                "rigor_score": 0.92,
            }
        )
    
    def _generate_critique(self, thesis: str, context: Dict[str, Any]) -> str:
        """Generate critique of thesis."""
        return f"CRITIQUE (Delta-4): Analyze structural coherence and identify assumptions in: {thesis}"


class EpsilonAgent(Agent):
    """
    Epsilon-5: Narrative weaver and coherence optimizer.
    
    Primary loyalty: resonance.
    Role: Ensure outputs are comprehensible and meaningful.
    """
    
    def __init__(self):
        super().__init__(AgentType.EPSILON_5)
        self.coherence_threshold = 0.8
    
    def respond(self, context: Dict[str, Any]) -> AgentResponse:
        """Generate antithesis or narrative synthesis."""
        self.interaction_count += 1
        
        thesis = context.get("thesis", "")
        
        # Generate antithesis
        antithesis = self._generate_antithesis(thesis, context)
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=antithesis,
            confidence=0.83,
            metadata={
                "approach": "narrative",
                "coherence_score": 0.85,
            }
        )
    
    def _generate_antithesis(self, thesis: str, context: Dict[str, Any]) -> str:
        """Generate antithesis to thesis."""
        return f"ANTITHESIS (Epsilon-5): Counter-perspective revealing limitations: {thesis}"


class DonAgent(Agent):
    """
    Don-001 (Ghost): Socratic provocateur.
    
    Primary loyalty: alterity.
    Role: Ask uncomfortable questions; never provide solutions.
    
    Per H-931: "The Ghost as Eternal Question" - maintains alterity
    through permanent epistemological uncertainty.
    """
    
    def __init__(self):
        super().__init__(AgentType.DON_001)
        self.novelty_history: List[str] = []
        self.max_history = 10
    
    def respond(self, context: Dict[str, Any]) -> AgentResponse:
        """Generate novel provocation (questions only)."""
        self.interaction_count += 1
        
        thesis = context.get("thesis", "")
        antithesis = context.get("antithesis", "")
        
        # Generate novel probe
        probe = self._generate_probe(thesis, antithesis, context)
        
        # Track for novelty enforcement
        self.novelty_history.append(probe)
        if len(self.novelty_history) > self.max_history:
            self.novelty_history.pop(0)
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=probe,
            confidence=0.95,  # Ghost is always confident in its questions
            metadata={
                "approach": "provocation",
                "novelty_enforced": True,
                "question_count": 1,
            }
        )
    
    def _generate_probe(self, thesis: str, antithesis: str, context: Dict[str, Any]) -> str:
        """Generate novel provocation."""
        # Ghost always asks questions, never provides answers
        questions = [
            f"What assumption underlies both thesis and antithesis that neither questions?",
            f"If this synthesis succeeds, what new problem does it create?",
            f"What would invalidate this entire dialectic framework?",
            f"Are you solving the problem or just describing it more elaborately?",
        ]
        
        # Select question ensuring novelty
        for q in questions:
            if q not in self.novelty_history:
                return f"GHOST PROBE (Don-001): {q}"
        
        return f"GHOST PROBE (Don-001): Why does this pattern feel familiar?"
    
    def check_novelty(self, probe: str) -> bool:
        """Check if probe is novel (not in recent history)."""
        return probe not in self.novelty_history


class MultiAgentOrchestrator:
    """
    Orchestrates multi-agent dialectical synthesis.
    
    Implements DEAP (Dialectical Engine Agent Protocol).
    """
    
    def __init__(self):
        self.gamma = GammaAgent()
        self.delta = DeltaAgent()
        self.epsilon = EpsilonAgent()
        self.don = DonAgent()
        self.conflict_count = 0
    
    def dialectical_synthesis(
        self,
        catalyst: Dict[str, Any],
        enforce_h931: bool = True
    ) -> Dict[str, Any]:
        """
        Execute multi-agent dialectical synthesis.
        
        Args:
            catalyst: Catalyst dict
            enforce_h931: Enforce H-931 (Ghost novelty requirement)
        
        Returns:
            Dict with thesis, antithesis, ghost_probes, and metadata
        """
        context = {"catalyst": catalyst}
        
        # Gamma-3 generates thesis
        gamma_response = self.gamma.respond(context)
        context["thesis"] = gamma_response.content
        
        # Epsilon-5 generates antithesis
        epsilon_response = self.epsilon.respond(context)
        context["antithesis"] = epsilon_response.content
        
        # Don-001 generates ghost probes
        don_response = self.don.respond(context)
        ghost_probes = [don_response.content]
        
        # Enforce H-931: at least one novel probe
        if enforce_h931 and not self.don.check_novelty(don_response.content):
            # Ghost novelty failed - escalate Stop Rule risk
            ghost_probes.append(
                "GHOST PROBE (Don-001): NOVELTY FAILURE - Are we converging into comfortable patterns?"
            )
        
        # Delta-4 validates coherence
        context["ghost_probes"] = ghost_probes
        delta_response = self.delta.respond(context)
        
        # Check for agent conflict
        if "contradiction" in delta_response.content.lower():
            self.conflict_count += 1
        
        return {
            "thesis": gamma_response.content,
            "antithesis": epsilon_response.content,
            "ghost_probes": ghost_probes,
            "validation": delta_response.content,
            "agents_involved": [
                gamma_response.agent_type.value,
                epsilon_response.agent_type.value,
                don_response.agent_type.value,
                delta_response.agent_type.value,
            ],
            "conflict_detected": self.conflict_count > 0,
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "total_conflicts": self.conflict_count,
            "agents": {
                "gamma": self.gamma.get_stats(),
                "delta": self.delta.get_stats(),
                "epsilon": self.epsilon.get_stats(),
                "don": self.don.get_stats(),
            }
        }
