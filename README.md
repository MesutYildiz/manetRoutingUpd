# 🌐 MANET Routing Protocol Simulator

**Python-based GUI for OMNeT++/INETMANET MANET simulations**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OMNeT++](https://img.shields.io/badge/OMNeT++-5.6.2-green.svg)](https://omnetpp.org/)
[![INETMANET](https://img.shields.io/badge/INETMANET-3.x-orange.svg)](https://github.com/aarizaq/inetmanet-3.x)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

Easy-to-use GUI application for controlling OMNeT++ MANET simulations. Configure, run, and analyze routing protocols (AODV, DSR, OLSR) with automated result parsing.

---

## ✨ Features

- ✅ **User-Friendly GUI** - Tkinter-based interface
- ✅ **Protocol Support** - AODV, DSR (DYMO), OLSR
- ✅ **AODV Fine-Tuning** - Route timeout, Hello interval, Hello loss parameters
- ✅ **Auto Configuration** - Generates OMNeT++ `.ini` files automatically
- ✅ **Smart Parser** - Extracts PDR, delay, hop count from `.sca` files
- ✅ **Real-Time Logs** - View simulation progress in GUI

---

## 📂 Project Structure

```
Vfman/
├── main.py              # Entry point
├── gui.py               # GUI interface
├── omnet_manager.py     # OMNeT++ integration
├── models.py            # Data models
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## 🚀 Quick Start

### Prerequisites

| Component | Version | Link |
|-----------|---------|------|
| **Python** | 3.8+ | [python.org](https://www.python.org/) |
| **OMNeT++** | 5.6.2+ | [omnetpp.org](https://omnetpp.org/download/) |
| **INETMANET-3.x** | 3.0+ | [GitHub](https://github.com/aarizaq/inetmanet-3.x) |

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Vfman.git
cd Vfman

# No additional Python packages needed (uses tkinter from standard library)

# Install OMNeT++ and INETMANET separately
```

### Configuration

Edit paths in `omnet_manager.py`:

```python
# Windows
self.omnet_bin = r"C:\omnetpp-5.6.2\bin\opp_run.exe"
self.working_dir = r"C:\inetmanet-3.0"

# Linux/macOS
self.omnet_bin = "/opt/omnetpp-5.6.2/bin/opp_run"
self.working_dir = "/home/user/inetmanet-3.0"
```

---

## 💻 Usage

### Launch GUI

```bash
python main.py
```

### GUI Steps

1. **Select Protocol**: AODV, DSR, or OLSR
2. **Set Parameters**:
   - Node Count: 10-50 (recommended: 20)
   - Simulation Time: e.g., 100s
   - AODV options (optional): Route timeout, Hello interval, Hello loss
3. **Click "Start Simulation"**
4. **View Results** - Automatically parsed and displayed

### Programmatic Usage

```python
from omnet_manager import OmnetManager

manager = OmnetManager()

# Configure
manager.create_config(
    protocol="AODV",
    num_nodes=20,
    sim_time_limit="100s",
    aodv_timeout=3.0,
    aodv_hello_interval=1.0,
    aodv_hello_loss=2
)

# Run
if manager.run_simulation():
    results = manager.parse_results()
    print(f"PDR: {results['pdr']:.2f}%")
    print(f"Avg Delay: {results['delay_avg']:.2f} ms")
    print(f"Avg Hops: {results['hop_avg']:.2f}")
```

---

## 🔧 Supported Protocols

| Protocol | Network Configuration | Status |
|----------|----------------------|--------|
| **AODV** | `inet.examples.aodv.AODVNetwork` |  Fully Featured |
| **DSR** | `inet.examples.manetrouting.dymo.DYMONetwork` | Developing |
| **OLSR** | `inet.examples.adhoc.ieee80211.Net80211` |  Developing |

---

## 📊 Metrics

Automatically extracted metrics:
- **PDR** (Packet Delivery Ratio) - %
- **Delay** (End-to-End) - milliseconds
- **Hop Count** - average route length
- **Sent/Received** - packet counts

---

## 🎯 AODV Parameters

Fine-tune AODV performance:

| Parameter | Default | Description |
|-----------|---------|-------------|
| **Route Timeout** | 3.0s | How long unused routes stay valid |
| **Hello Interval** | 1.0s | Frequency of neighbor discovery messages |
| **Hello Loss** | 2 | Missing hellos before link considered dead |

**Example Scenarios:**
- **High Mobility**: `timeout=1.5s, interval=0.5s`
- **Energy Saving**: `timeout=5.0s, interval=2.0s`

---

## 🐛 Troubleshooting

### Common Issues

**1. `libINET.dll not found`**
- Ensure INETMANET is compiled: `make MODE=release` in INETMANET directory

**2. `No module type named 'RandomWaypointMobility'`**
- Already fixed in code (uses `RandomWPMobility` for INET 3.x)

**3. GUI doesn't start**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

**4. No results shown**
- Check if `.sca` files are generated in `results/` folder
- Ensure simulation runs for sufficient time (>50s)

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m 'Add NewFeature'`
4. Push: `git push origin feature/NewFeature`
5. Open Pull Request

---

## 📚 Resources

- [OMNeT++ Documentation](https://omnetpp.org/documentation/)
- [INETMANET GitHub](https://github.com/aarizaq/inetmanet-3.x)
- [AODV RFC 3561](https://www.ietf.org/rfc/rfc3561.txt)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🌟 Support

If this project helped you:
- ⭐ Star this repository
- 🐛 Report issues on [GitHub Issues](https://github.com/YOUR_USERNAME/Vfman/issues)
- 📢 Share with colleagues

---

**Version**: 1.0.0  
**Last Update**: December 2024

[⬆ Back to Top](#-manet-routing-protocol-simulator)

