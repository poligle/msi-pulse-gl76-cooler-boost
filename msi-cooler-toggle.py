#!/usr/bin/env python3
"""
Toggle MSI Cooler Boost by changing bit 7 at EC offset 0x98.

Tested only on:
- MSI Pulse GL76 11UEK
- Board: MS-17L1
- EC firmware: 17L1EMS1.102

WARNING:
This writes directly to the Embedded Controller.
Do not use on other models/firmwares without verifying the EC offset first.
"""

from __future__ import annotations

import os
import subprocess
import sys


EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 0x98
COOLER_BOOST_MASK = 0x80


def notify(message: str) -> None:
    """Best-effort desktop notification."""
    try:
        subprocess.run(
            ["notify-send", "MSI Cooler Boost", message],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def main() -> int:
    if not os.path.exists(EC_PATH):
        message = (
            f"EC path not found: {EC_PATH}\n"
            "Try: sudo modprobe ec_sys write_support=1"
        )
        print(message, file=sys.stderr)
        notify("EC path not found")
        return 1

    try:
        with open(EC_PATH, "r+b", buffering=0) as ec:
            ec.seek(OFFSET)
            old_raw = ec.read(1)
            if len(old_raw) != 1:
                print("Could not read EC byte", file=sys.stderr)
                notify("Could not read EC byte")
                return 1

            old = old_raw[0]

            if old & COOLER_BOOST_MASK:
                new = old & ~COOLER_BOOST_MASK
                state = "OFF"
            else:
                new = old | COOLER_BOOST_MASK
                state = "ON"

            ec.seek(OFFSET)
            ec.write(bytes([new]))

    except PermissionError:
        print(
            "Permission denied. Run as root or configure sudoers.",
            file=sys.stderr,
        )
        notify("Permission denied")
        return 2
    except OSError as exc:
        print(f"EC write failed: {exc}", file=sys.stderr)
        notify("EC write failed")
        return 3

    print(f"Cooler Boost {state}: EC[0x{OFFSET:02x}] {old:02x} -> {new:02x}")
    notify(f"Cooler Boost {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
