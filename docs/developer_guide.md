# Commtrack - Developer Guide

The guide is written in Q&A format


## How to add a new type of link?

Links should be added to `commtrack/links`.
Each new type of link should inherit from Link class (which is defined in `commtrack/link.py`)

Any other related link modules are usually added to a directory named as the link itself.
For example: there is `commtrack/gerrit/` directory which holds information on gerrit exceptions,
constants, etc. The link itself is defined in `commtrack/links/gerrit.py`


## How to contribute?

To contribute use pull requests.
