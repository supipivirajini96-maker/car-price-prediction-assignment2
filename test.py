import os
import yaml

# Path to your experiment
experiment_path = "mlruns/1/runs"
target_run_id = "21ed4e080009440d912e76937fa5f5ac"

found = None

# Iterate over each run folder
for run_folder in os.listdir(experiment_path):
    artifacts_path = os.path.join(experiment_path, run_folder, "artifacts", "MLmodel")
    
    if not os.path.isfile(artifacts_path):
        continue  # skip if MLmodel not present
    
    with open(artifacts_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError:
            continue
    
    # Check if run_id matches
    if data.get("run_id") == target_run_id:
        found = os.path.join(experiment_path, run_folder)
        break

if found:
    print(f"✅ Found run folder for run_id {target_run_id}: {found}")
else:
    print(f"❌ Run_id {target_run_id} not found in MLmodel files")
