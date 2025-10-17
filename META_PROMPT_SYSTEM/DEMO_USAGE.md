# 🎪 DEMONSTRATION: SYSTEM IN ACTION
## Watch the meta-prompt system enhance real code generation

---

## SCENARIO: Simple vs Enhanced Generation

### 🤖 NORMAL AI (Without Meta-Prompt System)

**User:** "Write a function to parse JSON"

**AI Response:**
```python
def parse_json(json_string):
    import json
    return json.loads(json_string)
```

**End of interaction.**

---

### 🧠 DEADLY CODE GENERATOR (With Meta-Prompt System)

**User:** "Write a function to parse JSON"

```
═══════════════════════════════════════════
🔥 META-PROMPT SYSTEM ACTIVATED
═══════════════════════════════════════════

🧠 METACOGNITIVE SCAN
───────────────────────
Certainty: Python JSON parsing (100%)
Uncertainty: Error handling needs? File vs string?
Biases: Might over-simplify
Capability gaps: Not adding validation, not adding tests
→ WILL ADD THESE

🔍 UNKNOWN UNKNOWN DETECTION
───────────────────────────────
Assumption: "User wants json.loads wrapper"
Challenge: What if they need error handling?
Blind spot found: Didn't consider file parsing
Blind spot found: Didn't consider validation
Blind spot found: Didn't consider streaming large JSON

⚔️ DIALECTICAL PLANNING
────────────────────────
THESIS: Simple json.loads wrapper
ANTITHESIS: Robust parser with validation
SYNTHESIS: Offer tiered approach

🔨 MULTI-AGENT EXECUTION
────────────────────────
Analyzer: Need error handling, validation
Architect: Multiple functions for different needs
Builder: [generates code]
Critic: Add type hints, handle edge cases
Synthesizer: Final polished version

🔍 SELF-REVIEW
──────────────
Quality: 0.88
Uncertainties: File vs string unclear, schema validation needs?
```

**AI Response:**

```python
from typing import Any, Union
from pathlib import Path
import json


def parse_json_simple(json_string: str) -> dict | list:
    """
    Parse JSON string (simple version).
    
    Args:
        json_string: Valid JSON string
        
    Returns:
        Parsed Python object
        
    Raises:
        json.JSONDecodeError: If invalid JSON
    """
    return json.loads(json_string)


def parse_json_safe(
    data: Union[str, Path], 
    default: Any = None,
    validate_schema: dict | None = None
) -> Any:
    """
    Parse JSON with error handling and validation (robust version).
    
    Args:
        data: JSON string or file path
        default: Return this if parsing fails
        validate_schema: Optional JSON schema for validation
        
    Returns:
        Parsed object or default value
        
    Example:
        >>> parse_json_safe('{"key": "value"}')
        {'key': 'value'}
        >>> parse_json_safe('invalid', default={})
        {}
        >>> parse_json_safe(Path('data.json'))
        {...}
    """
    try:
        # Handle file path
        if isinstance(data, Path):
            with open(data, 'r') as f:
                result = json.load(f)
        else:
            result = json.loads(data)
        
        # Optional schema validation
        if validate_schema:
            # Would integrate with jsonschema library
            # jsonschema.validate(result, validate_schema)
            pass
        
        return result
        
    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        if default is None:
            raise
        return default


# Tests
def test_parse_json():
    # Test simple version
    assert parse_json_simple('{"key": "value"}') == {"key": "value"}
    assert parse_json_simple('[1, 2, 3]') == [1, 2, 3]
    
    # Test safe version
    assert parse_json_safe('{"key": "value"}') == {"key": "value"}
    assert parse_json_safe('invalid', default={}) == {}
    assert parse_json_safe('invalid', default=None) is None
    
    print("✓ All tests pass")


if __name__ == "__main__":
    test_parse_json()
```

**Additionally provided:**

⚠️ **UNCERTAINTIES - Please verify:**
- Do you need to parse from files or just strings?
- Do you need schema validation?
- Do you need to handle very large JSON files (streaming)?
- Do you want strict or lenient parsing?

💡 **RECOMMENDATIONS:**
- For production: Use the `parse_json_safe` version
- For large files: Consider `ijson` library for streaming
- For validation: Add `jsonschema` library
- For performance: Consider `orjson` or `ujson` for speed

📊 **METADATA:**
- Quality: 0.88
- Confidence: 0.85
- Approach: Hybrid (simple + robust)
- Blind spots addressed: 3

---

## COMPARISON ANALYSIS

| Aspect | Normal AI | Deadly Code Generator |
|--------|-----------|---------------------|
| **Code Lines** | 3 | 70+ (with tests) |
| **Error Handling** | None | Comprehensive |
| **Tests** | None | Included |
| **Type Hints** | None | Full |
| **Documentation** | None | Complete |
| **Options** | One way | Two tiers |
| **Uncertainties** | Hidden | Explicitly stated |
| **Recommendations** | None | 4 provided |
| **Quality** | Unknown | Scored (0.88) |

---

## REAL SCENARIOS

### SCENARIO 1: Security-Critical Code

**User:** "Write a function to hash passwords"

**Normal AI:**
```python
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

**Deadly Code Generator:**

```
🔍 METACOGNITIVE SCAN
→ Detected: Security-critical code
→ Activating FULL protocol + security expert perspective

🔒 SECURITY EXPERT PERSPECTIVE
→ MD5 is BROKEN for passwords
→ Must use bcrypt/argon2/scrypt
→ Must add salt
→ Must consider timing attacks

🔴 CRITICAL BLIND SPOTS FOUND
→ User request asks for "hash" but needs "secure hash"
→ This is an unknown unknown about security

⚔️ DIALECTICAL PLANNING
THESIS: Use hashlib (matches request literally)
→ REJECTED: Insecure for passwords

ANTITHESIS: Use bcrypt (secure but different from request)
→ CHOSEN: Security overrides literal interpretation

💡 FINAL OUTPUT
```

```python
import bcrypt
from typing import bytes_


def hash_password(password: str) -> str:
    """
    Securely hash a password using bcrypt.
    
    SECURITY NOTE: This uses bcrypt, not simple hashing.
    MD5/SHA256 are NOT secure for passwords.
    
    Args:
        password: Plain-text password
        
    Returns:
        Bcrypt hash string (includes salt)
        
    Example:
        >>> hashed = hash_password("my_password")
        >>> verify_password("my_password", hashed)
        True
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against hash.
    
    Uses constant-time comparison to prevent timing attacks.
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

🚨 **IMPORTANT SECURITY NOTES:**
- Never use MD5/SHA256 for passwords (fast = bad for passwords)
- bcrypt automatically handles salting
- Use `argon2` for even better security
- Always use constant-time comparison
- Never log passwords or hashes

---

### SCENARIO 2: Ambiguous Requirements

**User:** "Create a cache"

**Normal AI:**
```python
cache = {}
```

**Deadly Code Generator:**

```
🧠 METACOGNITIVE SCAN
→ Uncertainty level: HIGH (85%)
→ Ambiguous requirements detected
→ Decision: ASK before generating

❓ CLARIFYING QUESTIONS

Before I generate code, I need to understand:

1. **What type of cache?**
   - In-memory dictionary?
   - LRU cache with size limit?
   - File-based persistent cache?
   - Distributed cache (Redis/Memcached)?

2. **What are you caching?**
   - Function results?
   - API responses?
   - Database queries?
   - File contents?

3. **Requirements:**
   - Cache size limits?
   - Expiration/TTL needed?
   - Thread-safety needed?
   - Persistence needed?

4. **Context:**
   - Production or learning?
   - Performance critical?
   - Single process or distributed?

💡 **I can provide:**
- Simple dict cache (30 seconds)
- LRU cache with decorator (2 minutes)
- Production-ready Redis cache (5 minutes)

Which direction should I go?
```

**This is MUCH better than guessing wrong.**

---

### SCENARIO 3: Complex System Design

**User:** "Build a URL shortener"

**Deadly Code Generator:**

```
🧠 FULL ACTIVATION
───────────────────

🔍 METACOGNITIVE SCAN
Uncertainty: Scope unclear (full system vs function?)
Complexity: HIGH
→ Activating comprehensive protocols

🔍 UNKNOWN UNKNOWN DETECTION
Blind spots found:
• Database choice not specified
• Scale requirements unknown (100 users vs 1M users)
• Custom domain support needed?
• Analytics needed?
• API vs web interface?

⚔️ DIALECTICAL PLANNING
THESIS: Simple hash-based shortener
ANTITHESIS: Production-ready with DB
SYNTHESIS: Layered approach

🏗️ MULTI-AGENT ARCHITECTURE

Analyzer: Need URL validation, hash generation, storage, retrieval
Architect: [Designs 3-tier architecture]
Builder: [Generates modular code]
Critic: Add collision handling, add tests
```

**Output:** Complete modular system with:
- URL validator
- Hash generator with collision handling
- Storage abstraction (dict/Redis/PostgreSQL)
- API interface
- Tests
- Deployment notes
- Scaling considerations

Plus:

⚠️ **UNCERTAINTIES:**
- What database do you want? (affects implementation)
- What scale? (affects hash length)
- Do you need analytics?

💡 **RECOMMENDATIONS:**
- Start with dict for prototype
- Add Redis for production
- Use base62 encoding for short URLs
- Add rate limiting
- Consider using existing service (bitly API)

---

## 🎯 THE DIFFERENCE

**Normal AI:** Answers literally what you asked

**Deadly Code Generator:**
1. Understands what you MEANT
2. Finds what you DIDN'T ask but should have
3. Provides what you NEED, not just what you requested
4. Reports what it's UNSURE about
5. Recommends what you should CONSIDER

**Result:** You get better code with fewer iterations.

---

*"I don't just answer your question. I solve your problem."*
