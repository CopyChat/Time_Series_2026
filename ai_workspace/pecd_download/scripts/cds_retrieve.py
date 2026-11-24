"""Minimal CDS (new API) client with the standard library only: submit, poll, report size, download.

Usage: python3 cds_retrieve.py <request.json> <out_file> [--size-only]
request.json = {"dataset": "sis-energy-pecd", "request": {...}}
Key: ~/.cdsapirc (lines "url: ..." and "key: ...").
"""
import json
import sys
import time
import urllib.request
from pathlib import Path


def read_rc() -> tuple[str, str]:
    """Return (url, key) from ~/.cdsapirc."""
    rc: dict[str, str] = {}
    for line in (Path.home() / ".cdsapirc").read_text().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            rc[k.strip()] = v.strip()
    return rc["url"].rstrip("/"), rc["key"]


def call(url: str, key: str, data: dict | None = None) -> dict:
    """GET (data None) or POST JSON; return the decoded JSON reply."""
    body: bytes | None = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={"PRIVATE-TOKEN": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:800]}")


def main() -> None:
    spec: dict = json.loads(Path(sys.argv[1]).read_text())
    out: Path = Path(sys.argv[2])
    size_only: bool = "--size-only" in sys.argv
    base, key = read_rc()
    proc: str = f"{base}/retrieve/v1/processes/{spec['dataset']}"
    job: dict = call(f"{proc}/execution", key, {"inputs": spec["request"]})
    jid: str = job["jobID"]
    print("job", jid, job.get("status"), flush=True)
    while True:
        st: dict = call(f"{base}/retrieve/v1/jobs/{jid}", key)
        if st["status"] in ("successful", "failed", "rejected", "dismissed"):
            break
        time.sleep(20)
    if st["status"] != "successful":
        print(json.dumps(call(f"{base}/retrieve/v1/jobs/{jid}/results", key))[:1500])
        sys.exit(f"job {st['status']}")
    asset: dict = call(f"{base}/retrieve/v1/jobs/{jid}/results", key)["asset"]["value"]
    size: int = int(asset.get("file:size", -1))
    print(f"size_bytes {size}  ({size / 1e6:.1f} MB)  {asset['href']}", flush=True)
    if not size_only:
        out.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(asset["href"], out)
        print("saved", out, out.stat().st_size)


if __name__ == "__main__":
    main()
