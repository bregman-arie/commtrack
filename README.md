# Commtrack

Tracking commits was never easier.

<div align="center"><img src="./docs/commtrack_example.png" alt="commtrack example" width="400"></div><hr />

## Installation

```
git clone https://github.com/bregman-arie/commtrack.git
cd commtrack
pipenv install -e .
```

## Usage

Search for commit 2142:

    commtrack -c 2142

Search for change ID in OpenStack Gerrit:

    commtrack --changeid t3gq2 --links openstack_gerrit

Search using the change subject

    commtrack --subject "Fix smb 2.1.6"

## Supported Type of Links

Type | Description
:------:|:--------:
Gerrit | Code Review System
Git | Version Control System
Dist-Git | Packaging repo (Located in a git system)
Repository | A collection of packages :)


## User Guide

Would like to learn more about Commtrack? Click [here](docs/user_guide.md)

## Developer Guide

Would like to assist with Commtrack development? Click [here](docs/developer_guide.md)
