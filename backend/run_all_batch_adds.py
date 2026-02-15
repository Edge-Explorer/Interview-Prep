import subprocess
import os

scripts = [
    'batch_add_round2.py',
    'batch_add_ai_companies.py',
    'batch_add_domain_expansion.py',
    'batch_add_domain_balancing.py',
    'batch_add_perfect_balance.py',
    'batch_add_round7.py',
    'batch_add_round8.py',
    'batch_add_companies.py'
]

backend_dir = r'c:\Users\ASUS\OneDrive\Desktop\Interview Prep\backend'

for script in scripts:
    script_path = os.path.join(backend_dir, script)
    if os.path.exists(script_path):
        print(f"Running {script}...")
        try:
            # Using yes to answer 'yes' to any overwrite prompts
            # On Windows, we can echo yes | python script.py
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            cmd = f'echo yes | python "{script_path}"'
            result = subprocess.run(cmd, shell=True, cwd=backend_dir, capture_output=True, text=True, env=env)
            # Use safe printing for Windows
            print(result.stdout.encode('ascii', 'ignore').decode('ascii'))
            if result.stderr:
                print(f"Errors in {script}:")
                print(result.stderr.encode('ascii', 'ignore').decode('ascii'))
        except Exception as e:
            print(f"Failed to run {script}: {e}")
    else:
        print(f"Script not found: {script}")

print("All scripts processed.")
