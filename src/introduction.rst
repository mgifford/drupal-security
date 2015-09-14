A) Introduction
===============

Drupal is a leading Content Management System (CMS) in many institutions around 
the world. 

Governments are increasingly a target for cyber attacks, and yet the security 
culture is slow to change. Keeping up-to-date on best practices is critical to 
protect personal information and government assets. 

This guide provides an overview of the principles, best practices and next steps 
in securing your Drupal site. We have provided, where possible, some detailed 
instructions. Managers should read sections :doc:`principles` and :doc:`concerns`. 
System administrators will need to focus on sections :doc:`server`, :doc:`web-server`, 
:doc:`php`, :doc:`database`, :doc:`code`, :doc:`environments`, and :doc:`maintenance`.
Drupal developers can focus on section :doc:`drupal` and :doc:`code`, but should
be familiar with the impact of the other sections too.

It should be clear that not all of the steps outlined here will need to be taken
on all Drupal sites. The principles should be followed but not all of the
security suggestions described will need to be followed by all organizations.
Each practice or tool should be carefully evaluated to understand the potential
costs, risks and benefits.

This document raises issues to consider before you procure a server and especially 
when you first gain access to your server. It provides suggestions on what additional
software you can add to your site which can help improve its security. It also
highlights configuration options that you can apply to Apache, PHP and MySQL to
improve on the default settings. Finally we talk about things that you can do to
enhance Drupal security.

The code snippets which are included are not always a comprehensive guide, but
there are always links in the descriptive paragraph with more information which
you should consult before installing programs on your production server.
It is always worth consulting the `community documentation on Drupal.org`_.

Because this document strongly recommends against the use of Microsoft Windows
servers for Drupal sites, Windows security will not be addressed.

Security cannot be just a buzzword, it is a process that needs to be ingrained 
in the culture of an organization. There needs to be a clear understanding about 
lines of responsibility and ultimately management needs to provide the budget 
required to ensure that systems can be maintained and regularly re-evaluated.

Eternal vigilance is important as those searching for your vulnerabilities are
working around the clock and are well-financed. This document will, itself, need
to evolve to keep pace with new vulnerabilities.

.. _community documentation on Drupal.org: https://drupal.org/writing-secure-code
