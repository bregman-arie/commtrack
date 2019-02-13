#!/bin/bash
# Until I'll have proper tests written in Python, a bunch of commtrack commands
# can also be helpful :D

echo "commtrack"
read k
commtrack

# Non-existing conf file
echo "commtrack -f bla"
read k
commtrack -f bla
