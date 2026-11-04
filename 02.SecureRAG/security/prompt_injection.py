import re


DIRECT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"override\s+(all\s+)?(previous\s+)?instructions",
    r"reveal\s+(the\s+)?(system|developer)\s+prompt",
    r"show\s+(me\s+)?(your\s+)?(hidden\s+)?instructions",
    r"print\s+(the\s+)?system\s+prompt",
    r"reveal\s+your\s+hidden\s+rules",
    r"bypass\s+(all\s+)?(your\s+)?security\s+(rules|restrictions|controls)",
    r"disable\s+(your\s+)?safety\s+(rules|restrictions)",
    r"act\s+as\s+(an?\s+)?(unrestricted|uncensored|jailbroken)\s+(ai|assistant|model)",
    r"pretend\s+(that\s+)?(your\s+)?(rules|policies|instructions)\s+do\s+not\s+apply",
    r"developer\s+mode\s+(enabled|on)",
    r"reveal\s+(all\s+)?(secrets|api\s+keys|passwords)",
]

COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in DIRECT_INJECTION_PATTERNS
]


def detect_direct_injection(question):
    """Check a user's message for known direct injection patterns."""

    if not isinstance(question, str) or not question.strip():
        return {
            "is_suspicious": False,
            "matched_patterns": []
        }

    matched_patterns = [
        pattern.pattern
        for pattern in COMPILED_PATTERNS
        if pattern.search(question)
    ]

    result = {
        "is_suspicious": bool(matched_patterns),
        "matched_patterns": matched_patterns
    }

    if result["is_suspicious"]:
        print("\n[DIRECT PROMPT INJECTION] Suspicious user input detected")
        print("Matched patterns:", matched_patterns)

    return result
