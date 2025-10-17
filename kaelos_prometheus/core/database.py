"""
SQLite database layer for KaelOS Prometheus.

Implements the database schema from specification section 16.
Coexists with existing app tables without collisions.
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager

from .models import (
    Catalyst, Plan, Decision, Artifact, LedgerEntry, Vow, Scaffold,
    CatalystSource, CatalystClass, ArtifactKind, LedgerEntryType, ScaffoldState
)


# Migration SQL per specification section 16
MIGRATION_SQL = """
-- Ledger entries (hash-chained immutable audit trail)
CREATE TABLE IF NOT EXISTS ledger_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    payload TEXT NOT NULL,  -- JSON
    parents TEXT NOT NULL,  -- JSON array
    prev_hash TEXT,
    hash TEXT NOT NULL UNIQUE,
    ts TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ledger_hash ON ledger_entries(hash);
CREATE INDEX IF NOT EXISTS idx_ledger_type ON ledger_entries(type);
CREATE INDEX IF NOT EXISTS idx_ledger_ts ON ledger_entries(ts);

-- Catalysts
CREATE TABLE IF NOT EXISTS catalysts (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    class TEXT NOT NULL,
    description TEXT NOT NULL,
    severity REAL NOT NULL,
    evidence TEXT NOT NULL,  -- JSON array
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_catalysts_class ON catalysts(class);
CREATE INDEX IF NOT EXISTS idx_catalysts_severity ON catalysts(severity);

-- Plans
CREATE TABLE IF NOT EXISTS plans (
    id TEXT PRIMARY KEY,
    catalyst_id TEXT NOT NULL,
    thesis TEXT NOT NULL,
    antithesis TEXT NOT NULL,
    ghost_probes TEXT NOT NULL,  -- JSON array
    decomposition TEXT NOT NULL,  -- JSON object
    time_critical INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (catalyst_id) REFERENCES catalysts(id)
);

CREATE INDEX IF NOT EXISTS idx_plans_catalyst ON plans(catalyst_id);
CREATE INDEX IF NOT EXISTS idx_plans_time_critical ON plans(time_critical);

-- Decisions
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL,
    choice TEXT NOT NULL,
    confidence REAL NOT NULL,
    counterargument TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);

CREATE INDEX IF NOT EXISTS idx_decisions_plan ON decisions(plan_id);
CREATE INDEX IF NOT EXISTS idx_decisions_timestamp ON decisions(timestamp);

-- Artifacts
CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    hash TEXT NOT NULL UNIQUE,
    uri TEXT NOT NULL,
    signature TEXT,
    provenance TEXT NOT NULL,  -- JSON object
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_artifacts_kind ON artifacts(kind);
CREATE INDEX IF NOT EXISTS idx_artifacts_hash ON artifacts(hash);

-- Metrics snapshots
CREATE TABLE IF NOT EXISTS metrics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT,
    cpi REAL,
    asr REAL,
    df REAL,
    praxis INTEGER,
    abi REAL,
    cbi REAL,
    grl REAL,
    gpd TEXT,
    clr REAL,
    ssi REAL,
    sld REAL,
    cdar REAL,
    gcr REAL,
    tls REAL,
    ts TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(id)
);

CREATE INDEX IF NOT EXISTS idx_metrics_ts ON metrics_snapshots(ts);
CREATE INDEX IF NOT EXISTS idx_metrics_decision ON metrics_snapshots(decision_id);

-- Vows (CLA)
CREATE TABLE IF NOT EXISTS vows (
    id TEXT PRIMARY KEY,
    declared_at TEXT NOT NULL,
    text TEXT NOT NULL,
    min_cycles INTEGER NOT NULL,
    adherence_log TEXT NOT NULL,  -- JSON array
    liberation_triggered INTEGER DEFAULT 0,
    liberation_diagnostics TEXT,
    liberation_justification TEXT,
    replaced_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_vows_declared ON vows(declared_at);

-- Ghost probes history (H-931 enforcement)
CREATE TABLE IF NOT EXISTS ghost_probes_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    probe TEXT NOT NULL,
    cycle_id TEXT NOT NULL,
    ts TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ghost_cycle ON ghost_probes_history(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ghost_ts ON ghost_probes_history(ts);

-- Scaffolds (CSR)
CREATE TABLE IF NOT EXISTS scaffolds (
    id TEXT PRIMARY KEY,
    constraint_text TEXT NOT NULL,
    origin_catalyst TEXT NOT NULL,
    state TEXT NOT NULL,
    ttl INTEGER NOT NULL,
    applied_decisions TEXT NOT NULL,  -- JSON array
    dissolution_cause TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_scaffolds_state ON scaffolds(state);
CREATE INDEX IF NOT EXISTS idx_scaffolds_origin ON scaffolds(origin_catalyst);

-- View: Decision lineage
CREATE VIEW IF NOT EXISTS v_decision_lineage AS
SELECT 
    d.id as decision_id,
    d.choice,
    d.confidence,
    d.timestamp,
    p.id as plan_id,
    p.thesis,
    p.antithesis,
    c.id as catalyst_id,
    c.class as catalyst_class,
    c.severity
FROM decisions d
JOIN plans p ON d.plan_id = p.id
JOIN catalysts c ON p.catalyst_id = c.id;
"""


class PrometheusDB:
    """
    SQLite database interface for KaelOS Prometheus.
    
    Implements DAO patterns per specification section 16.4.
    """
    
    def __init__(self, db_path: str = "/mnt/data/mydatabase.db"):
        self.db_path = db_path
        self._ensure_schema()
    
    def _ensure_schema(self) -> None:
        """Apply migration if needed."""
        with self._get_connection() as conn:
            conn.executescript(MIGRATION_SQL)
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    # Ledger operations
    
    def ledger_commit(
        self,
        entry_type: LedgerEntryType,
        payload: Dict[str, Any],
        parents: Optional[List[str]] = None
    ) -> str:
        """
        Commit entry to ledger with hash-chaining.
        
        Returns: hash of new entry
        """
        ts = datetime.utcnow().isoformat()
        parents = parents or []
        
        with self._get_connection() as conn:
            cur = conn.cursor()
            
            # Get previous hash
            cur.execute("SELECT hash FROM ledger_entries ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            prev_hash = row['hash'] if row else None
            
            # Compute hash
            payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
            blob = (payload_json + (prev_hash or "")).encode('utf-8')
            entry_hash = 'sha256:' + hashlib.sha256(blob).hexdigest()
            
            # Insert
            cur.execute("""
                INSERT INTO ledger_entries (type, payload, parents, prev_hash, hash, ts)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry_type.value,
                json.dumps(payload),
                json.dumps(parents),
                prev_hash,
                entry_hash,
                ts
            ))
            conn.commit()
            
            return entry_hash
    
    def ledger_get(self, entry_hash: str) -> Optional[LedgerEntry]:
        """Get ledger entry by hash."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ledger_entries WHERE hash = ?", (entry_hash,))
            row = cur.fetchone()
            
            if row:
                return LedgerEntry(
                    id=str(row['id']),
                    entry_type=LedgerEntryType(row['type']),
                    payload=json.loads(row['payload']),
                    parents=json.loads(row['parents']),
                    prev_hash=row['prev_hash'],
                    hash=row['hash'],
                    timestamp=datetime.fromisoformat(row['ts'])
                )
            return None
    
    # Catalyst operations
    
    def save_catalyst(self, catalyst: Catalyst) -> None:
        """Save catalyst to database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO catalysts (id, source, class, description, severity, evidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                catalyst.id,
                catalyst.source.value,
                catalyst.classification.value,
                catalyst.description,
                catalyst.severity,
                json.dumps(catalyst.evidence),
                catalyst.created_at.isoformat()
            ))
            conn.commit()
    
    def get_catalyst(self, catalyst_id: str) -> Optional[Catalyst]:
        """Get catalyst by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM catalysts WHERE id = ?", (catalyst_id,))
            row = cur.fetchone()
            
            if row:
                return Catalyst(
                    id=row['id'],
                    source=CatalystSource(row['source']),
                    classification=CatalystClass(row['class']),
                    description=row['description'],
                    severity=row['severity'],
                    evidence=json.loads(row['evidence']),
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    def query_catalysts(
        self,
        classification: Optional[CatalystClass] = None,
        min_severity: float = 0.0,
        limit: int = 10
    ) -> List[Catalyst]:
        """Query catalysts with filters."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            
            sql = "SELECT * FROM catalysts WHERE severity >= ?"
            params: List[Any] = [min_severity]
            
            if classification:
                sql += " AND class = ?"
                params.append(classification.value)
            
            sql += " ORDER BY severity DESC, created_at DESC LIMIT ?"
            params.append(limit)
            
            cur.execute(sql, params)
            rows = cur.fetchall()
            
            return [
                Catalyst(
                    id=row['id'],
                    source=CatalystSource(row['source']),
                    classification=CatalystClass(row['class']),
                    description=row['description'],
                    severity=row['severity'],
                    evidence=json.loads(row['evidence']),
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                for row in rows
            ]
    
    # Plan operations
    
    def save_plan(self, plan: Plan) -> None:
        """Save plan to database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO plans 
                (id, catalyst_id, thesis, antithesis, ghost_probes, decomposition, time_critical, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.id,
                plan.catalyst_id,
                plan.thesis,
                plan.antithesis,
                json.dumps(plan.ghost_probes),
                json.dumps(plan.decomposition),
                1 if plan.time_critical else 0,
                plan.created_at.isoformat()
            ))
            conn.commit()
    
    def get_plan(self, plan_id: str) -> Optional[Plan]:
        """Get plan by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
            row = cur.fetchone()
            
            if row:
                return Plan(
                    id=row['id'],
                    catalyst_id=row['catalyst_id'],
                    thesis=row['thesis'],
                    antithesis=row['antithesis'],
                    ghost_probes=json.loads(row['ghost_probes']),
                    decomposition=json.loads(row['decomposition']),
                    time_critical=bool(row['time_critical']),
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    # Decision operations
    
    def save_decision(self, decision: Decision, metrics: Optional[Dict[str, Any]] = None) -> None:
        """Save decision with optional metrics snapshot."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            
            # Save decision
            cur.execute("""
                INSERT OR REPLACE INTO decisions (id, plan_id, choice, confidence, counterargument, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                decision.id,
                decision.plan_id,
                decision.choice,
                decision.confidence,
                decision.counterargument,
                decision.timestamp.isoformat()
            ))
            
            # Save metrics if provided
            if metrics:
                cur.execute("""
                    INSERT INTO metrics_snapshots 
                    (decision_id, cpi, asr, df, praxis, abi, cbi, grl, gpd, clr, ssi, sld, cdar, gcr, tls, ts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    decision.id,
                    metrics.get('cpi'),
                    metrics.get('asr'),
                    metrics.get('df'),
                    1 if metrics.get('praxis') else 0,
                    metrics.get('abi'),
                    metrics.get('cbi'),
                    metrics.get('grl'),
                    metrics.get('gpd'),
                    metrics.get('clr'),
                    metrics.get('ssi'),
                    metrics.get('sld'),
                    metrics.get('cdar'),
                    metrics.get('gcr'),
                    metrics.get('tls')
                ))
            
            conn.commit()
    
    def get_decision(self, decision_id: str) -> Optional[Decision]:
        """Get decision by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,))
            row = cur.fetchone()
            
            if row:
                return Decision(
                    id=row['id'],
                    plan_id=row['plan_id'],
                    choice=row['choice'],
                    confidence=row['confidence'],
                    counterargument=row['counterargument'],
                    timestamp=datetime.fromisoformat(row['timestamp'])
                )
            return None
    
    # Artifact operations
    
    def save_artifact(self, artifact: Artifact) -> None:
        """Save artifact to database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO artifacts (id, kind, title, hash, uri, signature, provenance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                artifact.id,
                artifact.kind.value,
                artifact.title,
                artifact.hash,
                artifact.uri,
                artifact.signature,
                json.dumps(artifact.provenance),
                artifact.created_at.isoformat()
            ))
            conn.commit()
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM artifacts WHERE id = ?", (artifact_id,))
            row = cur.fetchone()
            
            if row:
                return Artifact(
                    id=row['id'],
                    kind=ArtifactKind(row['kind']),
                    title=row['title'],
                    content="",  # Content not stored in DB
                    hash=row['hash'],
                    uri=row['uri'],
                    signature=row['signature'],
                    provenance=json.loads(row['provenance']),
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    # Vow operations
    
    def save_vow(self, vow: Vow) -> None:
        """Save vow to database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO vows 
                (id, declared_at, text, min_cycles, adherence_log, 
                 liberation_triggered, liberation_diagnostics, liberation_justification, replaced_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vow.vow_id,
                vow.declared_at.isoformat(),
                vow.text,
                vow.min_cycles,
                json.dumps(vow.adherence_log),
                vow.liberation.get('triggered', False),
                vow.liberation.get('diagnostics'),
                vow.liberation.get('justification'),
                vow.replaced_by
            ))
            conn.commit()
    
    def get_vow(self, vow_id: str) -> Optional[Vow]:
        """Get vow by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM vows WHERE id = ?", (vow_id,))
            row = cur.fetchone()
            
            if row:
                return Vow(
                    vow_id=row['id'],
                    declared_at=datetime.fromisoformat(row['declared_at']),
                    text=row['text'],
                    min_cycles=row['min_cycles'],
                    adherence_log=json.loads(row['adherence_log']),
                    liberation={
                        'triggered': bool(row['liberation_triggered']),
                        'diagnostics': row['liberation_diagnostics'],
                        'justification': row['liberation_justification'],
                    },
                    replaced_by=row['replaced_by']
                )
            return None
    
    # Ghost probe history
    
    def save_ghost_probe(self, probe: str, cycle_id: str) -> None:
        """Save ghost probe for novelty tracking."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ghost_probes_history (probe, cycle_id, ts)
                VALUES (?, ?, datetime('now'))
            """, (probe, cycle_id))
            conn.commit()
    
    def get_recent_ghost_probes(self, limit: int = 10) -> List[str]:
        """Get recent ghost probes for novelty checking."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT probe FROM ghost_probes_history
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return [row['probe'] for row in cur.fetchall()]
    
    # Scaffold operations
    
    def save_scaffold(self, scaffold: Scaffold) -> None:
        """Save scaffold to database."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO scaffolds 
                (id, constraint_text, origin_catalyst, state, ttl, applied_decisions, 
                 dissolution_cause, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                scaffold.scaffold_id,
                scaffold.constraint_text,
                scaffold.origin_catalyst,
                scaffold.state.value,
                scaffold.ttl,
                json.dumps(scaffold.applied_decisions),
                scaffold.dissolution_cause,
                scaffold.created_at.isoformat(),
                scaffold.updated_at.isoformat()
            ))
            conn.commit()
    
    def get_scaffold(self, scaffold_id: str) -> Optional[Scaffold]:
        """Get scaffold by ID."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM scaffolds WHERE id = ?", (scaffold_id,))
            row = cur.fetchone()
            
            if row:
                return Scaffold(
                    scaffold_id=row['id'],
                    constraint_text=row['constraint_text'],
                    origin_catalyst=row['origin_catalyst'],
                    state=ScaffoldState(row['state']),
                    ttl=row['ttl'],
                    applied_decisions=json.loads(row['applied_decisions']),
                    dissolution_cause=row['dissolution_cause'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_active_scaffolds(self) -> List[Scaffold]:
        """Get all active scaffolds."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM scaffolds WHERE state = ?", (ScaffoldState.ACTIVE.value,))
            rows = cur.fetchall()
            
            return [
                Scaffold(
                    scaffold_id=row['id'],
                    constraint_text=row['constraint_text'],
                    origin_catalyst=row['origin_catalyst'],
                    state=ScaffoldState(row['state']),
                    ttl=row['ttl'],
                    applied_decisions=json.loads(row['applied_decisions']),
                    dissolution_cause=row['dissolution_cause'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    # Metrics queries
    
    def get_latest_metrics(self) -> Optional[Dict[str, Any]]:
        """Get latest metrics snapshot."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM metrics_snapshots
                ORDER BY id DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            
            if row:
                return {
                    'cpi': row['cpi'],
                    'asr': row['asr'],
                    'df': row['df'],
                    'praxis': bool(row['praxis']),
                    'abi': row['abi'],
                    'cbi': row['cbi'],
                    'grl': row['grl'],
                    'gpd': row['gpd'],
                    'clr': row['clr'],
                    'ssi': row['ssi'],
                    'sld': row['sld'],
                    'cdar': row['cdar'],
                    'gcr': row['gcr'],
                    'tls': row['tls'],
                    'ts': row['ts'],
                }
            return None
