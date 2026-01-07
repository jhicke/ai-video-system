# services/broll/utils.py

import hashlib


def deterministic_seed(run_id: str, idx: int, prompt_text: str) -> int:
    key = f"{run_id}|{idx}|{prompt_text}".encode("utf-8")
    h = hashlib.sha256(key).hexdigest()
    return int(h[:8], 16)
