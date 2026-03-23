#!/usr/bin/env python3
"""
Generic caller for KPLApi methods.
"""

import argparse
import json
import sys

from kpl_api import KPLApi


def main() -> int:
    parser = argparse.ArgumentParser(description="Call a method on KPLApi.")
    parser.add_argument("--method", required=True, help="KPLApi method name")
    parser.add_argument(
        "--kwargs",
        default="{}",
        help="JSON object for keyword arguments, e.g. '{\"stock_id\":\"300827\"}'",
    )
    args = parser.parse_args()

    try:
        kwargs = json.loads(args.kwargs)
        if not isinstance(kwargs, dict):
            raise ValueError("--kwargs must be a JSON object")
    except Exception as exc:
        print(json.dumps({"error": f"invalid kwargs: {exc}"}), file=sys.stderr)
        return 2

    api = KPLApi()

    if not hasattr(api, args.method):
        print(json.dumps({"error": f"unknown method: {args.method}"}), file=sys.stderr)
        return 2

    fn = getattr(api, args.method)
    if not callable(fn):
        print(json.dumps({"error": f"not callable: {args.method}"}), file=sys.stderr)
        return 2

    try:
        result = fn(**kwargs)
    except TypeError as exc:
        print(json.dumps({"error": f"argument error: {exc}"}), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
