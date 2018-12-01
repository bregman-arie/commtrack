# Commtrack

Tracking commits was never easier...well, sort of :)


## Usage

```
commtrack 344a9956f9f2d055c96f3446ec03ef486294141b
```

## Configuration

There is a sample configuration in `samples` directory.
You have to specify the chain (where to look and in what order)
and each link in the chain has to be specified in a separate section

```
[DEFAULT]
links=openstack,my_repo

[Gerrit]
openstack = review.openstack.org

[Repository]

my_repo = http://my_server/repo
```

## How it works?

Commtrack is looking for the specified commit (or any other provided identifier)
in what is known as the "Chain". A chain is composed of links. A link can be one of
the following supported types:

* Gerrit

## Predefined Links

Name | Type | Description
:------ |:------:|:--------:
openstack | Gerrit | OpenStack Gerrit


## Contributions

To contribute use pull requests.
To suggest an idea/improvement or report a bug, use project issues.
