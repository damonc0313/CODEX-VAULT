"""Mentor-Σ: Knowledge codification and explanation agent."""

from typing import Any, Dict, List
from dataclasses import dataclass
import logging


@dataclass
class TeachingOutput:
    """Teaching and knowledge codification output."""
    
    concepts: List[str]
    explanations: Dict[str, str]
    examples: List[str]
    clarity_score: float


class MentorSigma:
    """
    Mentor-Σ Agent.
    
    Purpose: Codify knowledge and generate explanations
    Meta-reflection: reasoning_transparency()
    """
    
    def __init__(self, metacognition: Any) -> None:
        """Initialize mentor agent."""
        self.logger = logging.getLogger(__name__)
        self.metacognition = metacognition
        self.agent_id = "Mentor-Σ"
        
    def teach(
        self,
        artifact: Any,
        context: Dict[str, Any]
    ) -> TeachingOutput:
        """
        Create teaching materials from artifact.
        
        Args:
            artifact: Artifact to explain
            context: Teaching context
            
        Returns:
            Teaching output with explanations
        """
        # Ensure reasoning transparency
        self.metacognition.reasoning_transparency(
            decision="teach_artifact",
            rationale="Codifying knowledge for propagation"
        )
        
        self.logger.info(f"{self.agent_id}: Creating teaching materials")
        
        # Extract concepts
        concepts = self._extract_concepts(artifact)
        
        # Generate explanations
        explanations = self._generate_explanations(concepts)
        
        # Create examples
        examples = self._create_examples(concepts)
        
        # Calculate clarity
        clarity = self._assess_clarity(explanations, examples)
        
        output = TeachingOutput(
            concepts=concepts,
            explanations=explanations,
            examples=examples,
            clarity_score=clarity
        )
        
        self.logger.info(
            f"{self.agent_id}: Teaching complete - "
            f"{len(concepts)} concepts explained"
        )
        
        return output
        
    def _extract_concepts(self, artifact: Any) -> List[str]:
        """Extract key concepts from artifact."""
        concepts = []
        
        if hasattr(artifact, 'components'):
            concepts.extend(artifact.components)
        elif hasattr(artifact, 'content'):
            # Parse content for concepts
            content = str(artifact.content)
            if 'class' in content:
                concepts.append('object_oriented_design')
            if 'def' in content:
                concepts.append('functional_decomposition')
                
        return concepts
        
    def _generate_explanations(
        self,
        concepts: List[str]
    ) -> Dict[str, str]:
        """Generate explanations for concepts."""
        explanations = {}
        
        for concept in concepts:
            if 'core' in concept:
                explanations[concept] = (
                    "Core module providing central functionality"
                )
            elif 'learning' in concept:
                explanations[concept] = (
                    "Adaptive learning component for improvement"
                )
            else:
                explanations[concept] = f"Component: {concept}"
                
        return explanations
        
    def _create_examples(self, concepts: List[str]) -> List[str]:
        """Create usage examples."""
        examples = []
        
        for concept in concepts[:3]:  # Limit to 3 examples
            examples.append(
                f"# Example usage of {concept}\n"
                f"component = {concept}()\n"
                f"result = component.execute()"
            )
            
        return examples
        
    def _assess_clarity(
        self,
        explanations: Dict[str, str],
        examples: List[str]
    ) -> float:
        """Assess clarity of teaching materials."""
        # Simple clarity metric
        has_explanations = len(explanations) > 0
        has_examples = len(examples) > 0
        
        clarity = 0.5
        if has_explanations:
            clarity += 0.25
        if has_examples:
            clarity += 0.25
            
        return clarity
