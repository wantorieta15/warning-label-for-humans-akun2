#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh -- entry generator.

Writes exactly one line -- a warning label that should be printed on
every human -- to <out_dir>/entry.txt. Pure standard library only.

Validation enforced before any byte is written:
  * exactly one line, 1-160 characters, UTF-8
  * printable characters only (no control characters, no newline)
  * no leading or trailing whitespace, not whitespace-only
  * SHA-256 of the exact output bytes must match the pinned digest
  * file written directly (open + chmod 0644), never via a temp file
"""

import hashlib
import os
import sys

ENTRY = "CAUTION: Human overheats when wrong. Keep away from facts, mirrors, and anyone who remembers what they said."

EXPECTED_SHA256 = "b2d44bdcc0513c027ef24a93fdbf50543a3608577e4bc7e090b9259fa1107fb6"
EXPECTED_BYTES = 108
MAX_CHARS = 160


def build_entry() -> str:
    """Return the entry text after strict single-line validation."""
    text = ENTRY
    if not isinstance(text, str):
        raise TypeError("entry must be str, got %s" % type(text).__name__)
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.isprintable():
        raise ValueError("entry must contain printable characters only")
    return text


def entry_bytes(text: str) -> bytes:
    """Encode the entry as UTF-8 bytes with no trailing newline."""
    data = text.encode("utf-8")
    if data.endswith(b"\n"):
        raise ValueError("entry bytes must not end with a newline")
    return data


def verify_digest(data: bytes) -> str:
    """Check byte length and SHA-256 against the pinned values."""
    if len(data) != EXPECTED_BYTES:
        raise ValueError(
            "entry must be %d bytes, got %d" % (EXPECTED_BYTES, len(data))
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("entry digest mismatch: %s" % digest)
    return digest


def write_entry(data: bytes, out_dir: str) -> str:
    """Write bytes directly to <out_dir>/entry.txt with mode 0644."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    os.chmod(path, 0o644)
    return path


def main() -> int:
    text = build_entry()
    data = entry_bytes(text)
    digest = verify_digest(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = write_entry(data, out_dir)
    print("wrote %s (%d bytes, sha256 %s)" % (path, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
