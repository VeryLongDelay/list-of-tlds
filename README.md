# TLD List

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Github Pages](https://img.shields.io/badge/github%20pages-121013?style=flat&logo=github&logoColor=white)
![Update TLDs](https://github.com/verylongdelay/tldlist/actions/workflows/update-tlds.yml/badge.svg?)

## Source of truth

[IANA Root Zone Database](https://data.iana.org/TLD/tlds-alpha-by-domain.txt)

### `tlds.txt`

Plain newline-separated lowercase TLD list.

Example:

```txt
com
net
org
dev
xn--fiqs8s
```

---

### `tlds.json`

Pretty-formatted JSON metadata + TLD list.

Example:

```json
{
  "source": "https://data.iana.org/TLD/tlds-alpha-by-domain.txt",
  "updated_at": "2026-05-10T21:00:00+00:00",
  "count": 1438,
  "checksum_sha256": "...",
  "tlds": ["com", "net", "org"]
}
```

---

### `tlds.min.json`

Minified JSON version optimized for web delivery.

---

### `tlds.sha256`

SHA256 checksum of the canonical TLD dataset.

The checksum only changes when the actual TLD list changes.

## License

[MIT](license)
