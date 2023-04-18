# find_library_depend
Find dynamically linked library dependencies in Linux

This is intended to check that cross compiled embedded systems have all the required dynamic libraries present.
This can be run on the build host from the root of the build tree, or on the target from /

There is a working version in shell and a partial verison in python.
The python is much faster. You need to pip install python-magic for it to work.
