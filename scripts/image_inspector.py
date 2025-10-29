from pathlib import Path
from PIL import Image
def list_file(base=".", recursive=False, exts={".jpg", ".png"}):
    base = Path(base)
    file = base.rglob('*') if recursive else base.glob('*')
    return[f for f in file if f.is_file() and f.suffix.lower() in exts]

def  get_basic_info(path):
    path = Path(path)
    try:
        with Image.open(path) as img:
            fmt = img.format
            mode = img.mode
            width, height = img.size
        size = path.stat().st_size
        return {'path': str(path), 'size': size, 'format': fmt, 'mode': mode, 'width': width, 'height': height}
    except Exception:
        print("Warning image cannot read",path)
        return{'path': str(path), 'size': path.stat().st_size, 'format': None, 'mode': None, 'width': None, 'height': None}

def average_color(path, thumb_size=(100,100)):
    try: 
        with Image.open(path) as img:
            rgb = img.convert("RGB")
            rgb.thumbnail(thumb_size)
            pixels = list(rgb.getdata())    
            if not pixels:
                return None
            r = sum(p[0] for p in pixels) // len(pixels)
            g = sum(p[1] for p in pixels) // len(pixels)
            b = sum(p[2] for p in pixels) // len(pixels)
            return (r ,g, b)
    except Exception as e:
        print(f'Warning: cannot compute avrage color {path} -> {e}')
        return None
    
if __name__=="__main__":
    print(Path("sample/img.jpg").exists())  
    print(average_color('sample/img.jpg'))