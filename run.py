import subprocess
import os

def run_azure_function():
    subprocess.run(["func", "start"], check=True)

if __name__ == "__main__":
    run_azure_function()
