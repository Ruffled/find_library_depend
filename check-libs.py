#!/usr/bin/python3

# Find out what libraries are required by executables in a path.

# find * -type f | xargs file | grep EABI.*SYSV.*dynamic | sed 's/:.*//' > ../dynamic_list
# cat ../dynamic_list | xarfs readelf -d | grep NEEDED | sort -u | sed -e 's/.*\[//' -e 's/\].*//' | while read LL
# do
# LLL=$(find . -name $LL);
# if [ -z "$LLL" ]
# then echo $LL appears to be missing
# fi
# done

from os import walk as Walk
from os import path as Path
import magic
import subprocess

depends={}
depend_cnt=0

def check_dynamic(fpath):
    try:
        ftype_string = magic.from_file(fpath)

    except Exception as e:
        # print('magic failed: ', e)
        return False

    for check in ['ARM', 'EABI5', '(SYSV)', 'dynamically linked']:
        if check not in ftype_string:
            return False

    return True

def check_depends(fpath):
    global depend_cnt
    cmd = [ '/usr/bin/readelf', '-d', fpath ]

    completed = subprocess.run(cmd, capture_output=True)
    # print(completed)
    if completed.returncode == 0:
        string = completed.stdout.decode('utf-8')
        # print(string)
        for elem in string.splitlines():
            # print(elem)
            if 'NEEDED' in elem:
                needed = elem.split()[-1]
                needed = needed[1:-1]
                # print(needed)
                if needed not in depends:
                    depends[needed] = []
                    depend_cnt = depend_cnt + 1
                if fpath not in depends[needed]:
                    depends[needed].append(fpath)

for root, dirs, files in Walk(".", topdown=False):
    for name in files:
        fpath = Path.join(root, name)
        if check_dynamic(fpath):
            # print (fpath, 'is dynamic binary exec or lib')
            # Maybe use pyelftools ???
            check_depends(fpath)
            # print(depends)

print(depends.keys())
