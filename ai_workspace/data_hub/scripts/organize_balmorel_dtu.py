"""Move the public DTU Data files (collection doi:10.11583/DTU.c.7964141) out of Shubham's working copy
into ~/local_data/Balmorel_DTU/raw/<item>/<public name>, and replace every copy in the working copy with
a symlink to that file. Only files whose MD5 equals the online MD5 are touched.

Usage: python3 organize_balmorel_dtu.py <remote_md5.txt> [--run]
remote_md5.txt lines: "<md5> <article id> <size> <name>" (figshare API, computed_md5).
Without --run it prints the plan only.
"""
import hashlib
import os
import sys
from pathlib import Path

SRC: Path = Path.home() / "local_data" / "Shubham_minimum_working_copy_p3"
DST: Path = Path.home() / "local_data" / "Balmorel_DTU" / "raw"
ITEM: dict[str, str] = {
    "32881565": "electricity_demand", "32881376": "hydro_inflow", "32881508": "heat_demand",
    "32881544": "heat_pump_COP", "29618153": "wind_onshore", "29617955": "wind_offshore",
    "29617220": "solar_PV",
}
OFFSHORE_BOTTOM_FIXED_SIZE: int = 105306319  # the 2 online SP316/SP370 files of this size are bottom-fixed


def md5(p: Path) -> str:
    """MD5 hex digest of a file."""
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    run: bool = "--run" in sys.argv
    remote: dict[str, list[tuple[str, int, str]]] = {}
    for line in Path(sys.argv[1]).read_text().splitlines():
        m, art, size, name = line.split(maxsplit=3)
        if name != "readme.txt" and not name.endswith(".png"):
            remote.setdefault(m, []).append((art, int(size), name))
    plan: dict[Path, list[Path]] = {}
    for p in sorted(SRC.rglob("*.csv")):
        if p.is_symlink() or "/balmorel/" in str(p):
            continue
        m: str = md5(p)
        if m not in remote:
            continue
        cands = remote[m]
        hit = [c for c in cands if c[2] == p.name] or cands  # same name first; P.csv -> the only online name
        art, size, name = hit[0]
        sub: str = "Future_bottom_fixed/" if art == "29617955" and size == OFFSHORE_BOTTOM_FIXED_SIZE else ""
        target: Path = DST / ITEM[art] / f"{sub}{name}"
        plan.setdefault(target, []).append(p)
    n_links: int = 0
    for target, copies in plan.items():
        print(f"{target.relative_to(DST)}  <=  {len(copies)} copy/copies")
        for c in copies:
            print("      ", c.relative_to(SRC))
        if not run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            os.rename(copies[0], target)  # same filesystem: a rename, no data copied
        tm: str = md5(target)
        for c in copies:
            if c.exists() and not c.is_symlink():
                assert md5(c) == tm, f"checksum differs: {c}"
                c.unlink()
            if not c.is_symlink():
                c.symlink_to(os.path.relpath(target, c.parent))  # relative: works at every local_data root
                n_links += 1
    print(f"{len(plan)} public files, {sum(len(v) for v in plan.values())} copies, {n_links} links made")


if __name__ == "__main__":
    main()
