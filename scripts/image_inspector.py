from pathlib import Path
from PIL import Image
import argparse
import csv

def list_files(base".", recursive=False, exts={'.jpg', '.png'}):
    base = Path(base)
    files = 