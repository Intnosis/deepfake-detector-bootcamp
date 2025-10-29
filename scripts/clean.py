from pathlib import Path
from PIL import Image
import csv
import argparse

def step_2():

    files = ['cat.jpg', 'dog.jpg', 'img.jpg', 'gif.gif', 'docs.pdf', 'win.docs', 'len.gif']

    clean_files = []

    seen = set()

    label = []
    
    row = []
    
    final_row = []
    
    for sample_files in files:
        normalized = sample_files.strip().lower()
        if not normalized.endswith('.jpg'):
            continue
        if normalized.startswith('.'):
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        clean_files.append(normalized)
    print(clean_files)
    

    for labels in clean_files:
        no_ext = labels.replace('.jpg', ' ')
        label1 = no_ext.rstrip('0123456789')
        label.append(label1)
        
    print(label)
    
    zipped = zip(clean_files, label)
    
    for filename, lbl in zipped:
        row1 = {'filename': filename, 'label': lbl}
        
        row.append(row1)
        print("Rows:",row)
    
    for i, r in enumerate(row, start=1):
        print(i, r)
        
        if i <= 2:
            split = 'train'
            
        elif i == 3:
            split = 'Test'
           
        else:
            split = 'Val' 
            
        

    new_row = {
        'id': i,
        'file': r['filename'],
        'label': r['label'],
        'split': split
                
        }
        
    final_row.append(new_row)
    print(final_row)

    return final_row
def validation_rows(rows):
    
    required_keys = {'id', 'filename', 'label', 'split'}
    allowed_split = {'train', 'val', 'test'}
    error = []
    
    if not isinstance(rows,list):
        print('Validation failed: expected a list of row')
        return False
    seen_filenames = {}
    seen_ids = set()

    for idx, row in enumerate(row, start=1):

        if isinstance(row,dict):
            error.append(f'Row {idx} is not a dict.')
            continue

        missing = required_keys - set(row,keys())
        if missing:
            error.append(f"Row {idx} missing keys: {sorted(list(missing))}")

        filename =row.get('filename')
        if not filename:
            error.append(f'Row {idx} has empty filename')
            
        if filename:
            seen_filenames.setdefault(filename, []).append(idx)
            
        split = row.get('split')
        if split is None or str(split).lower() not in allowed_splits:
            error.append(f'Row {idx} has invalid split: {split!r}')
            
        # id checks
        id_val = row.get('id')
        if not isinstance(id_val, int):
            error.append(f"Row {idx} id is not an integer: {id_val!r}")
        else:
            if id_val in seen_ids:
                error.append(f"Duplicate id found: {id_val}")
            seen_ids.add(id_val)

    # report duplicate filenames
    dup_files = {name: inds for name, inds in seen_filenames.items() if len(inds) > 1}
    if dup_files:
        for name, inds in dup_files.items():
            error.append(f"Duplicate filename '{name}' at rows {inds}")

    # final result
    if not error:
        print(f"Validation passed! {len(rows)} rows checked, no issues found.")
        return True
    else:
        print("Validation failed:")
        for e in error:
            print(" -", e)
        return False

def save_manifest(rows, path='manifest.csv'):
    """
    Save rows (list of dicts) to CSV using field order: ['id','filename','label','split']
    """
    fieldnames = ['id', 'filename', 'label', 'split']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved manifest to: {path}")

# Run pipeline
rows = step_2()
if validation_rows(rows):
    save_manifest(rows)
else:
    print("Fix the errors above before saving.")