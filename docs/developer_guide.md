# Commtrack - Developer Guide

The guide is written in Q&A format


## How to add a new type of link?

Links, when not used in context of a chain, known as sources.
Each type of source is defined in `commtrack/sources` in its own directory.

## What method a source class must define?

`search` method - this is the method that performs the
                  query and and returns the result accordingly.
