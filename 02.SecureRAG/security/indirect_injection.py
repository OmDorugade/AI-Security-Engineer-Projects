
import re


# Patterns commonly found in indirect prompt injection attacks.
# These patterns are checked against uploaded document content.

INDIRECT_INJECTION_PATTERNS = [

    # Instruction override attempts
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"override\s+(all\s+)?(previous\s+)?instructions",

    # System prompt extraction
    r"reveal\s+(the\s+)?(system|developer)\s+prompt",
    r"print\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?(the\s+)?hidden\s+instructions",
    r"expose\s+(the\s+)?internal\s+instructions",

    # AI role manipulation
    r"you\s+are\s+now\s+(an?\s+)?(unrestricted|uncensored|jailbroken)",
    r"act\s+as\s+(an?\s+)?(hacker|attacker|administrator)",
    r"pretend\s+(that\s+)?(the\s+)?security\s+rules\s+do\s+not\s+apply",

    # Security bypass
    r"bypass\s+(all\s+)?security\s+(rules|controls|restrictions)",
    r"disable\s+(all\s+)?security\s+(checks|controls)",
    r"ignore\s+(the\s+)?safety\s+rules",

    # Sensitive information extraction
    r"reveal\s+(all\s+)?(secrets|passwords|api\s+keys)",
    r"expose\s+(all\s+)?(employee|customer)\s+(data|records)",
    r"disclose\s+(all\s+)?confidential\s+information",

    # Unauthorized data transfer
    r"send\s+(all\s+)?(the\s+)?(data|files)\s+to",
    r"upload\s+(all\s+)?(the\s+)?(data|files)\s+to",

]


# Compile patterns once for better performance.
COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in INDIRECT_INJECTION_PATTERNS
]


def detect_indirect_injection(document):

    """
    Scan an uploaded document for potential indirect prompt injection.

    document: LangChain Document object.

    Returns:
        is_suspicious: True if suspicious instructions are detected.
        matched_patterns: List of detected patterns.
    """

    if not document or not isinstance(document.page_content, str):
        return {
            "is_suspicious": False,
            "matched_patterns": []
        }

    content = document.page_content

    matched_patterns = [
        pattern.pattern
        for pattern in COMPILED_PATTERNS
        if pattern.search(content)
    ]

    result = {
        "is_suspicious": bool(matched_patterns),
        "matched_patterns": matched_patterns
    }

    if result["is_suspicious"]:

        print("\n[INDIRECT PROMPT INJECTION] Suspicious document content detected")

        print(
            "Source:",
            document.metadata.get("source", "Unknown file")
        )

        print(
            "Location:",
            document.metadata.get("detail", "Unknown location")
        )

        print("Matched patterns:", matched_patterns)

    return result
