import paramiko
import time
import os

# --- SCRIPT INTENTION: Remote Command Execution with Paramiko (SSH) ---
# This script shows how to connect to a remote server via SSH and execute
# commands using the 'paramiko' library. It illustrates secure
# programmatic control over remote machines for automation tasks.
# Remember to configure your server details and prioritize SSH keys for security!

# --- Configuration for your remote server ---
REMOTE_HOST = "localhost"
REMOTE_PORT = 22 # Default SSH port
REMOTE_USER = "your_remote_username"
REMOTE_PASSWORD = "your_remote_password" # Use for simple demo, but SSH keys are more secure
# OR: PATH_TO_PRIVATE_KEY = "/path/to/your/ssh/private_key" # e.g., ~/.ssh/id_rsa

def run_paramiko_example():
    print("--- Paramiko Remote Command Execution Example ---")

    # Create an SSH client instance
    client = paramiko.SSHClient()
    # Automatically add the server's host key (NOT RECOMMENDED FOR PRODUCTION)
    # In production, you'd usually load known_hosts: client.load_system_host_keys()
    # or client.set_missing_host_key_policy(paramiko.RejectPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"\n1. Connecting to {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PORT}...")
        # Connect using password
        client.connect(hostname=REMOTE_HOST, port=REMOTE_PORT,
                       username=REMOTE_USER, password=REMOTE_PASSWORD,
                       timeout=10)
        # OR connect using private key:
        # client.connect(hostname=REMOTE_HOST, port=REMOTE_PORT,
        #                username=REMOTE_USER, key_filename=PATH_TO_PRIVATE_KEY,
        #                timeout=10)
        print("   Successfully connected.")

        # --- Example 1: Execute a simple command ---
        command = "ls -l /tmp" # Example: list contents of /tmp on remote
        print(f"\n2. Executing command remotely: '{command}'")
        stdin, stdout, stderr = client.exec_command(command)

        # Read output
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        if output:
            print("   Remote Command Output:\n", output)
        if errors:
            print("   Remote Command Errors:\n", errors)
            # You might want to check the exit status if more robust error handling is needed
            # exit_status = stdout.channel.recv_exit_status()
            # print(f"   Exit Status: {exit_status}")

        # --- Example 2: Create a dummy file on remote ---
        remote_file_content = "This is a file created via Paramiko."
        remote_file_path = "/tmp/paramiko_test.txt" # Change if /tmp isn't writable

        # Command to create a file
        create_command = f"echo '{remote_file_content}' > {remote_file_path}"
        print(f"\n3. Creating remote file: '{remote_file_path}'")
        stdin, stdout, stderr = client.exec_command(create_command)
        stdout.channel.recv_exit_status() # Wait for command to complete and get exit status

        if not stderr.read(): # If no errors in stderr
            print(f"   Successfully created file: {remote_file_path}")
            # Verify its content
            verify_command = f"cat {remote_file_path}"
            print(f"   Verifying content of '{remote_file_path}':")
            _, verify_stdout, _ = client.exec_command(verify_command)
            verified_content = verify_stdout.read().decode().strip()
            print(f"   Remote content: '{verified_content}'")
        else:
            print(f"   Error creating file: {stderr.read().decode().strip()}")

    except paramiko.AuthenticationException:
        print("\nAuthentication failed. Check username and password/key.")
    except paramiko.SSHException as e:
        print(f"\nCould not establish SSH connection: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Close the SSH connection
        if client:
            client.close()
            print("\nSSH connection closed.")
        print("--- Paramiko Remote Execution Example Finished ---")

if __name__ == "__main__":
    # IMPORTANT: Replace these placeholders with your actual server details!
    # For security, avoid hardcoding passwords in real applications.
    # Consider using environment variables or a configuration file.
    # Also, always use SSH keys in production.
    if REMOTE_HOST == "your_remote_server_ip_or_hostname":
        print("--- WARNING: Please configure REMOTE_HOST, REMOTE_USER, and REMOTE_PASSWORD (or PATH_TO_PRIVATE_KEY) ---")
        print("--- in 'paramiko_remote_exec.py' before running this example. ---")
    else:
        run_paramiko_example()