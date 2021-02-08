import os,subprocess,os.path

for d in os.scandir('data'):
    if not d.is_dir(): continue
    subprocess.run([
        'python',
        'cep_estimatory.py',
        'data/%s/latest.csv' % d.name,
        '--output-folder',
        'dist/static/%s/' % d.name
    ])

