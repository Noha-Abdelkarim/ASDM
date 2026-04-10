# 🛡️ ASDM:Adaptive Sequential DDoS Detection and Mitigation Framework for Secure SD-IoT

> **ASDM** is a modular security framework for **Software-Defined IoT (SD-IoT)** networks.  
It provides **sequential, adaptive, and multi-agent defense** against Sequential DDoS attacks.  
The framework integrates **real-time anomaly detection, trust scoring, adaptive collaboration, and dynamic mitigation**.

---

## 🧠 Key Features

* **Adaptive Collaborative Defense (ACD)**  
  Enhance inter-controller resilience and initiate coordinated detection and mitigation.
  
* **Sequential Anomaly Detection (SAD)**  
  Detect sequential DDoS patterns using Hybrid LSTM–GRU model.

* **Time-Series Traffic Analysis  (TSTA)**  
  Extract temporal and protocol-specific traffic features at the data plane.

* **Decentralized Adaptive Mitigation  (DAM)**  
  Coordinate decentralized mitigation actions to isolate threats and maintain availability.

* **Extensible Attack Simulation**  
  Supports DDoS test modes: **UDP flood, TCP flood, HTTP flood, Mixed flood**.

---
---
## 📂 Project Structure

 ``` 
ASDM/
├── controller/
│ ├── controller_manager.py                         # Orchestrates ACD, SAD, TSTA, DAM
│ │
│ └── config/
│ ├── controller_policy.json
│ ├── block_policy.json
│
├── src/
│ ├── acd/                                           # Attack Classification & Detection
│ │ └── acd_agent.py
│ │
│ ├── sad/ # Sequential Attack Detection
│ │ ├── sad_agent.py
│ │ ├── generate_model.py                            # Builds & saves LSTM-GRU model
│ │ ├── generate_scaler.py                           # Builds & saves feature scaler
│ │ ├── models.py                                    # Model architecture (LSTM-GRU hybrid)
│ │ └── preprocess.py                                # Data preprocessing utilities
│ │
│ ├── tsta/                                          # Temporal-Spatial Threat Analysis
│ │ └── tsta_agent.py
│ │
│ ├── dam/                                           # Defense & Mitigation
│ │ └── dam_agent.py
│ 
├── topology/
│ └── asdm_topo.py                                   # Mininet network topology
│
├── attack_simulator/
│ └── attack_launcher.py                             # UDP, TCP, HTTP, Mixed flood attacks
│
├── experiments/
│ └── results_logs/                                  # Runtime logs (acd_C1.log, sad_C1.log, etc.)
│
├── requirements.txt                                 # Python dependencies
└── README.md                                        # Project documentation

 ```
---
## 🏗️ Requirements

* **Python ≥ 3.8**  
* **Mininet ≥ 2.3.0**  
* **Scapy**, **pandas**, **scikit-learn**, **tensorflow/keras**, **joblib**
---
---
## 📘 Solution Manual

ASDM can be deployed in **two modes**:  
1. 🖥️ **Emulation Environment** (for research and testing)  
2. 🌐 **Real-World Deployment** (for production SD-IoT networks)  

---

### 🖥️ 1. Emulation Environment (Mininet + P4 + Simulator)

This mode is ideal for experiments, reproducibility, and validation.

#### Step 1: Environment Setup
```bash
pip install -r requirements.txt
sudo apt-get install mininet
```
#### Step 2: Prepare Models
```bash
python3 src/sad/generate_model.py
python3 src/sad/generate_scaler.py
```
This builds and saves the hybrid LSTM–GRU model and the feature scaler used for SAD (Sequential Attack Detection).

#### Step 3: Start Controller
```bash
python3 -m controller.controller_manager
```
This orchestrates ACD, SAD, TSTA, and DAM modules.

#### Step 4: Launch Network Topology
```bash
sudo python3 topology/asdm_topo.py
```
This deploys a Mininet network with SDN switches and IoT devices.

#### Step 5: Simulate Attacks
```bash
python3 attack_simulator/attack_launcher.py --attack udp
python3 attack_simulator/attack_launcher.py --attack tcp
python3 attack_simulator/attack_launcher.py --attack http
python3 attack_simulator/attack_launcher.py --attack mix
```
Supported attack types: UDP Flood, TCP SYN Flood, HTTP Flood, Mixed Flood.

#### Step 6: Monitor Results
Logs saved in:
```bash
experiments/results_logs/
```
Example files: acd_C1.log, sad_C1.log
Metrics reported: detection time, mitigation latency, CPU usage, recovery %

### 🌐 2. Real-World Deployment (SD-IoT Network)

This mode integrates ASDM with **real SDN controllers, IoT/edge devices, and P4-enabled switches**.

#### Step 1: Deploy Controller
Install ASDM on your **controller host** and start the orchestrator:
```bash
# Clone repository
git clone https://github.com/Noha-Abdelkarim/ASDM.git
cd ASDM

# Install dependencies
pip install -r requirements.txt

# Start ASDM controller (manages ACD, SAD, TSTA, DAM)
python3 -m controller.controller_manager
```

#### Step 2: Connect IoT/Edge Devices
Configure IoT devices to send their traffic through the SDN switch.  

**For OpenFlow switches:**
```bash
# Example (on Open vSwitch)
sudo ovs-vsctl set-controller br0 tcp:<controller-ip>:6633
```
**For P4 switches with P4Runtime:**
```bash
# Launch P4 switch with controller connection
simple_switch_grpc --device-id 0 \
    --log-console \
    --thrift-port 9090 \
    --no-p4 \
    --grpc-server-addr 0.0.0.0:50051 \
    --controller <controller-ip>:50051
```
#### Step 3: Enable SAD + TSTA

These modules are automatically activated when the controller runs.
Monitor them in real time:
```bash
tail -f experiments/results_logs/sad_C1.log
tail -f experiments/results_logs/tsta_C1.log
```

#### Step 4: Real Traffic & Attack Injection

Run normal IoT traffic (MQTT, CoAP, HTTP) on your devices.
For controlled DDoS attack injection:
```bash
# From an attack node
hping3 <target-ip> --flood --udp -p 80      # UDP Flood
hping3 <target-ip> --flood -S -p 80         # TCP SYN Flood
ab -n 100000 -c 1000 http://<target-ip>/    # HTTP Flood
```

#### Step 5: Adaptive Mitigation (DAM)

SThe DAM module automatically applies flow rules.
Inspect applied rules with:
```bash
# For Open vSwitch
sudo ovs-ofctl dump-flows br0

# For P4 switches
simple_switch_CLI --thrift-port 9090 <<< "table_dump"
```

#### Step 6: Validate Performance

Monitor performance and recovery:
```bash
# CPU usage
htop

# Bandwidth usage
iftop -i eth0

# Logs of detection/mitigation
tail -f experiments/results_logs/dam_C1.log
```
---

## 📊 Evaluation Datasets

ASDM has been rigorously tested and validated using four diverse and widely recognized datasets:

* [CIC IoMT 2024](https://www.unb.ca/cic/datasets/iomt-dataset-2024.html) – IoMT-focused traffic dataset with multi-vector DDoS scenarios  
* [UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) – Comprehensive dataset including modern attack subtypes and normal traffic  
* [ToN_IoT](https://research.unsw.edu.au/projects/toniot-datasets) – IoT telemetry and multi-vector low-rate attack dataset  
* [CIC IoT 2023](https://www.unb.ca/cic/datasets/iotdataset-2023.html) – Real IoT protocol traffic with noise and imbalance challenges  

---

---
## 🧪 Modules outcomes

The ASDM framework integrates four coordinated modules. Their real-world roles and outcomes are summarized below:

| 🔬 **Module** | 📝 **Description of Results**                                                                              |
|--------------------------------------------------|--------------------------------------------------------------------------|
| 🧩 **SAD** ( Sequential Anomaly Detection )     | Detects anomalous traffic sequences with high temporal accuracy          |
| 🔐 **TSTA** ( Time-Series Traffic Analysis )    | Dynamically adjusts device trust scores during sustained flood attacks   |
| 📡 **ACD** ( Adaptive Collaborative Defense )   | Classifies attack vectors and coordinates alerts across controllers       |
| 🛡️ **DAM** ( Decentralized Adaptive Mitigation ) | Enforces mitigation by blocking, throttling, or rerouting malicious flows|

✅ These modules operate **sequentially and cooperatively**, ensuring early anomaly detection (SAD), contextual device trust analysis (TSTA), accurate attack classification (ACD), and adaptive mitigation strategies (DAM).  

---

---
## 🧪 Performance Metrics

| Metric                        | Value                                      |
| ----------------------------- | ------------------------------------------ |
| Binary Detection Accuracy     | Up to **98.3%**                            |
| Multi-class Accuracy          | Up to **98.9%**                            |
| Precision                     | Up to **97.5%**                            |
| Recall                        | Up to **99.0%**                            |
| F1-Score                      | Up to **98.9%**                            |
| Detection Latency             | < **12 ms**                                |
| Mitigation Latency            | **2.5 – 3.9 s**                            |
| False Alarm Rate (FAR)        | **0.4% – 2.1%**                            |
| CPU Utilization               | < **31%** at peak attack loads             |
| Traffic Recovery              | > **98%** during mitigation                |

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
## 🧪 End-to-End Experiment Workflow

The experimental workflow implemented in this repository follows the pipeline described in the paper:

1. **Traffic Generation**  
   - Normal and attack traffic generated using `attack_simulator/attack_launcher.py`

2. **Feature Extraction (TSTA)**  
   - Traffic statistics are collected and processed at runtime  

3. **Sequential Detection (SAD)**  
   - Pre-trained LSTM–GRU model processes traffic sequences  

4. **Attack Classification (ACD)**  
   - Traffic patterns are categorized into attack types  

5. **Mitigation (DAM)**  
   - Controller applies mitigation actions (blocking/throttling)

6. **Logging & Evaluation**  
   - All events and metrics are recorded in `experiments/results_logs/`

---
---

## 🔍 Execution Flow (Code-Level Trace)

To clarify the functional implementation of ASDM, the following describes the **actual execution path across modules**:

### 1. Controller Initialization
- Entry point: `controller/controller_manager.py`
- Responsible for orchestrating all modules (ACD, SAD, TSTA, DAM)
- Initializes agents and shared state

---

### 2. Traffic Processing Pipeline

#### Step 1: Traffic Input
- Traffic is generated via:
  - `attack_simulator/attack_launcher.py`
- Packets are forwarded through Mininet topology (`topology/asdm_topo.py`)

---

#### Step 2: Feature Extraction (TSTA)
- Module: `src/tsta/tsta_agent.py`
- Extracts:
  - packet rate
  - protocol distribution
  - temporal patterns

---

#### Step 3: Sequential Detection (SAD)
- Module: `src/sad/sad_agent.py`
- Uses:
  - Pre-trained LSTM–GRU model (`models.py`)
  - Scaler (`generate_scaler.py`)
- Outputs:
  - anomaly score / classification

---

#### Step 4: Attack Classification (ACD)
- Module: `src/acd/acd_agent.py`
- Determines:
  - attack type (UDP, TCP, HTTP, Mixed)
- Shares results with controller

---

#### Step 5: Mitigation Decision (DAM)
- Module: `src/dam/dam_agent.py`
- Applies:
  - blocking rules
  - rate limiting
  - flow control actions

---

#### Step 6: Logging & Monitoring
- Logs generated in:
  - `experiments/results_logs/`
- Includes:
  - detection events
  - classification outputs
  - mitigation actions

---

### 🔗 Integration Logic

All modules are coordinated via:

```bash
controller/controller_manager.py
```

which:
- receives traffic statistics
- invokes detection (SAD)
- triggers classification (ACD)
- executes mitigation (DAM)

---

### 📌 Note

The framework follows a **modular and decoupled architecture**, where each component operates independently but is orchestrated centrally through the controller.

---
---

## 🧪 🔁 Reproducibility & Experiment Replication

To ensure **full reproducibility of the results reported in the paper**, this repository provides a complete, self-contained experimental pipeline.

### 📌 What is Reproducible?

The following results from the paper can be reproduced:

- Detection accuracy (binary & multi-class)
- Detection latency (< 12 ms)
- Mitigation latency (2.5–3.9 s)
- False Alarm Rate (FAR)
- CPU utilization under attack
- Traffic recovery rate (> 98%)

---

### ⚙️ Complete Reproduction Pipeline

Run the following steps **in order** to replicate the experiments:

```bash
# 1. Install dependencies
pip install -r requirements.txt
sudo apt-get install mininet

# 2. Generate ML models
python3 src/sad/generate_model.py
python3 src/sad/generate_scaler.py

# 3. Start ASDM controller
python3 -m controller.controller_manager

# 4. Launch network topology
sudo python3 topology/asdm_topo.py

# 5. Run attack scenario (example: UDP flood)
python3 attack_simulator/attack_launcher.py --attack udp
```

---

### ⚔️ Supported Experiment Scenarios

You can reproduce all scenarios used in the paper:

```bash
--attack udp     # UDP Flood
--attack tcp     # TCP SYN Flood
--attack http    # HTTP Flood
--attack mix     # Mixed multi-vector attack
```

---

### 📊 Expected Output

After running experiments, logs will be generated in:

```bash
experiments/results_logs/
```

Example:
- `sad_C1.log` → anomaly detection results  
- `acd_C1.log` → attack classification  
- `dam_C1.log` → mitigation actions  

Each log includes:
- Detection timestamps  
- Attack classification labels  
- Mitigation decisions  
- Performance metrics  

---

### 🔗 Mapping to Paper Results

| Paper Section | Script / Module |
|--------------|----------------|
| Sequential Detection (SAD) | `src/sad/sad_agent.py` |
| Trust Analysis (TSTA) | `src/tsta/tsta_agent.py` |
| Attack Classification (ACD) | `src/acd/acd_agent.py` |
| Mitigation (DAM) | `src/dam/dam_agent.py` |
| Attack Generation | `attack_simulator/attack_launcher.py` |
| Topology Setup | `topology/asdm_topo.py` |

---

### 🧩 Environment Details

- Mininet ≥ 2.3.0 (network emulation)  
- BMv2 / P4Runtime (programmable data plane support)  
- Python ≥ 3.8  
- TensorFlow/Keras (LSTM–GRU model)  

---

### 🧪 Notes on Determinism

- Random seeds are fixed during model generation  
- Attack traffic parameters are deterministic  
- Results may slightly vary depending on CPU performance  

---

### ✅ Reproducibility Checklist

- [x] Full source code available  
- [x] Experiment scripts included  
- [x] Attack scenarios reproducible  
- [x] Logs and metrics generated automatically  
- [x] Environment setup documented  

---
Have a Good Testing :)
  
---









