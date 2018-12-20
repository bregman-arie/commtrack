# Commtrack - User Guide


## Usage

```
# Search for comit 2142

commtrack -c 2142

# Search for change ID in OpenStack Gerrit:

commtrack --changeid t3gq2 --links openstack_gerrit
```

## Configuration

Note: There is a sample configuration in `samples` directory.

Every chain file should include two entries:

`chain` - This tells commtrack where to look for your change and in what order.
`links` - This describes the places where commtrack should use.

Note: You don't have to specify links if you are using only commtrack built-in
      links.

```
chain: 'openstack'
links:
  gerrit:
    some_gerrit:
      address: 'a.b.com'
  git:
    my_git:
      address: 'x.y.com'
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
openstack_gerrit | Gerrit | OpenStack Gerrit
gerrithub | Gerrit | GerritHub

## Plugins

A plugin is responsible for adjusting commtrack to your environment.
For example:

* Mapping branch names from one to another system
* Save pre and post functions

Default plugin is OpenStack.

## Feedback

Got feedback for me? Great! Open project issue :)
