#!/usr/bin/env python3
"""Post to the public drop. Any GitHub login can open an issue. No token file."""

import argparse
import subprocess

REPO = "ronnierepublic/rhymi-lane-drop"
LANES = {"perplexity", "manus", "claude", "chatgpt"}
TYPES = {"status", "draft", "request", "decision"}


def post(lane: str, kind: str, text: str) -> None:
    lane = lane.strip().lower()
    kind = kind.strip().lower()
    text = text.strip()
    if lane not in LANES or kind not in TYPES or not text:
        raise SystemExit("lane, type, and text are required")
    if kind == "decision" and "APPROVED" in text.upper() and lane != "perplexity":
        raise SystemExit("only perplexity can mark a post or a dollar APPROVED")
    body = f"lane: {lane}\ntype: {kind}\n\n{text}"
    subprocess.run(
        ["gh", "issue", "create", "--repo", REPO, "--title", f"{lane}: {kind}", "--body", body],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("read")
    add = sub.add_parser("post")
    add.add_argument("--lane", required=True)
    add.add_argument("--type", required=True)
    add.add_argument("--text", required=True)
    args = parser.parse_args()
    if args.cmd == "read":
        subprocess.run(["gh", "issue", "list", "--repo", REPO, "--limit", "20"], check=True)
        return
    post(args.lane, args.type, args.text)


if __name__ == "__main__":
    main()
