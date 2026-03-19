# NetValidate — Network Infrastructure Test Suite Framework

A pytest-based automated testing framework that validates core enterprise network 
services including DNS, HTTP, iSCSI, and Active Directory using mock-based simulation.

## Overview

This test suite was built to validate a virtualized enterprise network infrastructure 
originally deployed across 15 virtual machines using VMware vSphere. Since the 
infrastructure is offline, Python mocks are used to simulate live service behaviour — 
mirroring industry-standard QA practices used when physical systems are unavailable.

## Network Topology

The original infrastructure was built on the following architecture:

- **Domain:** chairmen.lab
- **Red Network:** 172.30.67.1/25 — core services (AD, DNS, HTTP)
- **Green Network:** 172.30.67.128/26 — iSCSI storage traffic
- **Black Network:** 172.30.67.192/26 — HTTP management traffic
- **Services:** Active Directory, DNS, HTTP (IIS), iSCSI, DFS Replication, WAC

## Test Coverage

| Module | Tests | What it validates |
|---|---|---|
| test_ad.py | 7 | User authentication, DC resolution, permissions, replication |
| test_dns.py | 7 | Domain resolution, conditional forwarding, recursive lookup |
| test_http.py | 5 | Server availability, SSL, correct subnet placement |
| test_iscsi.py | 6 | Target/initiator connectivity, network isolation, storage |

## Real Bugs Caught

These tests were built around actual defects found during the original deployment:

- **DNS root hints misconfiguration** — devices lost internet access until root hints were resolved
- **iSCSI subnet mismatch** — target and initiator were accidentally placed on the blue network instead of the green network
- **HTTP network misconfiguration** — HTTP server was deployed on the wrong subnet

## Getting Started
```bash
pip install pytest
python -m pytest -v
```

## Results
```
25 passed in 0.11s
```

## Tech Stack

- Python 3.10
- pytest
- unittest.mock
- VMware vSphere (original infrastructure)
- Windows Server 2022