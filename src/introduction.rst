A) Introduction
===============

Drupal 7 is a leading content management system in governments around the world.
It has been widely adopted by institutions around the world that are looking to
meet increasing demands for service, larger challenges with accessibility and
mobile requirements, and ever smaller budgets.

With governments increasingly targeted for cyber attacks, it is important that
they remain up to date with best practices so that personal information and
government assets are protected.

This guide provides an overview of important security principles, best practices
for basic security; plus extra steps to be considered, if budget allows. We have
provided, where possible, some detailed instructions. Managers should read
sections :doc:`principles` and :doc:`concerns`. System administrators will need
to focus on sections :doc:`server`, :doc:`web-server`, :doc:`php`,
:doc:`database`, :doc:`code`, :doc:`environments`, and :doc:`maintenance`.
Drupal developers can focus on section :doc:`drupal` and :doc:`code`, but should
be familiar with the impact of the other sections too.

It should be clear that not all of the steps outlined here will need to be taken
on all drupal sites. The principles should be followed but not all of the
security suggestions described will need to be followed by all organizations.
Each practice or tool should be carefully evaluated to understand the potential
costs, risks and benefits.

This document raises issues to consider before you procure a server and when you
first gain access to your server. It provides suggestions on what additional
software you can add to your site which can help improve its security. It also
highlights configuration options that you can apply to Apache, PHP and MySQL to
improve on the default settings. Finally we talk about things that you can do to
enhance Drupal security.

The code snippets which are included are not always a comprehensive guide, but
there are always links in the descriptive paragraph with more information which
you should consult before installing programs on your production server.
Section I has information on building secure modules and themes, but it is also
worth consulting the `community documentation on Drupal.org`_.

Because this document strongly recommends against the use of Microsoft Windows
servers for Drupal sites, Windows security will not be addressed.

Security cannot be just a buzzword, it is a `process`_. There needs to be clear
understanding about lines of responsibility and ultimately management needs to
provide the budget required to ensure that systems can be maintained and
regularly re-evaluated.

Eternal vigilance is important as those searching for your vulnerabilities are
working around the clock and are well-financed. This document will, itself, need
to evolve to keep pace with new vulnerabilities.

.. _community documentation on Drupal.org: https://drupal.org/writing-secure-code
.. _process: https://www.schneier.com/essays/archives/2000/04/the_process_of_secur.html
