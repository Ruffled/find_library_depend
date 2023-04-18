#!/bin/sh
echo "generate dynamic list"
find . -executable | xargs file | grep EABI.*SYSV.*dynamic | sed 's/:.*//' > /tmp/dynamic_list 2>/dev/null
echo "generate depend list"
cat /tmp/dynamic_list | xargs readelf -d | grep NEEDED | sort -u | sed -e 's/.*\[//' -e 's/\].*//' > /tmp/depended_libs 2>/dev/null
echo "look for dependent files"
cat /tmp/depended_libs | while read LL; do LLL=$(find . -name $LL); if [ -z "$LLL" ]; then echo $LL appears to be missing; fi; done 2>/dev/null
echo "done"
