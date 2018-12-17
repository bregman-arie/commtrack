# Commtrack

Tracking commits was never easier.


## Installation

```
cd commtrack
pipenv install -e .
```

## Usage

```
# Search for comit 2142

commtrack -c 2142

# Search for change ID in OpenStack Gerrit:

commtrack --changeid t3gq2 --links openstack
```

## Configuration

Note: There is a sample configuration in `samples` directory.

Every chain file should define `links`. This is tells commtrack
where to look for your commit and in what order.

Also, if a link is not pre-defined in commtrack, you have to specify
it in its own section based on its type (Gerrit, Git, ...)

```
[DEFAULT]
links=openstack,my_repo

[gerrit]
openstack = review.openstack.org

[repository]
my_repo = http://my_server/repo
```

The configuration file should be set in one of the following locations:

```
.chain
/etc/commtrack/chain
```

You can also pass it with `commtrack --conf` or `commtrack --chain`.

## How it works?

Commtrack is looking for the specified change in what is known as the "Chain".
A chain is composed out of links. A link can be one of the following supported types:

* Gerrit
* Git

## Predefined Links

Name | Type | Description
:------ |:------:|:--------:
openstack | Gerrit | OpenStack Gerrit


## Contributions

To contribute use pull requests.
To suggest an idea/improvement or report a bug, use project issues.
