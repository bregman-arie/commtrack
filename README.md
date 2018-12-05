# Commtrack

Tracking commits was never easier.


## Usage

```
# Search for comit 2142

commtrack -c 2142

# Search for change ID in OpenStack Gerrit:

commtrack --changeid t3gq2 --links openstack
```

## Configuration

There is a sample configuration in `samples` directory.
You have to specify the chain (where to look and in what order)
and each link in the chain has to be specified in a separate section

```
[DEFAULT]
links=openstack,my_repo

[gerrit]
openstack = review.openstack.org

[repository]
my_repo = http://my_server/repo
```

## How it works?

Commtrack is looking for the specified change in what is known as the "Chain".
A chain is composed of links. A link can be one of the following supported types:

* Gerrit
* Git

## Predefined Links

Name | Type | Description
:------ |:------:|:--------:
openstack | Gerrit | OpenStack Gerrit


## Contributions

To contribute use pull requests.
To suggest an idea/improvement or report a bug, use project issues.
