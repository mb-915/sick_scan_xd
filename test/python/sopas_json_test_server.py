"""
    A simple sopas test server using json input. A listening tcp socket is opened, incoming connections are accepted and cola telegrams are responded on client requests.
    After 10 seconds, datagrams are sent continously.
    All data (sopas responses and telegrams) are read from json file, which can be created from pcapng-file by pcap_json_converter.py
    Note: This is just a simple test server for sick_scan_xd unittests. It does not emulate any device.

    Usage:
    python sopas_json_test_server.py --tcp_port=<int> --json_file=<filepath>
    
    Example:
    python ../test/python/sopas_test_server.py --tcp_port=2111 --json_file=../emulator/scandata/20221018_rms_1xxx_ascii_rawtarget_object.pcapng.json

"""

import argparse
import datetime
import json
import select
import socket
import time
import threading

"""
    SopasTestServer connects to a tcp client, receives cola telegrams and sends a response to the client.
"""
class SopasTestServer:

    # Constructor
    def __init__(self, tcp_port = 2112, json_tcp_payloads = []):
        self.tcp_port = tcp_port
        self.json_tcp_payloads = json_tcp_payloads
        self.run_message_loop = False

    # Waits for an incoming tcp connection and connects to the tcp client
    def connect(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(("", self.tcp_port))
        print("SopasTestServer: listening on tcp port {}".format(self.tcp_port))
        self.serversocket.listen(1)
        (clientsocket, clientaddress) = self.serversocket.accept()
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        self.clientsocket.setblocking(0)
        self.run_message_loop = True
        print("SopasTestServer: tcp connection to {} established".format(self.clientaddress))

    # Receives a cola telegram and returns its payload (i.e. the telegram without header and CRC)
    def receiveTelegram(self, recv_timeout_sec):
        payload = bytearray(b"")
        payload_idx = -1
        ready_to_recv = select.select([self.clientsocket], [], [], recv_timeout_sec)
        if ready_to_recv[0]:
            byte_recv = b"\x00"
            while byte_recv != b"\x02":
                byte_recv = self.clientsocket.recv(1)
            payload = payload + byte_recv
            while True:
                byte_recv = self.clientsocket.recv(1)
                payload = payload + byte_recv
                if payload in self.json_tcp_payloads:
                    payload_idx = self.json_tcp_payloads.index(payload)
                    break
            print("SopasTestServer.receiveTelegram(): received {} byte telegram {}".format(len(payload), payload))
        return payload, payload_idx

    # Sends a cola telegram "as is"
    def sendTelegram(self, telegram, verbosity):
        if verbosity > 1:
            print("SopasTestServer.sendTelegram(): sending {} byte telegram {}".format((len(telegram)), telegram))
        elif verbosity > 0:
            print("SopasTestServer.sendTelegram(): sending {} byte telegram".format(len(telegram)))
        self.clientsocket.send(telegram)

    # Runs the message loop, i.e. receives sopas telegrams and sends a response to the client
    def run(self):
        print("SopasTestServer: running event loop...")
        while self.run_message_loop:
            # Receive a cola telegram
            received_telegram, json_tcp_payload_idx = self.receiveTelegram(1)
            if len(received_telegram) <= 0: # timeout (no message rececived)
                continue
            # Lookup sopas response to sopas request
            if json_tcp_payload_idx >= 0 and json_tcp_payload_idx + 1 < len(self.json_tcp_payloads):
                response_payload = self.json_tcp_payloads[json_tcp_payload_idx + 1]
                print("SopasTestServer: request={}, response={}".format(received_telegram, response_payload))
                self.sendTelegram(response_payload, 2)
            else:
                print("## ERROR SopasTestServer: request={} not found in json file".format(received_telegram))
            time.sleep(0.01)
        
    # Starts the message loop in a background thread
    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    # Stops the message loop thread
    def stop(self):
        self.run_message_loop = False

"""
    Run sopas test server using json input for sopas requests and responses
"""
if __name__ == "__main__":

    # Configuration
    tcp_port = 2111 # tcp port to listen for tcp connections
    scandata_id = "sSN LMDradardata"
    json_file = "../emulator/scandata/20221018_rms_1xxx_ascii_rawtarget_object.pcapng.json"  # input jsonfile with sopas requests, responses and telegrams
    verbosity = 2  # print all telegrams
    send_rate = 10 # send 10 scandata telegrams per second
    
    # Overwrite with command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--tcp_port", help="tcp port to listen for tcp connections", default=tcp_port, type=int)
    arg_parser.add_argument("--json_file", help="input jsonfile with sopas requests, responses and telegrams", default=json_file, type=str)
    arg_parser.add_argument("--scandata_id", help="sopas id of scandata telegrams, e.g. \"sSN LMDradardata\"", default=scandata_id, type=str)
    arg_parser.add_argument("--send_rate", help="send rate in telegrams per second", default=send_rate, type=float)
    arg_parser.add_argument("--verbosity", help="verbosity (0, 1 or 2)", default=verbosity, type=int)
    cli_args = arg_parser.parse_args()
    tcp_port = cli_args.tcp_port
    json_file = cli_args.json_file
    scandata_id = cli_args.scandata_id
    verbosity = cli_args.verbosity
    send_rate = cli_args.send_rate
    
    # Parse json file
    print("sopas_json_test_server: parsing json file \"{}\":".format(json_file))
    with open(json_file, 'r') as file_stream:
        json_input = json.load(file_stream)
    json_tcp_payloads = [] # list of bytearray of the tcp payload
    for json_entry in json_input:
        try:
            tcp_description = json_entry["_source"]["layers"]["tcp"]["tcp.description"]
            tcp_payload_json = json_entry["_source"]["layers"]["tcp"]["tcp.payload"]
            tcp_payload_hex_str = "".join(tcp_payload_json.split(":"))
            tcp_payload = bytearray.fromhex(tcp_payload_hex_str)
            json_tcp_payloads.append(tcp_payload)
            # print("tcp_description: \"{}\", tcp_payload: \"{}\", payload_bytes: {}".format(tcp_description, tcp_payload, payload))
        except Exception as exc:
            print("## ERROR parsing file {}: \"{}\", exception {}".format(json_file, json_entry, exc))
    for json_tcp_payload in json_tcp_payloads:     
        print("{}".format(json_tcp_payload))

    # Run sopas test server
    print("sopas_json_test_server: running event loop ...")
    server = SopasTestServer(tcp_port, json_tcp_payloads)
    server.connect()
    server.start()

    # Send sopas telegrams, e.g. "sSN LMDradardata ..."
    time.sleep(5)
    print("sopas_json_test_server: start sending scandata \"{}\" ...".format(scandata_id))
    scandata_id = bytearray(scandata_id.encode())
    while True:
        for payload in json_tcp_payloads:
            if payload.find(scandata_id,0) >= 0:
                # print("sopas_json_test_server: sending scandata \"{}\" ...".format(payload))
                server.sendTelegram(payload, 2)
                time.sleep(1.0 / send_rate)

    server.stop()