import subprocess
import sys
import yaml
from pathlib import Path

MODELS = [
    # "gpt-4o",
    # "gpt-4o-mini",
    # "gpt-5",
    # "deepseek-chat",
    "deepseek-reasoner",
]

STRICTNESS_LEVELS = [
    "default",
    "hard",
    "soft",
]

PARAMS_FILE = Path(__file__).parent / "params.yaml"

def update_params(model: str, strictness: str):
    """Update params.yaml with specified model and strictness."""
    with open(PARAMS_FILE, 'r') as f:
        params = yaml.safe_load(f)
    
    params['params']['models']['model'] = model
    params['params']['prompts']['strictness'] = strictness
    
    with open(PARAMS_FILE, 'w') as f:
        yaml.dump(params, f, default_flow_style=False, sort_keys=False)

def run_pipeline(model: str, strictness: str):
    """Run DVC pipeline with specified model and strictness."""
    print(f"\n{'='*80}")
    print(f"Running pipeline: model={model}, strictness={strictness}")
    print(f"{'='*80}\n")
    
    # Update params.yaml
    update_params(model, strictness)
    
    # Run DVC pipeline
    cmd = ["dvc", "repro", "-f"]
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode != 0:
        print(f"ERROR: Pipeline failed for model={model}, strictness={strictness}", file=sys.stderr)
        return False
    
    print(f"\n✓ Completed: model={model}, strictness={strictness}\n")
    return True

def main():
    """Run pipeline for all model and strictness combinations."""
    total = len(MODELS) * len(STRICTNESS_LEVELS)
    current = 0
    failed = []
    
    print(f"Running pipeline for {total} combinations ({len(MODELS)} models × {len(STRICTNESS_LEVELS)} strictness levels)")
    
    for model in MODELS:
        for strictness in STRICTNESS_LEVELS:
            current += 1
            print(f"\n[{current}/{total}] Processing: {model} with {strictness} strictness")
            
            success = run_pipeline(model, strictness)
            if not success:
                failed.append((model, strictness))
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total runs: {total}")
    print(f"Successful: {total - len(failed)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed combinations:")
        for model, strictness in failed:
            print(f"  - {model} with {strictness}")
        sys.exit(1)
    else:
        print("\n✓ All pipelines completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
