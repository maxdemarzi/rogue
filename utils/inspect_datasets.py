import os
import glob
import pandas as pd

data_dir = '/home/maxdemarzi/rogue/data'
dirs = sorted(os.listdir(data_dir))

report = []

for d in dirs:
    d_path = os.path.join(data_dir, d)
    if not os.path.isdir(d_path):
        continue
    # Find all CSV or Excel files
    files = glob.glob(os.path.join(d_path, '*.csv')) + glob.glob(os.path.join(d_path, '*.xlsx'))
    if not files:
        # Check subdirectories (e.g. ohlcv has subdirs)
        files = glob.glob(os.path.join(d_path, '**/*.csv'), recursive=True) + glob.glob(os.path.join(d_path, '**/*.xlsx'), recursive=True)
    
    if files:
        first_file = files[0]
        ext = os.path.splitext(first_file)[1].lower()
        rel_path = os.path.relpath(first_file, data_dir)
        try:
            if ext == '.csv':
                df = pd.read_csv(first_file, nrows=5)
            elif ext == '.xlsx':
                df = pd.read_excel(first_file, nrows=5)
            else:
                df = None
            
            if df is not None:
                report.append({
                    'dataset': d,
                    'file': rel_path,
                    'columns': list(df.columns),
                    'shape_cols': df.shape[1]
                })
            else:
                report.append({
                    'dataset': d,
                    'file': rel_path,
                    'error': 'Unsupported file type'
                })
        except Exception as e:
            report.append({
                'dataset': d,
                'file': rel_path,
                'error': str(e)
            })
    else:
        report.append({
            'dataset': d,
            'file': 'No files found'
        })

for r in report:
    print(f"\n--- Dataset: {r['dataset']} ---")
    if 'error' in r:
        print(f"  Error reading {r['file']}: {r['error']}")
    elif r['file'] == 'No files found':
        print("  No files found")
    else:
        print(f"  File: {r['file']}")
        print(f"  Columns ({r['shape_cols']}): {r['columns'][:10]}")
