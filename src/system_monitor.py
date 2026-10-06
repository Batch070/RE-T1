#!/usr/bin/env python3

import argparse
import csv
import os
import time
from datetime import datetime

import psutil


def get_system_info():
    """Collect current system-level information."""

    cpu_percent = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    swap = psutil.swap_memory()

    uptime_seconds = time.time() - psutil.boot_time()

    try:
        load_1, load_5, load_15 = os.getloadavg()
    except (AttributeError, OSError):
        load_1 = load_5 = load_15 = 0.0

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cpu_percent": cpu_percent,
        "cpu_count": psutil.cpu_count(logical=True),
        "memory_total_mb": round(memory.total / (1024 ** 2), 2),
        "memory_used_mb": round(memory.used / (1024 ** 2), 2),
        "memory_available_mb": round(memory.available / (1024 ** 2), 2),
        "memory_percent": memory.percent,
        "swap_total_mb": round(swap.total / (1024 ** 2), 2),
        "swap_used_mb": round(swap.used / (1024 ** 2), 2),
        "swap_percent": swap.percent,
        "uptime_seconds": round(uptime_seconds, 2),
        "load_1min": round(load_1, 2),
        "load_5min": round(load_5, 2),
        "load_15min": round(load_15, 2),
    }


def get_top_processes(top_n=5):
    """Return processes consuming the most CPU."""

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"] or "unknown",
                "cpu_percent": info["cpu_percent"] or 0.0,
                "memory_percent": info["memory_percent"] or 0.0,
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"],
        reverse=True
    )

    return processes[:top_n]


def display_system_info(info):
    """Display system monitoring information."""

    print("\n" + "=" * 60)
    print("          RE-T1 SYSTEM MONITOR")
    print("=" * 60)

    print(f"Timestamp        : {info['timestamp']}")
    print(f"CPU Usage        : {info['cpu_percent']:.2f}%")
    print(f"Logical CPUs     : {info['cpu_count']}")

    print(
        f"RAM Usage        : "
        f"{info['memory_used_mb']:.2f} MB / "
        f"{info['memory_total_mb']:.2f} MB "
        f"({info['memory_percent']:.2f}%)"
    )

    print(
        f"RAM Available    : "
        f"{info['memory_available_mb']:.2f} MB"
    )

    print(
        f"Swap Usage       : "
        f"{info['swap_used_mb']:.2f} MB / "
        f"{info['swap_total_mb']:.2f} MB "
        f"({info['swap_percent']:.2f}%)"
    )

    print(f"Uptime           : {info['uptime_seconds']:.2f} seconds")

    print(
        f"Load Average     : "
        f"{info['load_1min']:.2f}, "
        f"{info['load_5min']:.2f}, "
        f"{info['load_15min']:.2f}"
    )

    print("\nTop CPU Processes")
    print("-" * 60)

    print(
        f"{'PID':<8}"
        f"{'PROCESS':<25}"
        f"{'CPU %':<10}"
        f"{'MEM %':<10}"
    )

    print("-" * 60)

    for process in get_top_processes():
        print(
            f"{process['pid']:<8}"
            f"{process['name'][:24]:<25}"
            f"{process['cpu_percent']:<10.2f}"
            f"{process['memory_percent']:<10.2f}"
        )


def save_csv(info, output_file):
    """Append system information to a CSV file."""

    file_exists = os.path.exists(output_file)

    fieldnames = list(info.keys())

    with open(output_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(info)


def main():
    parser = argparse.ArgumentParser(
        description="RE-T1 Linux System Monitoring Tool"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Monitoring interval in seconds"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of monitoring samples"
    )

    parser.add_argument(
        "--output",
        default="logs/system_monitor.csv",
        help="CSV output file"
    )

    args = parser.parse_args()

    print("Starting RE-T1 System Monitor...")
    print(f"Interval : {args.interval} seconds")
    print(f"Samples  : {args.count}")
    print(f"Log file : {args.output}")

    for sample in range(1, args.count + 1):

        print(f"\nSample {sample}/{args.count}")

        info = get_system_info()

        display_system_info(info)

        save_csv(info, args.output)

        if sample < args.count:
            time.sleep(args.interval)

    print("\nMonitoring completed.")
    print(f"Data saved to: {args.output}")


if __name__ == "__main__":
    main()