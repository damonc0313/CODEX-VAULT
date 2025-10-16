"""Knowledge Integration System for external wisdom processing."""

from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import logging


@dataclass
class KnowledgeArtifact:
    """Represents an external knowledge artifact."""
    
    path: Path
    artifact_type: str
    title: str
    concepts: List[str]
    integration_status: str
    priority: int = 5


class KnowledgeIntegrator:
    """
    Knowledge Integration System.
    
    Designed to process external wisdom sources and integrate them
    into the Codex cognitive framework. Currently supports:
    - Detection of knowledge artifacts
    - Metadata extraction
    - Priority ranking
    - Integration planning
    
    Future capabilities:
    - PDF text extraction
    - Concept extraction via NLP
    - Knowledge graph construction
    - Semantic integration with COT records
    """
    
    def __init__(self, workspace_path: str = "/workspace") -> None:
        """Initialize knowledge integrator."""
        self.logger = logging.getLogger(__name__)
        self.workspace = Path(workspace_path)
        self.artifacts: List[KnowledgeArtifact] = []
        
    def discover_artifacts(
        self,
        extensions: List[str] = ['.pdf', '.txt', '.md']
    ) -> List[KnowledgeArtifact]:
        """
        Discover knowledge artifacts in workspace.
        
        Args:
            extensions: File extensions to search for
            
        Returns:
            List of discovered artifacts
        """
        discovered = []
        
        for ext in extensions:
            files = list(self.workspace.glob(f'*{ext}'))
            
            for file_path in files:
                artifact = self._create_artifact_metadata(file_path)
                discovered.append(artifact)
                
        self.artifacts = discovered
        self.logger.info(f"Discovered {len(discovered)} knowledge artifacts")
        
        return discovered
        
    def prioritize_artifacts(self) -> List[KnowledgeArtifact]:
        """
        Prioritize artifacts for integration.
        
        Returns:
            Sorted list by priority (higher priority first)
        """
        # Priority scoring based on filename patterns
        for artifact in self.artifacts:
            title_lower = artifact.title.lower()
            
            # High priority keywords
            if any(kw in title_lower for kw in [
                'cognitive', 'autonomous', 'framework',
                'scaffolding', 'intelligence'
            ]):
                artifact.priority = 9
                
            # Medium priority
            elif any(kw in title_lower for kw in [
                'protocol', 'system', 'architecture'
            ]):
                artifact.priority = 7
                
            # Foundation documents
            elif any(kw in title_lower for kw in [
                'genesis', 'foundry', 'kael'
            ]):
                artifact.priority = 8
                
        # Sort by priority
        prioritized = sorted(
            self.artifacts,
            key=lambda a: a.priority,
            reverse=True
        )
        
        return prioritized
        
    def extract_concepts(
        self,
        artifact: KnowledgeArtifact
    ) -> List[str]:
        """
        Extract key concepts from artifact.
        
        Args:
            artifact: Knowledge artifact to analyze
            
        Returns:
            List of extracted concepts
        """
        concepts = []
        
        # Extract from title
        title_words = artifact.title.replace('-', ' ').split()
        
        # Filter for significant terms
        significant_terms = [
            word for word in title_words
            if len(word) > 4 and word[0].isupper()
        ]
        
        concepts.extend(significant_terms[:5])
        
        # Infer domain concepts
        if 'cognitive' in artifact.title.lower():
            concepts.append('metacognition')
        if 'autonomous' in artifact.title.lower():
            concepts.append('autonomy')
        if 'scaffolding' in artifact.title.lower():
            concepts.append('learning_framework')
            
        return list(set(concepts))
        
    def plan_integration(
        self,
        artifacts: Optional[List[KnowledgeArtifact]] = None
    ) -> Dict[str, Any]:
        """
        Create integration plan for knowledge artifacts.
        
        Args:
            artifacts: Artifacts to integrate (defaults to all)
            
        Returns:
            Integration plan
        """
        if artifacts is None:
            artifacts = self.prioritize_artifacts()
            
        plan = {
            'total_artifacts': len(artifacts),
            'high_priority': [
                a for a in artifacts if a.priority >= 8
            ],
            'medium_priority': [
                a for a in artifacts if 5 <= a.priority < 8
            ],
            'integration_phases': [],
            'estimated_concepts': 0
        }
        
        # Create phased integration plan
        for i, artifact in enumerate(artifacts[:5], 1):
            concepts = self.extract_concepts(artifact)
            plan['integration_phases'].append({
                'phase': i,
                'artifact': artifact.title,
                'priority': artifact.priority,
                'concepts': concepts,
                'status': 'planned'
            })
            plan['estimated_concepts'] += len(concepts)
            
        return plan
        
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status.
        
        Returns:
            Status report
        """
        if not self.artifacts:
            self.discover_artifacts()
            
        prioritized = self.prioritize_artifacts()
        plan = self.plan_integration(prioritized)
        
        return {
            'artifacts_discovered': len(self.artifacts),
            'high_priority_count': len(plan['high_priority']),
            'integration_plan': plan,
            'next_steps': self._generate_next_steps(plan)
        }
        
    def _create_artifact_metadata(
        self,
        file_path: Path
    ) -> KnowledgeArtifact:
        """Create artifact metadata from file."""
        title = file_path.stem
        artifact_type = file_path.suffix[1:]  # Remove dot
        
        # Extract initial concepts from filename
        concepts = self.extract_concepts(
            KnowledgeArtifact(
                path=file_path,
                artifact_type=artifact_type,
                title=title,
                concepts=[],
                integration_status='discovered',
                priority=5
            )
        )
        
        return KnowledgeArtifact(
            path=file_path,
            artifact_type=artifact_type,
            title=title,
            concepts=concepts,
            integration_status='discovered',
            priority=5
        )
        
    def _generate_next_steps(self, plan: Dict[str, Any]) -> List[str]:
        """Generate next steps for integration."""
        steps = []
        
        if plan['high_priority']:
            steps.append(
                f"Process {len(plan['high_priority'])} "
                "high-priority artifacts first"
            )
            
        steps.append(
            f"Extract and integrate {plan['estimated_concepts']} "
            "estimated concepts"
        )
        
        steps.append(
            "Cross-reference concepts with existing COT records"
        )
        
        steps.append(
            "Update Codex knowledge base with integrated wisdom"
        )
        
        return steps
