import subprocess
import time
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch

class ASDMTopo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')

        # Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Links
        self.addLink(h1, s1)
        self.addLink(h3, s1)
        self.addLink(h2, s2)
        self.addLink(h4, s2)
        self.addLink(s1, s2)   # inter-switch link

def run_topology():
    # Step 1: Start ASDM Controller
    print("🚀 Starting ASDM Controller...")
    controller_process = subprocess.Popen(
        ["python3", "-m", "controller.controller_manager"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)

    # Step 2: Tail all logs
    log_files = [
        "experiments/results_logs/acd_C1.log",
        "experiments/results_logs/sad_C1.log",
        "experiments/results_logs/tsta_C1.log",
        "experiments/results_logs/dam_C1.log",
        "experiments/results_logs/controller_C1.log",
    ]
    print("📜 Tailing logs:", ", ".join(log_files))
    log_tail = subprocess.Popen(
        ["tail", "-f"] + log_files
    )

    # Step 3: Start Mininet with Remote Controller
    topo = ASDMTopo()
    controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=None,
        autoSetMacs=True,
        link=TCLink
    )
    net.addController(controller)
    net.start()

    print("✅ Topology started and linked to ASDM controller.")
    h1, h2 = net.get('h1', 'h2')
    print("🔎 Testing connectivity between h1 and h2:")
    print(h1.cmd('ping -c 3 %s' % h2.IP()))

    # Step 4: Enter CLI
    CLI(net)

    # Step 5: Stop everything
    net.stop()
    controller_process.terminate()
    log_tail.terminate()
    print("🛑 Topology, Controller, and log tail stopped.")

if __name__ == '__main__':
    run_topology()
