import socket
import ipaddress
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


#ports that to be scanned
CommonPorts = [22,80,445,3389,139,21,25,443]

#Timeout value for connections
Timeout = 1


#checks one port on one ip
def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(Timeout)
        #tries to connect through the sock
        sock.connect((str(ip), port))
        sock.close()
        return "open"
    except ConnectionRefusedError:
        #Means the host replied with RST "Port closed but host is live"
        return "closed"
    except socket.timeout:
        # didnot recieve a reply to the connection
        return "filtered"
    except:
        return "filtered"



#scan one host for all common ports
def scan_host(ip):
    result = {}
    result["ip"] = str(ip)
    result["status"] = "down"
    result["open_ports"] = []
    result["closed_ports"] = []

    host_is_alive = False


    for port in CommonPorts:
        port_result = check_port(ip, port)

        if port_result == "open":
            host_is_alive = True
            result["open_ports"].append(port)

        elif port_result == "closed":
            #host will be considered alive due to the respones recieved from the closed port
            host_is_alive = True
            result["closed_ports"].append(port)

    if host_is_alive:
        result["status"] = "up"

    return result



#Markdown report
def markdown(results):
    file = open("Scan_Report.md", "w")
    file.write("Network subnet Scan Report\n")
    file.write("Scan date: " + str(datetime.now()) + "\n\n")
    #prints the live ips only
    for host in results:
        file.write("Host: " + host["ip"] + "\n")
        file.write("Status: UP\n")
        file.write("Open Ports: " + str(host["open_ports"]) + "\n")
        file.write("Closed Ports: " + str(host["closed_ports"]) + "\n\n")

    file.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cidr")
    args = parser.parse_args()

    network = ipaddress.ip_network(args.cidr, strict=False)
    print("\n Welcome!\n Please wait while scanning the subnet:", args.cidr)
    print("--------------------------------------------------")

    results = []

    executor = ThreadPoolExecutor(max_workers=50)
    futures = []

    #submitting the tasks
    for ip in network.hosts():
        future = executor.submit(scan_host, ip)
        futures.append(future)

    #getting and saving the results
    for future in futures:
        host_result = future.result()
        #if the result of the thread that scanned the host is up
        if host_result["status"] == "up":
            print("Host UP:", host_result["ip"])
            print("  Open ports:", host_result["open_ports"])
            print("  Closed ports:", host_result["closed_ports"])
            print("-----------------------------------")
            results.append(host_result)


    executor.shutdown()

    #saving the json file
    file = open("scan_results.json", "w")
    json.dump(results,file, indent=4)
    file.close()

    markdown(results)

    print("\n Scan Finished.\n Results saved to scan_results.json and scan_report.md")


if __name__ == "__main__":
    main()
