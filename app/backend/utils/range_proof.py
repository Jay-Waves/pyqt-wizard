class range_proof:
    def __init__():
        return 
    
    def log_handler(self):
        # deserialize the output of backend
        return

    def container(self):
        # subprocess of backend
        return 

import re
import time
import subprocess

pattern = re.compile(
    r'\((enter|leave)\)\s+(.*?)\s+\[\s*(.*?)\s*\]\s+\((.*?)\s+from start\)'
)


process = subprocess.Popen(
    './test_fri', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
)


stack = 0
while True:
    output = process.stdout.readline()
    
    if output == '' and process.poll() is not None:
        break
    
    if output:
        match = pattern.match(output.strip())
        if match:
            execution_status = match.group(1)
            module_name = match.group(2)
            single_module_execution_time = match.group(3)
            total_execution_time = match.group(4)
            
            if execution_status == 'enter':
                print(" "*stack, f"begin: {module_name}")
                stack += 2
            else:
                stack -= 2
                print(" "*stack, f"finish: {module_name}, after {single_module_execution_time}")
        # time.sleep(1)
    

rc = process.poll()
print(f"Program exited with code {rc}")
print(f"Total Execution Time: {total_execution_time}")
