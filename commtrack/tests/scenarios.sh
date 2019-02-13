#!/bin/bash
# Until I'll have proper tests written in Python, a bunch of commtrack commands
# can also be helpful :D

echo "> commtrack"
read k
commtrack

# Non-existing conf file
echo "> commtrack -f bla"
read k
commtrack -f bla

# Bad chain file - missing link
echo "> commtrack -f commtrack/tests/chain_files/missing_link"
read k
commtrack -f commtrack/tests/chain_files/missing_link

# Builtin link & made up changeid
echo "> commtrack --links openstack_gerrit --changeid 12ja"
read k
commtrack --links openstack_gerrit --changeid 12ja

# Normal execution
echo ">commtrack --changeid I32e76a83443dd8e7d79b396499747f29b4762e92"
read k
commtrack --changeid I32e76a83443dd8e7d79b396499747f29b4762e92
