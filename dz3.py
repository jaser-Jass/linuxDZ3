import subprocess
import pytest
import os
import time

def run_command_and_check_output(command, text):
    try:
       
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        
        
        if result.returncode == 0:
        
            return text in result.stdout
        else:
            return False
    except Exception as e:
        print(f"Error executing command: {e}")
        return False
@pytest.fixture(autouse=True)
def log_statistics():
   
    with open('stat.txt', 'a') as f:
        
        with open('/proc/loadavg', 'r') as loadavg_file:
            loadavg = loadavg_file.read().strip()
        
       
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
       
        try:
            with open('config.txt', 'r') as config_file:
                config_data = config_file.readlines()
                number_of_files = len(config_data)  
                file_size = os.path.getsize(config_data[0].strip()) if config_data else 0  
        except FileNotFoundError:
            number_of_files = 0
            file_size = 0
        f.write(f"{current_time}, {number_of_files}, {file_size}, {loadavg}n")

def test_run_command():
    result = run_command_and_check_output('echo Hello World', 'Hello')
    assert result == True

def test_run_command_failure():
    result = run_command_and_check_output('ls non_existent_file', 'Hello')
    assert result == False 
