drupal-security
===============

This document is meant to be a living guide for setting up and running secure
Drupal websites.

This represents current best practices and "not to do"s for administrating
servers and specifically drupal website.

How do I get a usable document?
-------------------------------

You will need to get a few things before being able to generate the documents:

* First, install sphinx, pygments, and alabaster. You can grab them through pip
  or, if available, your distro's repositories.
* Then, run the sphinx-build to generate the epub -> make epub
* A backup PDF version can be made available through online tools like http://www.epubconverter.com

If you have make installed, you can also run `make {format}` in the root of the
repository, for convenience.

If you want to develop, we recommend installing sphinx-autobuild, and running
`make livehtml`. You'll then have a server at http://localhost:8000/ with live
reloads.

Can I help?
-----------

**YES!**, we'd like to get your thoughts, concerns, comments. If you have an 
improvements submit a PR or a patch!
