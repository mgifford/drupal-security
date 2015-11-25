Drupal Security
===============

This document is meant to be a living guide for setting up and running secure
Drupal websites. You can find it in an ePub or PDF version from:
  http://openconcept.ca/drupal-security-guide

This represents many of the current best practices and "not to do"s for 
administrating servers and specifically drupal websites.

We wanted a document that was easy to maintain, was text-based so that
it would be easier to maintain with Git, capable of producing complex
documents in an ePub or PDF format.

This led us to choose Sphinx which leverages reStructuredText and converts it 
to an ePub format:
	http://sphinx-doc.org/

Although generating a PDF is pretty easy these days, we wanted to default to 
ePub because it produces more accessible files by default.

Editing the Text
----------------

One of the advantages of reStructuredText is that you don't need anything other 
than a text editor to contribute to it.  If there are changes you would like to
see in the text, you can make them by editing the files in the /src/ directory. 
All of the *rst files are mostly text. 

More information about reStructuredText is available from:
	http://sphinx-doc.org/rest.html 

However this is just another text based markup that it similar to MarkDown. The
files should be easy enough to read that if you want to make a text change, you
really shouldn't need to learn anything. GitHub makes it pretty easy to suggest
changes directly through their website too which is sweet.

How do I get a usable document?
-------------------------------

You will need to get a few things before being able to generate the documents:

* First, install sphinx, pygments, and alabaster. You can grab them through pip
  or, if available, your distro's repositories. http://sphinx-doc.org/install.html
* When it is all installed you can use sphinx to generate the ePub by running the
  following command from the root of the repository:
		make epub
* Look for the results within the /build/epub directory and view the .epub results 
  with your favourite ePub reader.
* ePubs are just just encapsulated HTML, so the HTML files are available in that 
  directory and you can view them with a browser.
* The fastest way to make a PDF version at the moment is through online tools like
  http://www.epubconverter.com

If you want to develop, we recommend installing sphinx-autobuild, and running
`make livehtml`. You'll then have a server at http://localhost:8000/ with live
reloads.

Can I help?
-----------

**YES!** We'd like to get your thoughts, concerns, comments. If you have an 
improvement submit a comment, a pull request or a patch! 
