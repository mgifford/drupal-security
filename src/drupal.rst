H) Drupal
=========

.. highlight:: bash

.. image:: /_static/images/druplicon.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: Drupal icon

1) Files
--------

`Verify Drupal file permissions on the server`_. You really need to restrict
write access to the server and verify that the right users/groups have the
access that they need for Drupal to operate effectively. One can set all of
Drupal's files to be read only, only allowing for file uploads, cached files,
sessions and temporary directories with write permissions. The major limitation
of this approach is that it makes applying security upgrades more difficult.

By default, Drupal 7 disables execution of PHP in directories where you can
upload PHP. Check the :file:`.htaccess` file in the files directory. You can
also add this to your Apache Virtual Host to ensure that no handlers have been
overlooked.

.. code-block:: apache

 <Directory /var/www/drupal/sites/default/files/>
  # Important for security, prevents someone from
  # uploading a malicious .htaccess
  AllowOverride None
  SetHandler none
  SetHandler default-handler
  Options -ExecCGI
  php_flag engine off
  RemoveHandler .cgi .php .php3 .php4 .php5 .phtml .pl .py .pyc .pyo

  <Files *>
   AllowOverride None
   SetHandler none
   SetHandler default-handler
   Options -ExecCGI
   php_flag engine off
   RemoveHandler .cgi .php .php3 .php4 .php5 .phtml .pl .py .pyc .pyo
  </Files>
 </Directory>

Drupal needs to be able to write to the server to be able to perform certain
tasks like managing file uploads and compressing/caching CSS/JS files. Ensure
that Apache has write access to /tmp and also to the public sites folder:

::

 # Ubuntu/Debian:
 $ chown -R www-data:www-data sites/default/files

 # CentOS:
 $ chown -R nobody:nobody sites/default/files

Make sure that you are only allowing users to upload file types that have
limited security problems with them. Text and images are usually quite safe.
There have been some exploits on PDF files, but they are quite rare. Microsoft
Office documents should be scanned if they are going to be uploaded onto the
server.

`ClamAV`_ can be incorporated into Drupal to scan uploaded files for viruses and
other malicious code.  Acquia recommends excluding the following file types:
*flv*, *swf*, *exe*, *html*, *htm*, *php*, *phtml*, *py*, *js*, *vb*, *vbe*,
*vbs*.

2) Drush
--------

Drush is a command line shell and scripting interface for Drupal. We strongly
recommend using `Drush`_ on both staging and production servers because it
simplifies development and maintenance. Note that the version of Drush packaged
with your OS is likely to be extremely out of date.

It is recommended to install Drush with `Composer`_ (the dependency manager for 
PHP) but other options and details on the `Drush git page`_.

There is a `Security Check`_ module available for Drush which is a basic sanity
test for your configuration. When the module is added, you can run this against
your site from Apache's document root (docroot) on the command line using::

 $ drush secchk

As with the server configuration in general, document what you are using. Drush
makes this fairly straightforward as you can simply export a list from the
command line::

 $ drush pm-list --type=Module --status=enabled

Cron is the Linux time-based job scheduler and it is used for a lot of key
Drupal functions. Check to see that you are running cron several times a day.
For Drupal 7 and above, `if there is traffic to the site, cron jobs are run
every 3 hours`_. The status page will tell you when the last time cron was run
on the site. You may want to set up a Linux cron job using Drush if you
have either a low traffic site or have special requirements.

To run cron on all of your sites in /home/drupal - from the command line enter
``crontab -e`` and then insert::

 30 2,6,11,18 * * * cd /home/drupal && drush @sites core-cron -y > /dev/null

You will need developer modules to help you build your site, but they are a
security risk on your production site and need to be disabled. Many modules
(such as Views) have separate administration screens that can also be disabled
in a production environment. They are absolutely required when building the
site, but can be disabled when they are not in use. It is always a good practice
to see if there are any unnecessary modules that can be disabled on your site. This
also offers performance benefits. Views is an incredibly powerful query building
tool. Because of that, it is important that all Views have explicit access
permissions set at ``/admin/build/views`` .

3) Errors
---------

Check the Status Report and Watchdog pages regularly and resolve issues - Drupal
should be happy! This needs to be done regularly, even after launch. Remember
that you can more quickly scan your logs by filtering for PHP errors. With the
`Views Watchdog`_ module you could also build custom reports to display on your
website. On your production server, make sure to disable the display of PHP
errors. These should be recorded to your logs, but not visible to your visitors.
On your staging site you will want to see those errors to help you debug PHP
problems, but it is a potential vulnerability to have those exposed. This won't
catch all PHP errors however, and so it is also useful to review the error log
of the web server itself.

Watchdog is a good tool, but is `limited in a number of ways`_. Simply because
it is database dependent, even having a lot of 404 errors can affect
performance. Fortunately, logs can be easily directed to the server's syslog,
with the `Syslog Access`_ module, which also allows you to leverage your
favourite log management tool. The Drupal Handbook also has a great resource for
how to `send your logs to Syslog`_ with integrated logging.

4) Core and Contrib Hacks
-------------------------

Before launching your site (and periodically afterwards) it is useful to run the
`Hacked!`_ module to check what code differs from what was released on
Drupal.org. Particularly when the `diff`_ module is enabled, this is a powerful
tool to evaluate your code. There are millions of lines of code in a given
Drupal site, so Hacked! is a really valuable analysis tool. If you need to apply
patches against the stable released version of the code, the patch should be in
a clearly documented directory. It is unfortunately a common practice for less
experienced Drupal developers to cut corners and hack Drupal Core to provide some
functionality that is required. There are lots of reasons why this is a bad idea
and `why responsible developers don't hack core`_. For the purposes of this
document it is sufficient to say it makes it harder to secure. The `same is true
for contributed modules`_, you shouldn't have to alter the code to customize it
most of the time. The Hacked! module is very useful in identifying when modules
no longer are the same as their releases on Drupal.org. Being able to quickly
scan through hundreds of thousands of lines of code and find differences against
known releases is a huge security advantage.

You can also generate Drush make file from an existing Drupal site and then
recreate a clean copy of the codebase which you can then diff (a command line
comparison tool) to determine if your site has been hacked.

::

 $ drush generate-makefile make-file.make
 $ drush make make-file.make -y

It is recommended to run all modules you use through the `Coder`_ module, but
especially any custom built modules and themes. This module `can give you
suggestions`_ on how to follow the `Drupal communities coding standards`_.

It can also help you identify other coding errors that may affect your site.
Particularly when building custom modules the Coder module can help identify
`unsanitized user input`_, `SQL injection vulnerabilities`_ and `Cross Site
Request Forgery (CSRF)`_ problems. It is unfortunately quite common for
developers to extend Drupal by forking existing projects and not provide
enhancements back to the community. Doing this breaks assumptions within the
Update module but more importantly makes upgrades much more difficult. Even with
a properly documented patch, it is a lot of work to upgrade, patch and re-write
a function in a live website.

By contributing the improved code upstream, you can avoid that often painful
process. The peer review that comes with contributing your code back to the
community is a secondary benefit: your code base will become more robust because
more people will understand it. Your `bus factor`_ (the number of people who can
go missing from a project by either being hit by a bus or winning the lottery)
will increase by releasing your code. Publishing the code elsewhere forces you
to actually think about what is required. Further, if someone tries to install
your code/system, they might notice missing parts or for that matter parts that
might be confidential.

5) Administration
-----------------

Drupal has a very fine grained and customizable permissions model. In its
simplest form, users are assigned roles and each role is given permissions to
various functions. Take the time to review roles with access to any of
Administer filters, Administer users, Administer permissions, Administer content
types, Administer site, Administer configuration, Administer views and translate
interface. It is useful to review the permissions after upgrades to verify if
any new permissions have been added.

Don't use *admin*, *root*, or simple variations of those as your user/1 admin
name. It's the first ones that a cracker is going to try, so be a bit more
unique. Obscurity isn't the same as security, but no need to give them their
first guess when choosing user names. Another good practice with regards to
user/1 is to `completely disable the account`_. With the advent of Drupal 7 and
Drush, user/1 is not required to administer Drupal websites anymore, and thus
can be simply blocked. The account can be re-enabled as needed through Drush or
directly in the database.

As with other server user accounts, you will want to restrict who has access to
servers. Make sure to delete any test or developer accounts on the production
server.

Don't run Drupal without enabling the Update module that comes with core. Drupal
core and contributed modules use a structured release process that allows your
administrators to be proactively alerted when one of those modules has a
security release. Any piece of code is susceptible to a security issue, and
having a central repository that a Drupal site can compare against is key to the
security paradigm. Aside from the releases that have fixes for known security
problems, some modules (or a version of that module) may become unsupported.
This is also a security problem, in that you will not receive updates if there
are security problems that are identified with the module. The Update module
also allows you to get a weekly email if there are security upgrades that need 
to be applied.

Drupal's input filters are very powerful, but can provide a vulnerability. **Don't
enable the PHP filter** which is available in Drupal 7 Core. Installing the
`Paranoia`_ module can really help enforce this practice. The PHP filter makes
debugging more difficult and exposes your site to a greater risk than it is
worth. This module has been removed from Drupal 8, but is available as a 
contributed module. All PHP code should be written to the file system and not 
stored in the database. 

Another input filter that is problematic is Full HTML which should
only be granted to administrator roles. Anyone with the Full HTML filter can
craft malicious JavaScript and gain full admin access to any website on the same
domain as the Drupal website. If needed, you can add some additional tags to the
Filtered HTML input format but be cautious.

6) Modules to Consider
----------------------

There are `a lot of Drupal security modules`_. Depending on your needs you will
want to add more or less than those listed here.

`Automated Logout`_
  Provides the ability to log users out after a specified time of inactivity.

`Clear Password Field`_
  Stops forms from pre-populating a password.

`Drupal Tiny-IDS`_
  An alternative to a server-based intrusion detection service.

`Local Image Input Filter`_
  Avoids CSRF attacks through external image references.

`Login Security`_
  Set access control to restrict access to login forms by IP address.

`Paranoia`_
  Limits PHP functionality and other controls.

`Password Policy`_
  Enforces your user password policy.

`Session Limit`_
  Limits the number of simultaneous sessions per user.

`Settings Audit Log`_
  Logs who did what, when.

`Security Kit`_
  Hardens various pieces of Drupal.

`Secure Login`_
  Provides secure HTTPS access, without mixed-mode capability.

`HTTP Strict Transport Security`_
  To be used together with Secure Login, to prevent ssl strip attacks.
  Alternatively, directly `enforce it through web-server settings`_.

`Secure Pages`_
  Manages mixed-mode (HTTPS and HTTP) authenticated sessions for enhanced
  security (note required core patches).

`Secure Permissions`_
  Disables the UI to set/change file permissions.

`Security Review`_
  Produces a quick but useful review of your site's security configuration. 

`Shield`_
  Protects your non-production environment from being accessed.

`Restrict IP`_
  Restrict access to an administrator defined set of IP addresses.

`Username Enumeration Prevention`_
  Stop brute force attacks from leveraging discoverable usernames.

7) Modules to Avoid on Shared Servers
-------------------------------------

Many Drupal modules intended to help developers develop code also disclose
sensitive information about Drupal and/or the web-server, or allow users to
perform dangerous operations (e.g.: run arbitrary PHP code or trigger
long-running operations that could be used to deny service). These modules can
be used to debug locally (and many are essential tools for Drupal developers),
but should never be installed on a shared environment (e.g.: a production,
staging, or testing server).

To limit the damage a malicious user can do if they gain privileged access to
Drupal, it's not sufficient for a development module to be simply disabled: the
files that make up the module should be removed from the file-system altogether.
Doing so prevents a malicious user from enabling it and gaining more data about
the system than they would be able to otherwise. Note that it is difficult to
automatically enforce that these modules are not deployed to shared systems:
developers need to understand why they should not commit these modules and take
care to double-check what they're about to deploy.

Some popular development modules which should not be present on any shared
website include:

`Delete all`_
  This module allows someone with sufficient privileges to delete all content
  and users on a site.

`Devel`_
  Besides letting users run arbitrary PHP from any page, Devel can be configured
  to display backtraces, raw database queries and their results, display raw
  variables, and disable caching, among other things.

`Drupal for Firebug`_
  Drupal for Firebug outputs the contents of most variables, raw database
  queries and their results, display PHP source code, and can be used to run
  arbitrary PHP. Furthermore, it does all this by interfacing with browser
  developer tools, making it difficult to determine if this module is enabled by
  glancing at the site.

`Theme Developer`_
  This module, which depends on the Devel module mentioned earlier, is very
  useful for determining which theme files / functions are used to output a
  particular section of the site, but it displays raw variables and slows down
  the site significantly.

`Trace`_
  This module can be used to display backtraces and raw variables, among other
  things.

Note that most "normal" modules can be dangerous if a malicious user gains
privileged access to Drupal. You should evaluate each new module you install to
determine what it does and whether the features it brings are worth the risks.
Some modules to take into special consideration are:

`Backup and Migrate`_
  This module allows you to download a copy of the site's database. If
  restrictions placed upon you by your hosting provider prevents you from being
  able to make backups, this module will allow you to do so; but a malicious
  user with privileged access would be able to download a copy of the whole
  Drupal database, including usernames, passwords, and depending on your site,
  access keys to the services you use.

`Coder`_
  This module is very useful for ensuring your code conforms to coding standards
  but can be used to display the PHP that makes up modules.

8) Drupal Distributions
-----------------------

Drupal distributions provide turnkey installations that have been optimized for
specific purposes, generally with a curated selection of modules and settings.
There are now two distributions which have been specifically built for security,
`Guardr`_ and `Hardened Drupal`_. Guardr is built to follow the `CIA information
security triad`_: confidentiality, integrity and availability. It is worth
watching the evolution of these distributions and installing them from time to
time if only to have a comparison of modules and configuration options.

9) Choosing Modules & Themes
----------------------------

There are over 30,000 modules and 2,000 themes that have been contributed on 
Drupal.org.  Unfortunately, not all of these modules are stable and secure 
enough to install in a production environment. When choosing projects to 
incorporate into your site consider:

* How many reported installs are there?
* What was the date of the last stable release?
* When was the last code commit to the repository? 
* How many open bugs are there vs the total number of bugs?
* Do the maintainers also work on other projects? 
* Is the project description useful and include screenshots?
* What documentation is available?
* Is there a Drupal 8 stable or development release?
* How many maintainers are listed?
* Are translations available?

Note that these are just some issues to consider when choosing modules. 
Ultimately, having an experienced Drupal developer involved in a project is
important when reviewing which projects to adopt. 


10) Drupal Updates
------------------

Eventually, all software will need an update if it is going to continue to be 
useful. Most commonly they are feature releases and do not impact security. The 
available updates report will show you these when the Update manager is enabled. 
This report will also alert you when there are security updates available on 
projects that are enabled and hosted on Drupal.org. The `risk levels`_ that 
the Drupal community has adopted is now based on the `NIST Common Misuse Scoring System`_ 
and converted into the following text descriptions: Not Critical, Less Critical, 
Moderately Critical, Critical and Highly Critical.

Sometimes a maintainer does not have the time to put out a full release, so will 
produce a development release, or simply post the code to the Git repository on 
Drupal.org.  For now the Update manager does not have a means to track anything 
other than full stable releases. The Available update report will show you when 
a new release is available, but is geared to stable releases. Using your site 
uses modules hosted on GitHub or other repositories, you will not have the 
benefit of the security alerts made by through Drupal.org.

Sometimes a module simply doesn't have an active maintainer or the maintainer
is focused on the next major version of the code base. For instance, Drupal 6 is
still officially supported, but there are very few maintainers actively 
addressing issues in this older code base. In these instances, a stable release 
can be removed because officially nobody is maintaining it. By definition, 
unmaintained code is a security problem. 

Tools like `Drop Guard`_ are designed to make this easier for developers to keep 
track of.

11) The settings.php
--------------------

After the initial install, make sure that there is not write permission on the 
settings.php has been removed. 

In Drupal 7 you can set the Base URL which can be useful to block some phishing 
attempts:

 $base_url = 'http://www.example.com';

In Drupal 8, this is now defined in the Trusted hosts patern:

 $settings['trusted_host_patterns'] = array('^www\.example\.com$');
 
There should be a `salt`_ in the settings.php so that there is some extra random
data used when generating strings like one-time login links. This is added by
default in Drupal 7 and 8, but is stored in the the settings.php file. You can 
store this value outside of the web root though for extra security:

In Drupal 7:
 
 $drupal_hash_salt = file_get_contents('/home/example/salt.txt');

and Drupal 8:

 $settings['hash_salt'] = file_get_contents('/home/example/salt.txt');

Drupal 8 has added a $config_directories array which specifies the location of 
file system directories used for configuration data. 

    On install, "active" and "staging" directories are created for configuration. 
    The staging directory is used for configuration imports; the active directory 
    is not used by default, since the default storage for active configuration 
    is the database rather than the file system (this can be changed; see "Active configuration settings" below).

By default this is done within a randomly-named directory, however for extra
security, you can override these locations and put it outside of your document
root.

 $config_directories = array(
    CONFIG_ACTIVE_DIRECTORY => '/some/directory/outside/webroot',
    CONFIG_STAGING_DIRECTORY => '/another/directory/outside/webroot',
 );

12) Miscellaneous
-----------------

Review the discussion in Section K and decide if you are going to remove the
:file:`CHANGELOG.txt` file. Ensure that you can keep up security upgrades on a
weekly basis and **do not hack core**! If you plan to distribute your live site
so that you can do testing or development outside of a controlled environment,
consider building a `sanitized version of the database`_. This is especially
important if you have user information stored in the database. If absolutely all 
information on the site is public, this may not be necessary.

.. _Verify Drupal file permissions on the server: https://drupal.org/node/244924
.. _ClamAV: https://drupal.org/project/clamav
.. _Drush: https://github.com/drush-ops/drush
.. _PHP's PEAR: http://pear.php.net/
.. _Composer: https://getcomposer.org/doc/00-intro.md#system-requirements
.. _Drush git page: https://github.com/drush-ops/drush#installupdate---composer
.. _Security Check: https://drupal.org/project/security_check
.. _if there is traffic to the site, cron jobs are run every 3 hours: https://drupal.org/cron
.. _Views Watchdog: https://drupal.org/project/views_watchdog
.. _limited in a number of ways: http://www.asmallwebfirm.net/blogs/2013/04/achieving-drupal-log-bliss-splunk
.. _Syslog Access: https://drupal.org/project/syslog_access
.. _send your logs to Syslog: https://drupal.org/documentation/modules/syslog
.. _Hacked!: https://drupal.org/project/hacked
.. _diff: https://drupal.org/project/diff
.. _why responsible developers don't hack core: http://drupal.stackexchange.com/questions/59054/why-dont-we-hack-core
.. _same is true for contributed modules: http://www.bluespark.com/blog/youre-doing-it-wrong-dont-hack-drupal-core-change-text
.. _Coder: https://drupal.org/project/coder
.. _can give you suggestions: https://drupal.org/node/2135539
.. _Drupal communities coding standards: https://drupal.org/coding-standards
.. _unsanitized user input: https://drupal.org/node/101495
.. _SQL injection vulnerabilities: http://www.pixelite.co.nz/article/sql-injection-and-drupal-7-top-1-10-owasp-security-risks
.. _Cross Site Request Forgery (CSRF): http://drupalscout.com/knowledge-base/introduction-cross-site-request-forgery-csrf
.. _bus factor: http://www.thesalesengineer.com/2011/06/20/whats-your-se-bus-count/
.. _completely disable the account: https://www.drupal.org/node/947312#disable
.. _Paranoia: https://drupal.org/project/paranoia
.. _a lot of Drupal security modules: https://github.com/wet-boew/wet-boew-drupal/issues/248
.. _Automated Logout: https://drupal.org/project/autologout
.. _Clear Password Field: https://drupal.org/project/clear_password_field
.. _Drupal Tiny-IDS: https://drupal.org/project/tinyids
.. _Local Image Input Filter: https://drupal.org/project/filter_html_image_secure
.. _Login Security: https://drupal.org/project/login_security
.. _Password Policy: https://drupal.org/project/password_policy
.. _Session Limit: https://drupal.org/project/session_limit
.. _Settings Audit Log: https://drupal.org/project/settings_audit_log
.. _Security Kit: https://drupal.org/project/seckit
.. _Secure Login: https://drupal.org/project/securelogin
.. _HTTP Strict Transport Security: https://www.drupal.org/project/hsts
.. _enforce it through web-server settings: http://opentodo.net/2012/10/enable-http-strict-transport-security-in-apache-nginx/)
.. _Secure Pages: https://drupal.org/project/securepages
.. _Secure Permissions: https://drupal.org/project/secure_permissions
.. _Security Review: https://drupal.org/project/security_review
.. _Shield: https://drupal.org/project/shield
.. _Restrict IP: https://drupal.org/project/restrict_ip
.. _Username Enumeration Prevention: https://drupal.org/project/username_enumeration_prevention
.. _Delete all: https://www.drupal.org/project/delete_all
.. _Devel: https://www.drupal.org/project/devel
.. _Drupal for Firebug: https://www.drupal.org/project/drupalforfirebug
.. _Theme Developer: https://www.drupal.org/project/devel_themer
.. _Trace: https://www.drupal.org/project/trace
.. _Backup and Migrate: https://www.drupal.org/project/backup_migrate
.. _Guardr: https://drupal.org/project/guardr
.. _Hardened Drupal: https://drupal.org/project/hardened_drupal
.. _CIA information security triad: https://en.wikipedia.org/wiki/Information_security
.. _sanitized version of the database: http://drupalscout.com/knowledge-base/creating-sanitized-drupal-database-backup
.. _risk levels: https://www.drupal.org/security-team/risk-levels
.. _`NIST Common Misuse Scoring System`: http://www.nist.gov/itl/csd/cmss-072512.cfm
.. _`Drop Guard`: http://www.drop-guard.net/
.. _salt: https://en.wikipedia.org/wiki/Salt_%28cryptography%29