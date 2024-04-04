import paramiko
import sys
import time
import keyboard

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
    secondary = False

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        stdin, stdout, stderr = ssh_client.exec_command("kubectl get pods")
     
        for line in stdout:
            if "secondary" in line:
                secondary = True
                print("Secondary store detected. Running rebuild for secondary store pods as well.")

        stdin, stdout, stderr = ssh_client.exec_command('kubectl delete -f /var/lib/rancher/k3s/server/manifests/workloads-default.yaml')
        for line in stdout:
            print(line.strip())

        print("Finished deleting main store pods. Rebuilding...")
        if secondary:
            print("Starting secondary store pod deletion...")
            time.sleep(6)
            stdin, stdout, stderr = ssh_client.exec_command('kubectl delete -f /var/lib/rancher/k3s/server/manifests/secondarystore.yaml')
            for line in stdout:
                print(line.strip())
            print("Finished deleting secondary store pods. Rebuilding...")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Command executed successfully. Please verify pods are running via rancher, or use the -view option.")
        print("Closing connection...")
        ssh_client.close()

def fte_log(username, key_filename):
    storeNumber = input("Enter store number, four digit format 0000: ")
    hostname = 's' + storeNumber + 'svr'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        print("Displaying last 200 lines of transfer.log...")
        stdin, stdout, stderr = ssh_client.exec_command("cd /var/local/volumes/ftp-logs/ && tail -n 200 transfer.log")
        for line in stdout:
            print(line.strip())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Closing connection...")
        ssh_client.close()


def fte_data(username, key_filename):
    storeNumber = input("Enter store number, four digit format 0000: ")
    hostname = 's' + storeNumber + 'svr'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("")
    print("Displaying contents of /var/local/volumes/fte-data/in and /var/local/volumes/fte-data/out...")
    print("")
    try:
        ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        
        print("Here are the files in the 'in' directory:")
        stdin, stdout, stderr = ssh_client.exec_command("cd /var/local/volumes/fte-data/in && ls -l")
        for line in stdout:
            print(line.strip())

        # Print message for the out directory
        print("\nHere are the files in the 'out' directory:")
        stdin, stdout, stderr = ssh_client.exec_command("cd /var/local/volumes/fte-data/out && ls -l")
        for line in stdout:
            print(line.strip())

    except Exception as e:
        print(f"Error: {e}")

    finally:
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
            "-fte_log": fte_log,
            "-fte_data": fte_data,
            "-help": lambda x, y: print("Options: -view, -rebuild, -fte_log, -fte_data"),
            "-ssh_help": lambda x, y: print("ssh connect command: ssh -i C:\Users\giblelc\Desktop\opensshputtykey rancher@s0002svr \n\n Note: path to /in and /out : /var/local/volumes/fte-data/in and /var/local/volumes/fte-data/.")
        }


        if argument in options_map:
            options_map[argument](username, key_filename)
        else:
            print("Option not found. Please use the -help option more information.")

    except IndexError:
        print("Please enter an option. ex: -help")

if __name__ == "__main__":
    main()