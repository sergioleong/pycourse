import subprocess
import platform # To determine the OS

# --- SCRIPT INTENTION: OS Interaction with Subprocess Module ---
# This script demonstrates how to execute external commands and programs
# using Python's `subprocess` module. It covers running commands,
# capturing their output, checking return codes, and highlights
# important security considerations.

def run_subprocess_example():
    print("--- Subprocess Module Example ---")

    # Determine command based on OS for portability
    if platform.system() == "Windows":
        list_command = ["dir"]
        echo_command = ["cmd", "/c", "echo"]
    else: # Linux, macOS
        list_command = ["ls", "-l"]
        echo_command = ["echo"]

    # --- Example 1: Running a simple command and checking return code ---
    print("\n1. Running a simple command (e.g., list current directory contents):")
    try:
        # Popen returns a Process object. communicate() waits for process to terminate.
        # stdout=subprocess.PIPE captures output, stderr=subprocess.PIPE captures errors.
        process = subprocess.Popen(list_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=10) # 10 second timeout

        if process.returncode == 0:
            print("   Command executed successfully.")
            print("   Output:\n", stdout)
        else:
            print(f"   Command failed with exit code {process.returncode}.")
            print("   Error:\n", stderr)

    except FileNotFoundError:
        print(f"   Error: Command '{list_command[0]}' not found.")
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("   Command timed out.")
    except Exception as e:
        print(f"   An unexpected error occurred: {e}")

    # --- Example 2: Running a command with arguments and capturing output ---
    print("\n2. Running a command with arguments and capturing specific output:")
    message = "Hello from subprocess!"
    command_with_args = echo_command + [message]
    try:
        # subprocess.run is a simpler wrapper for common use cases.
        # capture_output=True captures stdout/stderr, text=True decodes as text.
        result = subprocess.run(command_with_args, capture_output=True, text=True, check=True, timeout=5)
        # check=True raises CalledProcessError if return code is non-zero
        print(f"   Command output: '{result.stdout.strip()}'")
    except subprocess.CalledProcessError as e:
        print(f"   Command failed: {e.stderr}")
    except subprocess.TimeoutExpired:
        print("   Command timed out.")
    except FileNotFoundError:
        print(f"   Error: Command '{echo_command[0]}' not found.")
    except Exception as e:
        print(f"   An unexpected error occurred: {e}")

    # --- Example 3: Demonstrating security (no shell injection when shell=False) ---
    print("\n3. Security demonstration (no shell injection):")
    malicious_input = "Hello; rm -rf /" # Harmless on Windows, dangerous on Linux/macOS
    # DANGER: Using shell=True with untrusted input is a security risk!
    # subprocess.run([echo_command[0], malicious_input], shell=False, check=True) # THIS IS SAFE
    print(f"   Attempting to echo: '{malicious_input}'")
    try:
        # The command treats "Hello; rm -rf /" as a single argument to echo, not two commands.
        result = subprocess.run(echo_command + [malicious_input], capture_output=True, text=True, check=True, timeout=5)
        print(f"   Output: '{result.stdout.strip()}' (malicious part was treated as text)")
    except subprocess.CalledProcessError as e:
        print(f"   Command failed: {e.stderr}")

    print("\n--- Subprocess Module Example Finished ---")

if __name__ == "__main__":
    run_subprocess_example()