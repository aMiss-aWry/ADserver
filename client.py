# This file represents the basic setup for a client making
# a single request to a running BTO Server.

from BTOClient.BTO import BTO_Client
import sys

HOST = 'localhost'
PORT = 9999
USER = 'salin'
OPTIONS = '-e'
client = BTO_Client()
HEADER = ''

string_input = raw_input("Please enter .c input files, separated by spaces: ")
FILES = string_input.split()

for name in FILES:
	HEADER = HEADER + name + "\n" # + " " + inputfile.read() + "\n"

client.submit_request(HOST, PORT, USER, OPTIONS, FILES, FILES)
