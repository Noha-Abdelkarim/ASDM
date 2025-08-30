/* 
ASDM - P4 Feature Extraction Module
-----------------------------------
This P4 program extracts flow-level statistics required for TSTA:
 - Packet count per flow
 - Byte count per flow
 - Protocol type distribution
 - Inter-arrival times
*/

#include <core.p4>

header ethernet_t {
    mac_addr dst;
    mac_addr src;
    bit<16>  eth_type;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    bit<32>   srcAddr;
    bit<32>   dstAddr;
}

struct metadata {
    bit<64> timestamp;
}

parser MyParser(packet_in pkt,
                out ethernet_t eth,
                out ipv4_t ip,
                out metadata meta) {
    state start {
        pkt.extract(eth);
        transition select(eth.eth_type) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        pkt.extract(ip);
        transition accept;
    }
}

control Ingress(inout ethernet_t eth,
                inout ipv4_t ip,
                inout metadata meta) {
    /* Feature registers */
    register<bit<32>>(1024) pkt_count;
    register<bit<32>>(1024) byte_count;

    action count_packet(bit<32> flow_id, bit<32> size) {
        pkt_count[flow_id] = pkt_count[flow_id] + 1;
        byte_count[flow_id] = byte_count[flow_id] + size;
    }

    table traffic_stats {
        actions = { count_packet; }
        key = {
            ip.srcAddr: exact;
            ip.dstAddr: exact;
            ip.protocol: exact;
        }
        size = 1024;
    }

    apply {
        bit<32> flow_id = (ip.srcAddr ^ ip.dstAddr) ^ ip.protocol;
        count_packet(flow_id, ip.totalLen);
    }
}

control Egress() { apply { } }
control Deparser(packet_out pkt, in ethernet_t eth, in ipv4_t ip) {
    pkt.emit(eth);
    pkt.emit(ip);
}

V1Switch(MyParser(), Ingress(), Egress(), Deparser()) main;
