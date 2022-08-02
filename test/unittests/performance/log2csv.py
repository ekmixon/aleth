import sys
import re

# regex for the lines with relevant data
test_line = 'time -p ([-_./A-Za-z0-9]*/)*([-_A-Za-z0-9]+) .*; touch (.+).ran$'
gas_line = 'as used: ([0-9]+)'
secs_line = 'user ([0-9.]+)'

# read in data
path = ''
client = ''
test = ''
clients = []
tests = []
gas = {}
data = {}
for line in sys.stdin:
	if match := re.search(test_line, line):
		path = match[1]
		client = match[2]
		test = match[3]
		if client not in clients:
			clients += [client]
		if test not in tests:
			tests += [test]
		continue
	if match := re.search(gas_line, line):
		gas[test] = match[1]
		continue
	if match := re.search(secs_line, line):
		if test not in data:
			data[test] = {}
		data[test][client] = match[1]
		continue

# print the header
sys.stdout.write("(sec/run)")
if len(gas):
	sys.stdout.write(", gas")
for client in clients:
	sys.stdout.write(f", {client}")
sys.stdout.write("\n")

# print the test, gas, secs, secs, ...
for test in tests:
	sys.stdout.write(f"{test}")
	if gas[test]:
		sys.stdout.write(f", {gas[test]}")
	for client in clients:
		sys.stdout.write(f", {data[test][client]}")
	sys.stdout.write("\n")
