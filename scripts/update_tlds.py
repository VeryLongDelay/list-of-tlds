#!/usr/bin/env python3

from __future__ import annotations

import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

SOURCE = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

DATA_DIR = Path("public")

TXT_FILE = DATA_DIR / "tlds.txt"
JSON_FILE = DATA_DIR / "tlds.json"
MIN_JSON_FILE = DATA_DIR / "tlds.min.json"


def fetch_tlds() -> list[str]:
    with urllib.request.urlopen(SOURCE) as response:
        text = response.read().decode("utf-8")

    return sorted(
        line.strip().lower()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#")
    )


def build_payload(tlds: list[str]) -> dict:
    return {
        "source": SOURCE,
        "updated_at": datetime.now(UTC).isoformat(),
        "count": len(tlds),
        "tlds": tlds,
    }


def write_outputs(payload: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    tlds = payload["tlds"]

    TXT_FILE.write_text(
        "\n".join(tlds) + "\n",
        encoding="utf-8",
    )

    JSON_FILE.write_text(
        json.dumps(payload, indent=4) + "\n",
        encoding="utf-8",
    )

    MIN_JSON_FILE.write_text(
        json.dumps(payload, separators=(",", ":")),
        encoding="utf-8",
    )


def main() -> None:
    tlds = fetch_tlds()

    payload = build_payload(tlds)

    write_outputs(payload)

    print(f"Wrote {payload['count']} TLDs")


if __name__ == "__main__":
    main()
