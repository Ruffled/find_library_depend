#!/bin/sh
echo "generate dynamic list"
find . -executable 2>/dev/null | xargs file | grep EABI.*SYSV.*dynamic | sed 's/:.*//' > /tmp/dynamic_list
echo "generate depend list"
cat /tmp/dynamic_list | xargs readelf -d | grep NEEDED | sort -u | sed -e 's/.*\[//' -e 's/\].*//' > /tmp/depended_libs
echo "look for dependent files"
cat /tmp/depended_libs | while read LL; do LLL=$(find . -name $LL 2>/dev/null); if [ -z "$LLL" ]; then echo $LL appears to be missing; fi; done
echo "done"
