from preprocessing.text_extraction import *
from glob import glob
from tqdm import tqdm
import subprocess


filenames = glob('/home/karolis/Development/hackaburg2018_data/**/*.*')

print('Found', len(filenames), 'files.')

errors = 0
for filename in tqdm(filenames):
    try:
        t = extract_text(filename)
        if t is None or len(t) == 0:
            errors += 1
    except Exception as e:
        errors += 1
        print('Error extracting', filename, ':', e)

print(errors, 'extraction errors')

# TODO: figure out how to prevent these files from getting created in the first place
subprocess.run('rm pict*.*', shell=True)
