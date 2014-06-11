import socket

from hashlib import md5
from struct import unpack
from pickle import loads

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ipv4
from ryu.lib import hub


PORT = 12000
ETHTYPE_IPV4 = 0x0800


class FlowSamp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FlowSamp, self).__init__(*args, **kwargs)
        self.monitor_port = 1
        self.mac_to_port = {}
        self.monitor_feedback = None
        self.accept_limit = None
        self.accept_limit_percentage = 10
        self.update_accept_limit(self.accept_limit_percentage)
        self.feedback_loop = hub.spawn(self.monitor_feedback_loop)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        ipv4i = pkt.get_protocol(ipv4.ipv4)

        dst = eth.dst
        src = eth.src

        if ipv4i is not None:
            ipv4_src = ipv4i.src
            ipv4_dst = ipv4i.dst
        else:
            ipv4_src = "-"
            ipv4_dst = "-"

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s %s", dpid, src, dst,
                          ipv4_src, ipv4_dst)
        self.flow_string = self.build_flow_string(dpid, src, dst,
                                                  ipv4_src, ipv4_dst)

        # Learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = None
        #  Monitor Decision Mechanism
        if ipv4i is not None:
            monitor_flow = True
            monitor_flow = self.flow_decision(self.flow_string)

            if monitor_flow:
                # Forward to Monitor As Well
                actions = [parser.OFPActionOutput(out_port),
                           parser.OFPActionOutput(self.monitor_port)]
                self.logger.info("Flow Monitored")
            else:
                actions = [parser.OFPActionOutput(out_port)]
                self.logger.info("Flow Not Monitored")

            # install a flow to avoid packet_in next time
            if out_port != ofproto.OFPP_FLOOD:
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst,
                                        eth_src=src,
                                        eth_type=ETHTYPE_IPV4,
                                        ipv4_dst=ipv4_dst,
                                        ipv4_src=ipv4_src)
                print(match)
                self.add_flow(datapath, 1, match, actions)
                self.logger.info("Adding Flow...")

        else:
            actions = [parser.OFPActionOutput(out_port)]
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    def build_flow_string(self, *args):
        """Build a concatenated string from the various flow characteristics"""
        flow_string = ""
        for arg in args:
            flow_string += str(arg)
        return flow_string

    def flow_decision(self, flow_string):
        """Checks the new incoming flow and makes a decision based on
           last known monitor load.
        """
        flow_hash = hash_flow(flow_string)
        print(flow_hash)
        print(self.accept_limit)
        if flow_hash <= self.accept_limit:
            return True
        else:
            return False

    def update_accept_limit(self, percentage):
        """Change the monitor accept percentage to the argument"""
        max_size = 2 ** 32 - 1
        new_size = (max_size / float(100)) * percentage
        self.accept_limit = new_size
        self.logger.info("Accept Limit Changed To %s", percentage)

    def monitor_feedback_loop(self, port=PORT):
        """Listens to feedback from monitor
           Updates Accept Limit based on analysis
        """
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.bind(('', port))
        self.logger.info("Listening For Feedback")
        while True:
            data, addr = ss.recvfrom(4)
            self.logger.info("Feedback in..")
            message = unpack("!I", data)
            print(message)
            """self.accept_limit_percentage = self.accept_limit_percentage * (
                    adjustAcceptLimit(message) / float(100))
            if self.accept_limit_percentage > 100:
                self.accept_limit_percentage = 100
            self.update_accept_limit(self.accept_limit_percentage)
            """


def hash_flow(flow_string):
    """Creates an MD5 hash for a particular flow string.
       Return only first 4 characters of the hash
    """
    hasher = md5()
    hasher.update(flow_string)
    return unpack("!I", hasher.digest()[:4])[0]
