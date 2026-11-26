#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh -- entry generator.

Writes exactly one line -- a warning label that should be printed on
every human -- to <out_dir>/entry.txt. Pure standard library only.

Rules enforced before writing:
  * exactly one line, 1-160 characters, UTF-8, not only whitespace
  * no trailing newline in the output file
  * file written directly (open + chmod 0644), never via a temp file
"""

import hashlib
import os

ENTRY = "CAUTION: Human overheats when wrong. Keep away from facts, mirrors, and anyone who remembers what they said."

EXPECTED_SHA256 = "b2d44bdcc0513c027ef24a93fdbf50543a3608577e4bc7e090b9259fa1107fb6"


def main() -> None:
    text = ENTRY
    assert 1 <= len(text) <= 160, "entry must be 1-160 characters"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    assert text.strip(), "entry must not be only whitespace"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert digest == EXPECTED_SHA256, "entry digest mismatch: %s" % digest
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
