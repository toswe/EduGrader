"""
Analyzes correlation between professor grading and LLM grading scores.

Reads CSV files containing professor_score and llm_score columns, calculates
Pearson correlation, RMSE, averages, and other statistics to evaluate how well
the automated grading system matches human professor grading.

Usage: python calculate_correlations.py <dataset_name>
"""
import os
import sys
import pandas as pd
from scipy.stats import pearsonr

# Get dataset name from command line argument
if len(sys.argv) < 2:
    print("Usage: python calculate_correlations.py <dataset_name>")
    sys.exit(1)

dataset_name = sys.argv[1]
RESULTS_DIR = f'data/{dataset_name}/results/'
OUTPUT_CSV = f'data/{dataset_name}/correlation_results.csv'

results = []

for filename in os.listdir(RESULTS_DIR):
    if filename.endswith('.csv'):
        filepath = os.path.join(RESULTS_DIR, filename)
        try:
            df = pd.read_csv(filepath)
            if 'professor_score' in df.columns and 'llm_score' in df.columns:
                prof_scores = df['professor_score'].dropna()
                llm_scores = df['llm_score'].dropna()
                # Scale LLM scores from 0-100 to 0-10
                llm_scores = llm_scores / 10.0
                # Align indices in case of missing values
                valid = prof_scores.index.intersection(llm_scores.index)
                prof_scores = prof_scores.loc[valid]
                llm_scores = llm_scores.loc[valid]
                if len(prof_scores) > 1:
                    corr, _ = pearsonr(prof_scores, llm_scores)
                    rmse = ((prof_scores - llm_scores) ** 2).mean() ** 0.5
                    stddev_prof = prof_scores.std()
                    rmse_std_ratio = rmse / stddev_prof if stddev_prof != 0 else float('nan')
                else:
                    corr = float('nan')
                    rmse = float('nan')
                    stddev_prof = float('nan')
                    rmse_std_ratio = float('nan')
                avg_prof = prof_scores.mean()
                avg_llm = llm_scores.mean()
                avg_ratio = avg_llm / avg_prof if avg_prof != 0 else float('nan')
                results.append({
                    'filename': filename,
                    'correlation': corr,
                    'average_professor_score': avg_prof,
                    'average_llm_score': avg_llm,
                    'average_score_ratio': avg_ratio,
                    'rmse': rmse,
                    'professor_stddev': stddev_prof,
                    'rmse_stddev_ratio': rmse_std_ratio
                })
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_CSV, index=False)
print(f"Results saved to {OUTPUT_CSV}")
