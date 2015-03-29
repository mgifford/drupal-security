L) Points of Debate
===================

1) Security by Obscurity
------------------------

There is a bit of a division within the security community as to whether one
should expose information about what versions of software are being used.

Make it Obscure
~~~~~~~~~~~~~~~

Leaving a :file:`CHANGELOG.txt` file visible does nothing to improve security,
rather it only helps inform an attacker how to focus their research efforts to
find a zero day attack, a contrib module vulnerability even faster, or just
disable any scripted attacks that aren't relevant to your stack. Justin C. Klein
Keane, in his blog Open Source Software Security, strongly recommends `hiding
both the Drupal and server identification`_.

Make it Transparent
~~~~~~~~~~~~~~~~~~~

In many cases where the :file:`CHANGELOG.txt` has been removed, it is because
the webmaster hasn't done a Drupal core upgrade and they are looking for a way
to obscure that fact. By keeping the :file:`CHANGELOG.txt` up-to-date at the
very least it indicates that someone is paying attention to security updates.
There are `easy ways to fingerprint Drupal`_ and the security team could hide
access to this file in the .htaccess file that comes with Drupal core if they
were concerned. By making it transparent, there is an additional reason for
developers to make it a priority to upgrade core when there is a security
release.

Be Consistent
~~~~~~~~~~~~~

While there is some discussion on the benefits of hiding :file:`CHANGELOG.txt`
there is agreement that when security releases are announced, that developers
must apply them quickly so that the site cannot be compromised. By default, the
Linux distribution, Apache and PHP also announce information that can be turned
off in their configuration files. It is good to be consistent and have your
reasoning documented so that it is clearly understood.

.. _hiding both the Drupal and server identification: http://www.madirish.net/242
.. _easy ways to fingerprint Drupal: https://drupal.org/comment/3481992#comment-3481992

