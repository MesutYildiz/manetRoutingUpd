# 🌐 MANET Routing Protocol Simulator

**Advanced Python-based simulation framework for Mobile Ad-hoc Network (MANET) routing protocols with OMNeT++ integration**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OMNeT++](https://img.shields.io/badge/OMNeT++-5.6.2-green.svg)](https://omnetpp.org/)
[![INETMANET](https://img.shields.io/badge/INETMANET-3.x-orange.svg)](https://github.com/aarizaq/inetmanet-3.x)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

A comprehensive MANET simulation platform featuring:
- **Dual-Engine Architecture**: OMNeT++/INETMANET integration + Legacy Python discrete-event simulator
- **User-Friendly GUI**: Intuitive Tkinter interface for simulation control
- **Advanced Protocol Support**: AODV, DSR (DYMO), OLSR, and ZRP (Zone Routing Protocol)
- **Fine-Grained Control**: Extensive parameter tuning for protocol optimization
- **Automated Result Analysis**: Smart parsing and metrics extraction from simulation outputs

Perfect for academic research, protocol development, and network performance analysis.

---

## ✨ Key Features

### 🎮 Dual Simulation Modes
- **OMNeT++ Integration**: Industry-standard network simulation with INETMANET-3.x
- **Python Discrete-Event Engine**: Lightweight alternative for rapid prototyping (legacy support)

### 🖥️ GUI & Usability
- **Intuitive Interface**: Clean Tkinter-based control panel
- **Real-Time Monitoring**: Live simulation logs and progress tracking
- **One-Click Operations**: Automated configuration, execution, and result parsing

### 🔬 Protocol Support
- **AODV** (Ad-hoc On-Demand Distance Vector)
- **DSR** (Dynamic Source Routing via DYMO)
- **OLSR** (Optimized Link State Routing)
- **ZRP** (Zone Routing Protocol) - *Python engine only*

### ⚙️ Advanced Configuration
- **AODV Fine-Tuning**: Route timeout, Hello interval, Hello loss parameters
- **Network Parameters**: Node count, simulation time, mobility models
- **Traffic Control**: Packet rate, payload size, source/destination selection

### 📊 Metrics & Analysis
- **PDR** (Packet Delivery Ratio)
- **End-to-End Delay** (Average, Min, Max)
- **Hop Count** (Route length statistics)
- **Throughput** & Network overhead
- **Automatic .sca/.vec file parsing**

---

## 📂 Project Structure

```
Vfman/
├── main.py                      # Application entry point
├── gui.py                       # Tkinter GUI interface (291 lines)
├── omnet_manager.py             # OMNeT++ integration & result parser (624 lines)
├── models.py                    # Data models & structures (222 lines)
├── birlestir.py                 # Project file consolidation utility
│
├── legacy_python_engine/        # Standalone Python simulator (legacy)
│   ├── discrete_simulator.py   # Discrete-event simulation engine
│   ├── node.py                  # Node implementation
│   ├── mac_layer.py             # MAC layer simulation
│   ├── mobility.py              # Mobility models (Random Waypoint, etc.)
│   ├── metrics.py               # Performance metrics collection
│   ├── traffic_generator.py    # Traffic generation utilities
│   └── tests/                   # Legacy test suite
│
├── requirements.txt             # Python dependencies (tkinter only)
├── LICENSE                      # MIT License
├── README.md                    # This file
│
└── Documentation/
    ├── AODV_INCE_AYARLAR.md         # AODV fine-tuning guide (Turkish)
    ├── GITHUB_YUKLEME_KILAVUZU.md   # GitHub upload guide (Turkish)
    ├── GITHUB_HIZLI_BASLANGIC.md    # Quick start guide (Turkish)
    ├── GELISTIRMELER_OZET.md        # Development summary (Turkish)
    ├── HIZLI_OZET.md                # Quick overview (Turkish)
    └── OMNET_TROUBLESHOOTING.md     # OMNeT++ troubleshooting
```

**Total**: ~1,200+ lines of core code + extensive documentation

---

## 🚀 Quick Start

### Prerequisites

| Component | Version | Required For | Link |
|-----------|---------|-------------|------|
| **Python** | 3.8+ | All features | [python.org](https://www.python.org/) |
| **OMNeT++** | 5.6.2+ | OMNeT++ mode | [omnetpp.org](https://omnetpp.org/download/) |
| **INETMANET-3.x** | 3.0+ | OMNeT++ mode | [GitHub](https://github.com/aarizaq/inetmanet-3.x) |

> **Note**: The legacy Python simulator works without OMNeT++

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Vfman.git
cd Vfman

# 2. No external Python dependencies needed (uses tkinter from standard library)
# If tkinter is missing:
# - Ubuntu/Debian: sudo apt-get install python3-tk
# - macOS: Included with Python from python.org
# - Windows: Included with Python installer

# 3. (Optional) Install OMNeT++ and INETMANET for full functionality
```

### Configuration for OMNeT++ Mode

Edit paths in `omnet_manager.py`:

```python
# Windows example
self.omnet_bin = r"C:\omnetpp-5.6.2\bin\opp_run.exe"
self.working_dir = r"C:\inetmanet-3.0"

# Linux/macOS example  
self.omnet_bin = "/opt/omnetpp-5.6.2/bin/opp_run"
self.working_dir = "/home/user/inetmanet-3.0"
```

**Important**: Ensure INETMANET is compiled and `libINET.dll` (Windows) or `libINET.so` (Linux) exists.

---

## 💻 Usage

### 1. Launch GUI Application

```bash
python main.py
```

### 2. Configure Simulation

The GUI provides intuitive controls for all parameters:

**Basic Parameters:**
- **Protocol**: AODV, DSR (DYMO), or OLSR
- **Node Count**: 10-100 nodes (recommended: 20-30)
- **Simulation Time**: Duration in seconds (e.g., 100s)
- **Mobility Model**: RandomWaypointMobility (default)

**AODV-Specific Tuning:**
- **Route Timeout**: 1.0-10.0 seconds (default: 3.0s)
- **Hello Interval**: 0.5-2.0 seconds (default: 1.0s)
- **Hello Loss**: 1-5 packets (default: 2)

### 3. Run & Monitor

1. Click **"Start Simulation"**
2. Watch real-time logs in the GUI
3. Wait for completion (or stop early with interrupt)
4. Results auto-parse and display

### 4. Programmatic API (Advanced)

```python
from omnet_manager import OmnetManager

# Initialize
manager = OmnetManager()

# Configure
manager.create_config(
    protocol="AODV",
    num_nodes=25,
    sim_time_limit="150s",
    aodv_timeout=2.5,
    aodv_hello_interval=0.8,
    aodv_hello_loss=3
)

# Execute
if manager.run_simulation():
    results = manager.parse_results()
    
    print(f"📊 Results:")
    print(f"  PDR: {results['pdr']:.2f}%")
    print(f"  Packets Sent: {results['sent']}")
    print(f"  Packets Received: {results['received']}")
    print(f"  Avg Delay: {results['delay_avg']:.2f} ms")
    print(f"  Avg Hops: {results['hop_avg']:.2f}")
```

### 5. Batch Simulations (Research)

```python
from omnet_manager import OmnetManager
import pandas as pd

# Define parameter sweep
hello_intervals = [0.5, 1.0, 1.5, 2.0]
route_timeouts = [1.5, 3.0, 5.0]

results_data = []
manager = OmnetManager()

for timeout in route_timeouts:
    for interval in hello_intervals:
        print(f"Testing: timeout={timeout}s, interval={interval}s")
        
        manager.create_config(
            protocol="AODV",
            num_nodes=20,
            sim_time_limit="100s",
            aodv_timeout=timeout,
            aodv_hello_interval=interval
        )
        
        if manager.run_simulation():
            res = manager.parse_results()
            results_data.append({
                'timeout': timeout,
                'interval': interval,
                'pdr': res['pdr'],
                'delay': res['delay_avg'],
                'hops': res['hop_avg']
            })

# Export to CSV
df = pd.DataFrame(results_data)
df.to_csv('aodv_parameter_sweep.csv', index=False)
print("✅ Results saved to aodv_parameter_sweep.csv")
```

---

## 🔧 Routing Protocols

### OMNeT++ Mode

| Protocol | Full Name | Network Configuration | Host Type | Status |
|----------|-----------|----------------------|-----------|--------|
| **AODV** | Ad-hoc On-Demand Distance Vector | `inet.examples.aodv.AODVNetwork` | `AODVRouter` | ✅ **Fully Featured** |
| **DSR** | Dynamic Source Routing (via DYMO) | `inet.examples.manetrouting.dymo.DYMONetwork` | `DYMORouter` | ✅ Working |
| **OLSR** | Optimized Link State Routing | `inet.examples.adhoc.ieee80211.Net80211` | `AdhocHost` | ✅ Working |

### Python Simulator Mode (Legacy)

| Protocol | Implementation | Status |
|----------|---------------|--------|
| **AODV** | Full implementation with route discovery | ✅ Complete |
| **ZRP** | Zone Routing Protocol (hybrid) | ✅ Complete |

> **Note**: The Python simulator uses a discrete-event engine with simplified MAC layer

---

## 📊 Performance Metrics

The simulator automatically extracts and calculates the following metrics:

### Core Metrics

| Metric | Description | Unit | Source |
|--------|-------------|------|--------|
| **PDR** | Packet Delivery Ratio | % | Application layer sent/received |
| **Throughput** | Successfully delivered data rate | packets/s | Received count / time |
| **End-to-End Delay** | Average packet travel time | milliseconds | Per-packet timestamps |
| **Hop Count** | Average route length | hops | Network layer statistics |

### Additional Statistics (OMNeT++)

- **Min/Max Delay**: Best and worst case latency
- **Routing Overhead**: Control packet ratio
- **Route Discovery Time**: RREQ → RREP latency
- **Link Break Events**: Network topology changes

### Result Format

```python
{
    'pdr': 87.5,              # Packet Delivery Ratio (%)
    'sent': 400,              # Total packets sent
    'received': 350,          # Total packets received
    'delay_avg': 45.2,        # Average delay (ms)
    'delay_min': 12.3,        # Minimum delay (ms)
    'delay_max': 234.5,       # Maximum delay (ms)
    'hop_avg': 3.4,           # Average hop count
    'hop_min': 1,             # Minimum hops
    'hop_max': 7              # Maximum hops
}
```

---

## 🎯 AODV Fine-Tuning Parameters

AODV protocol has 3 critical parameters for optimization:

### 1. Route Timeout
- **Description**: How long an unused route stays valid before deletion
- **Default**: 3.0s
- **Impact**: 
  - Low → Frequent route discovery → High overhead
  - High → Old routes used → Potential packet loss

### 2. Hello Interval
- **Description**: Frequency of "I'm here" messages to neighbors
- **Default**: 1.0s
- **Impact**:
  - Low → Fast link break detection → High traffic
  - High → Low traffic → Slow link break detection

### 3. Hello Loss
- **Description**: Number of missing Hello messages before neighbor is considered dead
- **Default**: 2
- **Impact**:
  - Low → Fast reaction → Risk of false positives
  - High → Stable → Slow reaction

### Example Scenarios

**Fast Response** (High mobility):
```python
timeout=1.5s, hello_interval=0.5s
```

**Energy Saving** (IoT devices):
```python
timeout=5.0s, hello_interval=2.0s
```

---

## 🎓 Academic Research & Education

This simulator is designed for academic research, thesis work, and network protocol education.

### Ideal for Research Questions Like:

#### 1. **Parameter Optimization Studies**
- *"How do AODV Hello intervals affect PDR in high-mobility scenarios?"*
- *"What is the optimal route timeout for energy-constrained MANETs?"*
- *"Impact of node density on routing overhead"*

#### 2. **Protocol Performance Comparison**
- *"AODV vs OLSR: Scalability analysis"*
- *"Reactive vs Proactive routing in mobile networks"*
- *"DSR performance under varying traffic loads"*

#### 3. **Network Condition Analysis**
- *"Effect of node mobility speed on route stability"*
- *"PDR degradation under increasing network size"*
- *"Link break frequency vs routing protocol efficiency"*

### Example Research Workflow

```python
"""
Research Question: "What is the optimal AODV Hello Interval 
for maximizing PDR while minimizing routing overhead?"
"""

from omnet_manager import OmnetManager
import matplotlib.pyplot as plt

# Test parameters
hello_intervals = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
node_counts = [20, 30, 40]

results = {nodes: {'intervals': [], 'pdr': [], 'overhead': []} 
           for nodes in node_counts}

manager = OmnetManager()

for nodes in node_counts:
    for interval in hello_intervals:
        print(f"Testing: {nodes} nodes, interval={interval}s")
        
        manager.create_config(
            protocol="AODV",
            num_nodes=nodes,
            sim_time_limit="200s",
            aodv_hello_interval=interval
        )
        
        if manager.run_simulation():
            res = manager.parse_results()
            results[nodes]['intervals'].append(interval)
            results[nodes]['pdr'].append(res['pdr'])
            # Parse overhead from .sca file if needed

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
for nodes in node_counts:
    ax.plot(results[nodes]['intervals'], 
            results[nodes]['pdr'], 
            marker='o', 
            label=f'{nodes} nodes')

ax.set_xlabel('AODV Hello Interval (s)')
ax.set_ylabel('Packet Delivery Ratio (%)')
ax.set_title('Impact of Hello Interval on PDR')
ax.legend()
ax.grid(True)
plt.savefig('aodv_hello_interval_study.png', dpi=300)
print("✅ Research results saved!")
```

### Suggested Thesis Topics

1. **Adaptive Hello Interval Mechanism for AODV**
   - Dynamically adjust based on node mobility

2. **Energy-Efficient MANET Routing**
   - Compare protocols under battery constraints

3. **QoS-Aware Routing in MANETs**
   - Delay-sensitive vs throughput-optimized routing

4. **Cross-Layer Optimization**
   - MAC-Network layer interaction analysis

### Citation

If you use this simulator in your research, please cite:

```bibtex
@software{vfman_manet_simulator,
  title = {MANET Routing Protocol Simulator},
  author = {[Your Name]},
  year = {2024},
  url = {https://github.com/YOUR_USERNAME/Vfman},
  note = {Python-based MANET simulation framework with OMNeT++ integration}
}
```

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>1. "libINET.dll not found" (Windows) or "libINET.so not found" (Linux)</b></summary>

**Cause**: INETMANET library not compiled or path incorrect

**Solutions**:
```bash
# Navigate to INETMANET directory
cd C:\path\to\inetmanet-3.0  # Windows
cd /path/to/inetmanet-3.0     # Linux

# Build INETMANET
make clean
make MODE=release -j4

# Verify library exists
dir src\libINET.dll           # Windows
ls src/libINET.so             # Linux
```
</details>

<details>
<summary><b>2. "No module type named 'RandomWaypointMobility'"</b></summary>

**Cause**: INET 4.x vs INET 3.x mobility model name differences

**Solution**: Already fixed in code - uses `RandomWPMobility` for INET 3.x
</details>

<details>
<summary><b>3. PDR exceeds 100% or shows wrong values</b></summary>

**Cause**: Counting all packets instead of application-layer only

**Solution**: Parser correctly filters UDP application layer traffic (fixed in v1.0)
</details>

<details>
<summary><b>4. GUI doesn't start - tkinter missing</b></summary>

**Solutions by OS**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# macOS (install Python from python.org, not Homebrew)
# Windows (tkinter included by default)
```
</details>

<details>
<summary><b>5. Simulation runs but no results appear</b></summary>

**Checklist**:
- Check `results/` folder exists in INETMANET directory
- Verify `.sca` files are generated after simulation
- Look for errors in simulation log window
- Ensure simulation runs for sufficient time (>50s recommended)
</details>

For more detailed troubleshooting, see [`OMNET_TROUBLESHOOTING.md`](OMNET_TROUBLESHOOTING.md)

---

## 🛠️ Technical Architecture

### System Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| **OS** | Windows 10 / Ubuntu 18.04 / macOS 10.14 | Windows 11 / Ubuntu 22.04 / macOS 13+ | Cross-platform |
| **Python** | 3.8 | 3.10+ | Standard library only |
| **RAM** | 4 GB | 8 GB+ | For large simulations (50+ nodes) |
| **OMNeT++** | 5.6.2 | 5.7.x | Optional for Python mode |
| **INETMANET** | 3.0 | 3.8 | Requires compilation |

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│           GUI Layer (gui.py)                │
│  - Tkinter Interface                        │
│  - Parameter Input Forms                    │
│  - Real-time Log Display                    │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│      Application Logic (main.py)            │
│  - Event Handling                           │
│  - Simulation Orchestration                 │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴────────┐
      ▼                ▼
┌──────────────┐  ┌──────────────────────────┐
│ OMNeT++ Mode │  │  Python Simulator Mode   │
│              │  │  (legacy_python_engine)  │
└──────┬───────┘  └──────┬───────────────────┘
       │                 │
       ▼                 ▼
┌────────────────┐  ┌─────────────────────┐
│omnet_manager.py│  │discrete_simulator.py│
│- Config Gen    │  │- Event Queue        │
│- Execution     │  │- Node Management    │
│- Result Parse  │  │- MAC Layer          │
└────────────────┘  └─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│    Data Models (models.py) │
│  - Event, Packet, Node     │
│  - Metrics, Configuration  │
└────────────────────────────┘
```

### Key Components

| File | Lines | Purpose |
|------|-------|---------|
| **`main.py`** | 40 | Application entry point, GUI initialization |
| **`gui.py`** | 291 | Tkinter interface, user controls, log display |
| **`omnet_manager.py`** | 624 | OMNeT++ integration, `.ini` generation, result parsing |
| **`models.py`** | 222 | Data classes (Event, Packet, Node, Metrics, etc.) |
| **`birlestir.py`** | 29 | Utility to consolidate project files for documentation |

### Legacy Python Engine

| File | Purpose |
|------|---------|
| **`discrete_simulator.py`** | Core discrete-event simulation loop |
| **`node.py`** | Node implementation with routing protocols |
| **`mac_layer.py`** | Simplified MAC layer (CSMA/CA) |
| **`mobility.py`** | Mobility models (Random Waypoint, etc.) |
| **`metrics.py`** | Metrics collection and statistics |
| **`traffic_generator.py`** | Traffic pattern generation |

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

## 🤝 Contributing

Contributions are highly welcome! Whether it's bug fixes, new features, or documentation improvements.

### How to Contribute

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/Vfman.git`
3. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
4. **Make** your changes and commit: `git commit -m 'Add AmazingFeature'`
5. **Push** to your branch: `git push origin feature/AmazingFeature`
6. **Open** a Pull Request with detailed description

### Development Roadmap

#### High Priority
- [ ] **DSR/OLSR Parameter Tuning**: Fine-grained control like AODV
- [ ] **Batch Mode GUI**: Run multiple simulations with parameter sweeps
- [ ] **CSV/Excel Export**: Automated result export for analysis
- [ ] **Graph Visualization**: Real-time matplotlib plots (PDR, delay, hops)

#### Medium Priority
- [ ] **Mobility Model Selection**: GUI dropdown for different models
- [ ] **Traffic Pattern Control**: CBR, Poisson, burst traffic
- [ ] **Configuration Profiles**: Save/load simulation presets
- [ ] **Result Comparison**: Side-by-side protocol comparison
- [ ] **Animation Playback**: Visualize node movement and packet flow

#### Low Priority (Nice to Have)
- [ ] **Web Interface**: Browser-based GUI (Flask/Django)
- [ ] **Distributed Simulation**: Multi-core parallel execution
- [ ] **Machine Learning Integration**: Parameter optimization with ML
- [ ] **3D Visualization**: Network topology in 3D space

### Coding Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions/classes
- Include comments for complex logic
- Write unit tests for new features (use `pytest`)
- Update README when adding features

### Testing Your Changes

```bash
# Run the application
python main.py

# Test legacy Python engine
cd legacy_python_engine
python discrete_simulator.py

# Run unit tests (if available)
pytest tests/
```

---

## 📚 Documentation & Resources

### Project Documentation

- **[Quick Start Guide](GITHUB_HIZLI_BASLANGIC.md)** - Turkish quick start
- **[Upload Guide](GITHUB_YUKLEME_KILAVUZU.md)** - GitHub upload instructions (Turkish)
- **[AODV Fine-Tuning](AODV_INCE_AYARLAR.md)** - Detailed AODV parameter guide (Turkish)
- **[Troubleshooting](OMNET_TROUBLESHOOTING.md)** - OMNeT++ common issues and fixes
- **[Development Summary](GELISTIRMELER_OZET.md)** - Project development notes (Turkish)

### External Resources

| Resource | Description | Link |
|----------|-------------|------|
| **OMNeT++ Manual** | Complete simulation framework documentation | [omnetpp.org/doc](https://omnetpp.org/documentation/) |
| **INETMANET Project** | INET framework for mobile networks | [GitHub](https://github.com/aarizaq/inetmanet-3.x) |
| **AODV RFC 3561** | Official AODV protocol specification | [IETF](https://www.ietf.org/rfc/rfc3561.txt) |
| **DSR RFC 4728** | Dynamic Source Routing specification | [IETF](https://www.ietf.org/rfc/rfc4728.txt) |
| **OLSR RFC 3626** | Optimized Link State Routing spec | [IETF](https://www.ietf.org/rfc/rfc3626.txt) |
| **Python Tkinter** | GUI framework documentation | [docs.python.org](https://docs.python.org/3/library/tkinter.html) |

### Related Projects

- [NS-3 Network Simulator](https://www.nsnam.org/) - Alternative C++ network simulator
- [Cooja](https://github.com/contiki-ng/cooja) - Contiki network simulator
- [MiXiM](https://omnetpp.org/download-items/MiXiM.html) - OMNeT++ mobile network framework

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

```
MIT License - Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

## 🌟 Support This Project

If this simulator helped your research or project:

- ⭐ **Star** this repository
- 🐛 **Report** bugs and issues
- 💡 **Suggest** new features
- 🔀 **Contribute** code improvements
- 📢 **Share** with colleagues and students
- 📄 **Cite** in your research papers

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Vfman/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Vfman/discussions)
- **Email**: [your.email@example.com](mailto:your.email@example.com)

---

## 🏆 Acknowledgments

- **OMNeT++** team for the excellent simulation framework
- **INETMANET-3.x** developers for mobile network extensions
- **Python** community for amazing tools and libraries
- All contributors and users of this project

---

<div align="center">

**Made with ❤️ for MANET Research Community**

**Version**: 1.0.0 | **Last Update**: December 2024

[⬆ Back to Top](#-manet-routing-protocol-simulator)

</div>
