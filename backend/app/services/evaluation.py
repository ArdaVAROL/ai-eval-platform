import re
from difflib import SequenceMatcher


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = re.sub(r"\s+", " ", value.strip().lower())
    return re.sub(r"[^\w\s]", "", normalized)


def evaluate_output(output_text: str, expected_output: str | None) -> tuple[bool, float]:
    expected = _normalize_text(expected_output)
    actual = _normalize_text(output_text)

    if not expected:
        return True, 1.0
    if not actual:
        return False, 0.0
    if expected in actual:
        return True, 1.0

    expected_tokens = [token for token in expected.split(" ") if token]
    actual_tokens = set(token for token in actual.split(" ") if token)
    overlap_count = sum(1 for token in expected_tokens if token in actual_tokens)
    overlap_ratio = overlap_count / max(len(expected_tokens), 1)
    similarity = SequenceMatcher(None, actual, expected).ratio()

    passed = overlap_ratio >= 0.6 or similarity >= 0.72
    score = round(max(overlap_ratio, similarity), 4)
    return passed, score
