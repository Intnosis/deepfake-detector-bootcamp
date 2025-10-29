from pathlib import Path
from PIL import Image
import csv

def find_files(base, exts, recursive=True):
    base = Path(base)
    files = base.rglob("*") if recursive else base.glob("*")
    return[f for f in files if f.is_file() and f.suffix.lower() in exts]
def get_info(path):
    path = Path(path)
    
    try:
        with Image.open(path) as img:
            fmt = img.format
            mode = img.mode
            width, height = img.size
            avg = img.convert("RGB").resize((50,50)).getdata()
            
            r = sum(p[0] for p in avg) // ((50 * 50))
            g = sum(p[1] for p in avg) // ((50 * 50))
            b = sum(p[2] for p in avg) // ((50 * 50))
            
            avg_color = (r, g, b)
        size = path.stat().st_size
        return {'path': str(path), 
                'size': size, 
                'format': fmt, 
                'mode': mode, 
                'width': width, 
                'height': height, 
                'average': avg_color}
            
    except Exception as e:
        print(f"Warning image average cannot be found! {path} -> {e}")
        return {'path': str(path), 
                'size': path.stat().st_size, 
                'format': None, 
                'mode': None, 
                'width': None, 
                'height': None, 
                'average': None}
    
if __name__=="__main__":
    exts = {".jpg", ".png"}
    files = find_files("sample", exts, recursive=True)
    rows = [get_info (f) for f in files]
    for r in rows:
        print(r)