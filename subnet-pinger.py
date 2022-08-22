# Import modules
import subprocess
import ipaddress
import os.path
import signal

# Method to check if Ctrl-c was pressed
def handler(signum, frame):
    res = input("\n\nCtrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)

signal.signal(signal.SIGINT, handler)

# Helper variables to get percentage done
#  of the subnet pinger script
previous_percentage = 0
iteration = 1

# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Prompt the user to input a name for the file
fileName = input("Enter a name for the file where the output will be saved: ")
fileName = fileName+".txt"

# Check if file exists then create and open the file or overwrite
if os.path.exists(fileName):
    print("The file already exists. It will be overwritten.")
    ip_list = open(fileName,"w")
else:
    print("The file "+fileName+" will be created.")
    ip_list = open(fileName,"a")

# Create the network
subnet = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(subnet.hosts())
usable_hosts = len(all_hosts)


print("\n\n"+str(usable_hosts)+" hosts will be scanned.")

# For each IP address in the subnet, 
# run the ping command with subprocess.run interface

for i in range(len(all_hosts)):

    # Save ping output in the 'output' variable
    output = str(subprocess.run(["ping",str(all_hosts[i]),"-c","1","-W","1000"],capture_output=True))
    
    # Check what's inside the output variable and 
    # decide if the host is online or not
    if "Destination host unreachable" not in output:
        if "Request timeout" not in output:
            if "100.0% packet loss" not in output:
                ip_list.write(str(all_hosts[i])+" is Online\n")
    else:
        ip_list.write(str(all_hosts[i])+" is Offline\n")

    # Calculate the percentage done by knowing 
    # how many ips have already pinged
    percent_done = int((iteration/usable_hosts)*100)
    
    # Avoid repetitive percentages shown on the screen
    if previous_percentage == percent_done:
        pass
    else:
        previous_percentage = percent_done
        print(str(percent_done)+"%"+"\t\t"+str(iteration)+"/"+str(usable_hosts)+" hosts scanned")

    # Increase the number of iteration
    iteration = iteration + 1 

ip_list.close()
print("All done! You can check the output in the file "+fileName)