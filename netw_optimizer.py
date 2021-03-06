from munkres import Munkres
from collections import defaultdict
import itertools
import sys
import argparse
from copy import deepcopy

##################################################
# This code sorts the servers according to their
# network cost. It will then check whether the
# least network cost nodes support the requirements
# imposed by services. If the least network cost
# node does not support the the service, the next
# node in the list will be checked until a suitable
# node is found.
####################################################

#############################
#INPUT
parser = argparse.ArgumentParser()

parser.add_argument("-size", "--size", help="size of the graph", required=True)
parser.add_argument("-sbw", "--service_bw", type=int, help="service bandwidth", required=True)
parser.add_argument("-sproc", "--service_proc", type=int, help="service processing", required=True)

args = parser.parse_args()

size = args.size
service_bw = args.service_bw
service_proc = args.service_proc

filepath = "Files/"+ size

with open(filepath+"/device_conn") as f:
    device_conn = [[int(num) for num in line.split()] for line in f]

with open(filepath+"/device_proc") as f:
    for line in f:
        device_proc = [float(i) for i in line.split()]

with open(filepath+"/edge_levels") as f:
    for line in f:
        edge_levels = [int(i) for i in line.split()]

with open(filepath+"/bandwidth") as f:
    for line in f:
        bandwidth = [int(i) for i in line.split()]
################################

def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return (locs for key,locs in tally.items()
                            if len(locs)>1)

def print_assignment(index, command):
    proc_cost=0
    for row, column in index:
        proc = matrix[row][column]
        proc_cost += proc
        if (command==1):
            print("Job %d -> Device %d" % (row+1, column+1))
    if (command==1):
        print("total processing cost: %.3f" % proc_cost)
    else:
        return proc_cost

def print_network_cost(index, connections, command):
    net_cost = 0
    for i in range(len(connections)):
        job1 = connections[i][0]
        job2 = connections[i][1]
        for j in range(len(index)):
            if(index[j][0]==job1):
                device1 = index[j][1]
                continue
            if(index[j][0]==job2):
                device2 = index[j][1]
        cost = device_conn[device1][device2]
        net_cost += cost
    if (command==1):
        print("Total networking cost: %d" % net_cost)
    else:
        return net_cost


netw_conn = []
edge_netw_conn = []
devices = []

no_devices = len(device_proc)

## Get a list of devices
i = 0
while i < no_devices:
    devices.append(i)
    i += 1

i = 1
while i <= no_devices:
    netw_cost = device_conn[0][i]
    edge_netw_conn.append(netw_cost)

    netw_cost = netw_cost + device_conn[i][no_devices+1]            ## should this line not be there if you want to put services more towards the edge?
    netw_conn.append(netw_cost)

    i += 1

#edge_nw = deepcopy(edge_netw_conn)
edge_nw = deepcopy(netw_conn)

#sort the devices based on their network cost from the client
#devices_netw_sorted = [devices for edge_netw_conn, devices in sorted(zip(edge_netw_conn, devices))]
devices_netw_sorted = [devices for netw_conn, devices in sorted(zip(netw_conn, devices))]

i = 1
selected_device = 0;

while i <= no_devices:
    index = devices_netw_sorted[i-1]
    if bandwidth[index]>=service_bw and device_proc[index] >= service_proc:
        selected_device = index+1
        break
    i += 1

if selected_device != 0:
    proc_cost = device_proc[selected_device] / service_proc
    proc_cost = edge_levels[selected_device] * proc_cost

    print(" Selected Edge server: %d, Tier level: %d, Bandwidth: %d, Processing power: %d, Processing cost: %d, Network cost: %d" %
        (selected_device, edge_levels[selected_device-1], bandwidth[selected_device-1], device_proc[selected_device-1], proc_cost, edge_nw[selected_device-1]))

else:
    print("No good server found for placement")