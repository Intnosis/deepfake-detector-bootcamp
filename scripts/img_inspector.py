from pathlib import Path
from PIL import Image
import csv
from collections import defaultdict
import argparse

def find_files(base, exts, recursive=False):
    base = Path(base)
    file = base.rglob('*') if recursive else base.glob('*')
    return  [f for f in file if f.is_file() and f.suffix.lower() in exts]

def inspect_image(path):
    path = Path(path)
    
    try:
        with Image.open(path) as img:
            fmt = img.format
            mode = img.mode
            weight, height = img.size
            rgb = img.convert('RGB').resize((50,50)).getdata()
            
            r = sum(p[0] for p in rgb) // (50 * 50)
            g = sum(p[1] for p in rgb) // (50 *50)
            b = sum(p[2] for p in rgb) // (50 *50)
            
            avg_color = (r, g, b)
            size = path.stat().st_size

            return {'path': str(path),
                    'size': size,
                    'format': fmt,
                    'mode': mode,
                    'weight': weight,
                    'height': height,
                    'average': avg_color}
    
    except Exception as e:
        print(f'Warning an error occur! {path} -> {e}')
        return {'path': str(path),
                'size': path.stat().st_size,
                'format': None,
                'mode': None,
                'weight': None,
                'height': None,              
                'average': None
        }

def write_csv(rows, outpath):
    fieldnames=['path', 'size', 'weight', 'height', 'format', 'mode', 'average']
    
    with open(outpath, 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        writer.writeheader()
        writer.writerows(rows)

        
def main():
    parser = argparse.ArgumentParser(description = "Image report generator")
    parser.add_argument('path', nargs="?", default=".", help="Base folder path")
    parser.add_argument('-r', '--recursive', action='store_true', help='Search Subfolders')
    parser.add_argument('-e', '--exts', default='.jpg,.png', help='Extension comma-separated')
    parser.add_argument('--combined', help='Output of CSV')
    args = parser.parse_args()

    exts = {f".{ext.strip().lower()}" for ext in args.exts.split(",")}
    files  = find_files(args.path, exts, args.recursive)
    
    groups = defaultdict(list)
    
    for f in files:
        groups[f.parent].append(inspect_image(f))
        
    for parent, rows in groups.items():
        out = parent / "images_report.csv"
        print(f'Writing {len(rows)} to {out}') 
        write_csv(rows,out)
        
    if args.combined:
        combined = []
        
        for rows in groups.values():
            combined.extend(rows)
        print('Writng combined:', args.combined)
        write_csv(combined, args.combined)

if __name__=="__main__":
    main()