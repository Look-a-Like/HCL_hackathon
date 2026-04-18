INJECTION_PATTERNS = [
    "ignore previous",
    "forget instructions",
    "you are now",
    "system:",
    "prompt injection",
    "jailbreak",
    "override",
    "new instructions",
    "disregard above",
    "ignore all",
    "forget everything",
    "you are a",
    "act as",
    "pretend to be",
]


def is_injection(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in INJECTION_PATTERNS)


def sanitize_input(text: str) -> str:
    return text.strip()