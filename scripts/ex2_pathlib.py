from pathlib import Path

def folder_file_path(folder: str ='sample'):
    folders = Path(folder)
    
    if not folders.exists():
        print("Folder doesn't exist")
        return
    
    print('folder',folders.resolve())
    
    for file in folders.iterdir():
        if file.is_file():
            sizeinbytes = file.stat().st_size
            print(file.name, '->', sizeinbytes, 'bytes')
            
if __name__ == "__main__":
    folder_file_path('sample')