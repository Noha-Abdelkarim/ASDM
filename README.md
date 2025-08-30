# 🛡️ ASDM:Adaptive Sequential DDoS Detection and Mitigation Framework for Secure SD-IoT

> **ASDM** is a modular security framework for **Software-Defined IoT (SD-IoT)** networks.  
It provides **sequential, adaptive, and multi-agent defense** against Sequential DDoS attacks.  
The framework integrates **real-time anomaly detection, trust scoring, adaptive collaboration, and dynamic mitigation**.

---

## 🧠 Key Features

* **Adaptive Collaborative Defense (ACD)**  
  Coordinates alerts across controllers for resilience.
  
* **Sequential Anomaly Detection (SAD)**  
  Hybrid LSTM–GRU model for detecting abnormal traffic sequences.

* **Trust Scoring & Threat Assessment (TSTA)**  
  Evaluates device trustworthiness dynamically.

* **Dynamic Attack Mitigation (DAM)**  
  Enforces blocking, blacklisting, or rate limiting on flows.

* **Extensible Attack Simulation**  
  Supports DDoS test modes: **UDP flood, TCP flood, HTTP flood, Mixed flood**.

---
---
## 📁 Project Structure
ASDM/
├── controller/
│   ├── controller_manager.py        # Orchestrates SAD, TSTA, ACD, DAM agents
│   ├── config/
│   │   ├── controller_policy.json   # Controller thresholds/policies
│   │   ├── block_policy.json        # Mitigation policies
│
├── src/
│   ├── sad/                         # Sequential Anomaly Detection
│   │   ├── sad_agent.py
│   │   ├── models/                  # Saved ML models (lstm_gru_model.h5, scaler.pkl)
│   │   ├── generate_model.py        #  model training
│   │   └── preprocess.py
│   │
│   ├── tsta/                        # Trust Scoring & Threat Assessment
│   │   └── tsta_agent.py
│   │
│   ├── acd/                         # Adaptive Collaborative Defense
│   │   └── acd_agent.py
│   │
│   ├── dam/                         # Dynamic Attack Mitigation
│   │   └── dam_agent.py
│
├── topology/
│   └── asdm_topo.py                 # Mininet topology (IoT hosts + SDN switches)
│
├── attack_simulator/
│   └── attack_launcher.py           # UDP, TCP, HTTP, and Mixed DDoS attacks
│
├── experiments/
│   └── results_logs/                # Runtime logs of all agents & controller
│
├── requirements.txt
└── README.md
---
---
## 🏗️ Requirements

* **Python ≥ 3.8**  
* **Mininet ≥ 2.3.0**  
* **Scapy**, **pandas**, **scikit-learn**, **tensorflow/keras**, **joblib**
---
---
## 🚀 Quick Start

### 1. Set up the environment

Install P4 tools and dependencies:

```bash
pip install -r requirements.txt
```

### 2. Generate baseline model & scaler:

```bash
python3 src/sad/generate_model.py
python3 src/sad/generate_scaler.py
```

### 3. Run controller

```bash
python3 -m controller.controller_manager
```

### 4. Launch topology (With Attack simulation )

Open New TERMINAL

```bash
sudo python3 topology/asdm_topo.py
```

---

## 🧪 Moudels Results

| Moudels | results                                     |
| --------| --------------------------------------------|
| SAD     | Detecs anomaly sequences                    |
| TSTA    | Marks device trust ↓ during sustained flood |
| ACD     | Coordinates trust alerts across controller  |
| DAM     | Blocks/limits victim-facing flow            |

---

---
## 🧪 Performance Metrics

| Metric                        | Value                      |
| ----------------------------- | -------------------------- |
| Binary Detection Accuracy     | 99.22%                     |
| Multi-class Accuracy          | Up to 98.92%               |
| Detection Latency             | 0.21s                      |
| MFRR (Mitigation Flow Recall) | > 88%                      |
| EMP (Effective Mitigation %)  | > 96.9%                    |
| Failover Accuracy             | ≥ 96.6%                    |
| Controller Overhead Reduction | CPU: -31%, Bandwidth: -36% |

---
---
## 🔐 Attack Types Detected

| Attack Type       | Layer(s) | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| UDP Flood         | L3/L4    | High-rate packet flooding                    |
| TCP Flood         | L4       | SYN/ACK storm to exhaust connections         |
| HTTP Flood        | L7       | Application-layer request floods             |
| Mixed             | Multi    | Simultaneous UDP + TCP                       |

---

---

Enjoy Testing :)
  
---

