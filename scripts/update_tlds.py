#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SOURCE = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

PUBLIC_DIR = Path("public")

TXT_FILE = PUBLIC_DIR / "tlds.txt"
JSON_FILE = PUBLIC_DIR / "tlds.json"
MIN_JSON_FILE = PUBLIC_DIR / "tlds.min.json"
CHECKSUM_FILE = PUBLIC_DIR / "tlds.sha256"

def fetch_tlds() -> list[str]:
    with urllib.request.urlopen(SOURCE) as response:
        text = response.read().decode("utf-8")

    return sorted(
        line.strip().lower()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#")
    )


def build_checksum(tlds: list[str]) -> str:
    body = "\n".join(tlds) + "\n"
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def read_existing_payload() -> dict[str, Any] | None:
    if not JSON_FILE.exists():
        return None

    try:
        return json.loads(JSON_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def build_payload(tlds: list[str]) -> dict[str, Any]:
    checksum = build_checksum(tlds)
    existing = read_existing_payload()

    if existing and existing.get("checksum_sha256") == checksum:
        updated_at = existing.get("updated_at")
    else:
        updated_at = datetime.now(UTC).isoformat()

    return {
        "source": SOURCE,
        "updated_at": updated_at,
        "count": len(tlds),
        "checksum_sha256": checksum,
        "tlds": tlds,
    }


def write_outputs(payload: dict[str, Any]) -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    tlds = payload["tlds"]
    checksum = payload["checksum_sha256"]

    TXT_FILE.write_text(
        "\n".join(tlds) + "\n",
        encoding="utf-8",
    )

    JSON_FILE.write_text(
        json.dumps(payload, indent=4) + "\n",
        encoding="utf-8",
    )

    MIN_JSON_FILE.write_text(
        json.dumps(payload, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    CHECKSUM_FILE.write_text(
        f"{checksum}\n",
        encoding="utf-8",
    )

def main() -> None:
    tlds = fetch_tlds()
    payload = build_payload(tlds)

    write_outputs(payload)

    print(f"Wrote {payload['count']} TLDs")
    print(f"Checksum: {payload['checksum_sha256']}")


if __name__ == "__main__":
    main()
