from pathlib import Path
from PIL import Image
import argparse
import csv

def get_info_image(file_path):
    try:
        with Image.open(file_path) as img:
            width, height = img.size
        size = file_path.stat().st_size
        return{"path": str(file_path), 'size': size, 'width': width, 'height': height}
    except Exception:
        print(f"Warning could not read dimention for file {file_path}") 
        return {"path": str(file_path), "size": file_path.stat().st_size, "width": None, "height": None}

def find_files(base, exst, recursive=False):
    base = Path(base)
    
    if recursive:
        files = base.globe("*")
    else: 
        files = base.glob("*")
    return[f for f in files if f.suffix.lower() in exst and f.is_file()] 

def main():
    parser = argparse.ArgumentParser(description = "Image report generator") 
    parser.add_argument('path',nargs="?", default=".", help="Base folder path")
    parser.add_argument("-r",'--recursive', action='store_true', help= 'Search subfolders')
    parser.add_argument('-e','--exst', default='.jpg,png', help='Extension comma separated')
    parser.add_argument('--csv', default="out.cvs", help="CVS output filename")
    
    args = parser.parse_args()
    exst = {f".{ext.strip().lower()}" for ext in args.exst.split(",")} 
    
    print(f"Searching in: {args.path}")
    print(f"Extension: {exst}")
    print(f'Recursive: {args.recursive}')
    print(f"Output CSV: {args.csv}")
    
    files = find_files(args.path, exst, args.recursive)
    print(f"Found {len (files)} matching files")

    data = [get_info_image(f) for f in files]
    
    with open(args.csv, "w", newline="")as f:

        writer = csv.DictWriter(f, fieldnames=['path', 'size', 'width', 'height']) 
        writer.writeheader()
        writer.writerows(data)
        
    print(f"CSV report save as {args.csv}")
    
if __name__== "__main__":
    main()