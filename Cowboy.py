import paramiko
import sys



def view_pods(username, key_filename):
        storeNumber = input("Enter store number, four digit format 0000: ")
        hostname = 's' + storeNumber + 'svr'
        command = 'kubectl get pods'
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # Connect to the SSH server
            ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
            # Execute the command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            # Print the output of the command
            for line in stdout:
                print(line.strip())

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the SSH connection
            ssh_client.close()


def rebuild(username, key_filename):
    storeNumber = input("Enter store number, four digit format 0000: ")
    hostname = 's' + storeNumber + 'svr'
    command = 'kubectl delete -f /var/lib/rancher/k3s/server/manifests/workloads-default.yaml'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        stdin, stdout, stderr = ssh_client.exec_command(command)
     
        for line in stdout:
            print(line.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Command executed successfully. Please verify pods are running via rancher, or use the -view option.")
        print("Closing connection...")
        ssh_client.close()


def rebuild_secondary(username, key_filename):
    storeNumber = input("Enter store number, four digit format 0000: ")
    hostname = 's' + storeNumber + 'svr'
    command = 'kubectl delete -f /var/lib/rancher/k3s/server/manifests/secondarystore.yaml'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        stdin, stdout, stderr = ssh_client.exec_command(command)

        for line in stdout:
            print(line.strip())

    except Exception as e:
        print(f"Error: {e}")
  
        ssh_client.close()
    finally:
        print("Command executed successfully. Please verify pods are running via rancher, or use the -view option.")
        print("Closing connection...")
        ssh_client.close()

       

def main():
    username = 'rancher'
    key_filename = "C:\\Users\\giblelc\\Desktop\\opensshputtykey"

    try:
        argument = sys.argv[1]
        options_map = {
            "-view": view_pods,
            "-rebuild": rebuild,
            "-rebuild_secondary": rebuild_secondary,
            "-help": lambda x, y: print("Options: -view, -rebuild, -rebuild_secondary")
        }


        if argument in options_map:
            options_map[argument](username, key_filename)
        else:
            print("Option not found. Please use the -help option more information.")

    except IndexError:
        print("Please enter an option. ex: python3 HashHawk.py -help")

if __name__ == "__main__":
    main()