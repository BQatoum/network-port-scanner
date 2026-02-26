# Network-Port Scanner

TCP-based network scanner that scans a given CIDR subnet, identifies live hosts, performs port scanning on common ports, and generates structured JSON and Markdown reports.

---

## Overview

This project implements a CIDR subnet scanner using Python standard libraries only.

The scanner:

- Accepts a CIDR subnet as input (e.g., 192.168.1.0/24)

- Identifies live hosts within the subnet

- Performs TCP Connect port scanning on predefined common ports

- Generates structured JSON output

- Generates a Markdown report

- Uses multithreading to improve scanning performance

---

## Features

- CIDR subnet parsing using ipaddress

- TCP Connect scanning using socket

- Multithreaded scanning using ThreadPoolExecutor

- Host discovery based on TCP responses

- JSON output generation

- Markdown report generation

- No external dependencies (Python standard library only)

---

## Technologies Used

- Python 3

- socket

- ipaddress

- concurrent.futures

- argparse

- json

- datetime

---

## How It Works

### Host Discovery Logic

For each IP address in the given CIDR subnet:

- A TCP connection attempt is made to predefined common ports.

- If a connection succeeds → Port is Open

- If ConnectionRefusedError occurs → Port is Closed (RST received).

- If a timeout occurs → Port is considered Filtered.

A host is considered UP if at least one port responds (open or closed).

### Multithreading

The scanner uses:
```python
ThreadPoolExecutor(max_workers=50)
```
Each IP address is scanned in a separate thread to improve performance when scanning larger subnets.

---

## Installation

Make the installation script executable:

```bash
chmod +x install.sh
```
Run the installation script:

```bash
./install.sh
```
The script verifies that Python 3 is installed.

No need to download external dependencies.

---

## Usage

Run the scanner using:

```bash
python3 scanner.py <CIDR_SUBNET>
```
Example:
```bash
python3 scanner.py 192.168.1.0/24
```
---

## Output Files

After execution, the scanner generates the following files:

1. scan_results.json

Machine-readable structured output containing live hosts and their open/closed ports.

Example:
```json 
[
    {
        "ip": "192.168.1.10",
        "status": "up",
        "open_ports": [80, 443],
        "closed_ports": [22]
    }
]
```

---

2. Scan_Report.md

- Human-readable Markdown report including:

- Scan date
- Live hosts
- Open ports
- Closed ports


Example:
```
Network Subnet Scan Report
Scan date: 2026-02-25 15:20:41.477230

Host: 192.168.1.10
Status: UP
Open Ports: []
Closed Ports: [22, 80, 445, 3389, 139, 21, 25, 443]
```
  

---

## Project Structure
```
cidr-network-scanner/
│
├── README.md
├── install.sh
├── scanner.py
```



