H) Drupal
=========

1) Files
~~~~~~~~

| `Verify Drupal file permissions on the
server <https://drupal.org/node/244924>`__.
| You really need to restrict write access to the server and verify that
the right users/groups have the access that they need for Drupal to
operate effectively.
| One can set all of Drupal's files to be read only, only allowing for
file uploads, cached files, sessions and temporary directories with
write permissions.
| The major limitation of this approach is that it makes applying
security upgrades more difficult.

| By default, Drupal 7 disables execution of PHP in directories where
you can upload PHP.
| Check the .htaccess file in the files directory.
| You can also add this to your Apache Virtual Host to ensure that no
handlers have been overlooked.

::

    <Directory
    /var/www/drupal/sites/default/files/>

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

| Drupal needs to be able to write to the server to be able to perform
certain tasks like managing file uploads and compressing/caching CSS/JS
files.
| Ensure that Apache has write access to /tmp and also to the public
sites folder:

::

    Debian: chown -R www-data:www-data
    sites/default/files
    CentOS: chown -R nobody:nobody sites/default/files

| Make sure that you are only allowing users to upload file types that
have limited security problems with them.
| Text and images are usually quite safe.
| There have been some exploits on PDF files, but they are quite rare.
| Microsoft Office documents should be scanned if they are going to be
uploaded onto the server.
| `ClamAV <https://drupal.org/project/clamav>`__ can be incorporated
into Drupal to scan uploaded files for viruses and other malicious code.
| Acquia recommends excluding the following file types: flv, swf, exe,
html, htm, php, phtml, py, js, vb, vbe, vbs.

2) Drush
~~~~~~~~

| Drush is a command line shell and scripting interface for Drupal.
| We strongly recommend using
`Drush <https://github.com/drush-ops/drush>`__ on both staging and
production servers because it simplifies development and maintenance.
| Note that the version of Drush packaged with your OS is likely to be
extremely out of date.

| Although Drush used to be installed best with `PHP's
PEAR <http://pear.php.net/>`__, the current best practice is with
`Composer <https://getcomposer.org/doc/00-intro.md#system-requirements>`__
(the dependency manager for PHP).
| See install details on the `Drush git
page <https://github.com/drush-ops/drush#installupdate---composer>`__.

| There is a `Security
Check <https://drupal.org/project/security_check>`__ module available
for Drush which is a basic sanity test for your configuration.
| When the module is added, you can run this against your site from
Apache's document root (docroot) on the command line using:

::

    drush secchk

| As with the server configuration in general, document what you are
using.
| Drush makes this fairly straightforward as you can simply export a
list from the command line:

::

    drush pm-list --type=Module --status=enabled

| Cron is the Linux time-based job scheduler and it is used for a lot of
key Drupal functions.
| Check to see that you are running cron several times a day.
| For Drupal 7 and above, `if there is traffic to the site, cron jobs
are run every 3 hours <https://drupal.org/cron>`__.
| The status page will tell you when the last time cron was run on the
site.
| You may want to set up a Linux cron job using using Drush if you have
either a low traffic site or have special requirements.

To run cron on all of your sites in /home/drupal - from the command line
enter crontab -e and then insert:

::

    30 2,6,11,18 * * * cd /home/drupal && drush
    @sites core-cron -y > /dev/null

| You will need developer modules to help you build your site, but they
are a security risk on your production site and need to be disabled.
| Many modules (such as Views) have separate administration screens that
can also be disabled in a production environment.
| They are absolutely required when building the site, but can be
disabled when they are not in use.
| It is always a good practice to see if there are any unnecessary
modules can be disabled on your site.
| This also offers performance benefits.
| Views is an incredibly powerful query building tool.
| Because of that, it is important that all Views have explicit access
permissions set at /admin/build/views

3) Errors
~~~~~~~~~

| Check the Status Report and Watchdog pages regularly and resolve
issues - Drupal should be happy! This needs to be done regularly, even
after launch.
| Remember that you can more quickly scan your logs by filtering for PHP
errors.
| With the `Views
Watchdog <https://drupal.org/project/views_watchdog>`__ module you could
also build custom reports to display on your website.
| On your production server, make sure to disable the display of PHP
errors.
| These should be recorded to your logs, but not visible to your
visitors.
| On your staging site you will want to see those errors to help you
debug PHP problems, but it is a potential vulnerability to have those
exposed.
| This won't catch all PHP errors however, and so it is also useful to
review the error log of the web server itself.

| Watchdog is a good tool, but is `limited in a number of
ways <http://www.asmallwebfirm.net/blogs/2013/04/achieving-drupal-log-bliss-splunk>`__.
| Simply because it is database dependent, even having a lot of 404
errors can affect performance.
| Fortunately, logs can be easily directed to the server's syslog, with
the `Syslog Access <https://drupal.org/project/syslog_access>`__ module,
which also allows you to leverage your favourite log management tool.
| The Drupal Handbook also has a great resource for how to `send your
logs to Syslog <https://drupal.org/documentation/modules/syslog>`__ with
integrated logging.

4) Core and Contrib Hacks
~~~~~~~~~~~~~~~~~~~~~~~~~

| Before launching your site (and periodically afterwards) it is useful
to run the `Hacked! <https://drupal.org/project/hacked>`__ module to
check what code differs from what was released on Drupal.org.
| Particularly when the `diff <https://drupal.org/project/diff>`__
module is enabled this is a powerful tool to evaluate your code.
| There are millions of lines of code in a given Drupal site, so Hacked!
is a really valuable analysis tool.
| If you need to apply patches against the stable released version of
the code, the patch should be in a clearly documented directory.
| It is unfortunately a common practice for less experienced Drupal
developers to cut corners and hack core to provide some functionality
that is required.
| There are lots of reasons why this is a bad idea and `why responsible
developers don't hack
core <http://drupal.stackexchange.com/questions/59054/why-dont-we-hack-core>`__.
| For the purposes of this document it is sufficient to say it makes it
harder to secure.
| The `same is true for contributed
modules <http://www.bluespark.com/blog/youre-doing-it-wrong-dont-hack-drupal-core-change-text>`__,
you shouldn't have to alter the code to customize it most of the time.
| The Hacked! module is very useful in identifying when modules no
longer are the same as their releases on Drupal.org.
| Being able to quickly scan through hundreds of thousands of lines of
code and find differences against known releases is a huge security
advantage.

You can also generate Drush make file from an existing Drupal site and
then recreate a clean copy of the codebase which you can then diff (a
command line comparison tool) to determine if your site has been hacked.

::

    drush generate-makefile make-file.make
    drush make make-file.make -y

| It is recommended to run all modules you use through the
`Coder <https://drupal.org/project/coder>`__ module, but especially any
custom built modules and themes.
| This module `can give you
suggestions <https://drupal.org/node/2135539>`__ on how to follow the
`Drupal communities coding
standards <https://drupal.org/coding-standards>`__.

| It can also help you identify other coding errors that may affect your
site.
| Particularly when building custom modules the Coder module can help
identify `unsanitized user input <https://drupal.org/node/101495>`__,
`SQL injection
vulnerabilities <http://www.pixelite.co.nz/article/sql-injection-and-drupal-7-top-1-10-owasp-security-risks>`__
and `Cross Site Request Forgery
(CSRF) <http://drupalscout.com/knowledge-base/introduction-cross-site-request-forgery-csrf>`__
problems.
| It is unfortunately quite common for developers to extend Drupal by
forking existing projects and not provide enhancements back to the
community.
| Doing this breaks assumptions within the Update module but more
importantly makes upgrades much more difficult.
| Even with a properly documented patch, it is a lot of work to upgrade,
patch and re-write a function in a live website.

| By contributing the improved code upstream, you can avoid that often
painful process.
| The peer review that comes with contributing your code back to the
community is a secondary benefit: your codebase will become more robust
because more people will understand it.
| Your `bus
count <http://www.thesalesengineer.com/2011/06/20/whats-your-se-bus-count/>`__
(the number of people who can go missing from a project by either being
hit by a bus or winning the lottery) will increase by releasing your
code.
| Publishing the code elsewhere forces you to actually think about what
is required.
| Further, if someone tries to install your code/system, they might
notice missing parts or for that matter parts that might be
confidential.

5) Administration
~~~~~~~~~~~~~~~~~

| Drupal has a very fine grained and customizable permissions model.
| In its simplest form, users are assigned roles and each role is given
permissions to various functions.
| Take the time to review roles with access to any of Administer
filters, Administer users, Administer permissions, Administer content
types, Administer site, Administer configuration, Administer views and
translate interface.
| It is useful to review the permissions after upgrades to verify if any
new permissions have been added.

| Don't use "admin" as your user/1 admin name.
| It's the first one that a cracker is going to try, so be a bit more
unique.
| Obscurity isn't the same as security, but no need to give them their
first guess when choosing user names.
| Another good practice with regards to user/1 is to `completely disable
the account <https://www.drupal.org/node/947312#disable>`__.
| With the advent of Drupal 7 and drush, user/1 is not required to
administer Drupal websites anymore, and thus can be simply blocked.
| The account can be re-enabled as needed through drush or directly in
the database.

| As with other server user accounts, you will want to restrict who has
access to servers.
| Make sure to delete any test or developer accounts on the production
server.

| Don't run Drupal without enabling the Update module that comes with
core.
| Drupal core and contributed modules use a structured release process
that allows your administrators to be proactively alerted when one of
those modules has a security release.
| Any piece of code is susceptible to a security issue, and having a
central repository that a Drupal site can compare against is key to the
security paradigm.
| Aside from the releases that have fixes for known security problems,
some modules (or a version of that module) may become unsupported.
| This is also a security problem, in that you will not receive updates
if there are security problems that are identified with the module.
| The Update module also allows you to get a daily or weekly email if
there are security upgrades that need to be applied.

| Drupal's input filters are very powerful, but can provide a
vulnerability.
| Don't enable the PHP filter which is available in Drupal core.
| Installing the `Paranoia <https://drupal.org/project/paranoia>`__
module can really help enforce this practice.
| The PHP filter makes debugging more difficult and exposes your site to
a greater risk than it is worth.
| All PHP code should be written to the file system and not stored in
the database.
| Another input filter that is problematic is Full HTML which should
only be granted to administrator roles. Anyone with the Full HTML filter
can craft malicious JavaScript and gain full admin access to any website
on the same domain as the Drupal website.
| If needed, you can add some additional tags to the Filtered HTML input
format but be cautious.

6) Modules to Consider
~~~~~~~~~~~~~~~~~~~~~~

| There are `a lot of Drupal security
modules <https://github.com/wet-boew/wet-boew-drupal/issues/248>`__.
| Depending on your needs you will want to add more or less than those
listed here.

-  `Automated Logout <https://drupal.org/project/autologout>`__ -
   ability to log users out after a specified time of inactivity
-  `Clear Password
   Field <https://drupal.org/project/clear_password_field>`__ - Stops
   forms from pre-populating a password
-  `Drupal Tiny-IDS <https://drupal.org/project/tinyids>`__ - An
   alternative to a server-based intrusion detection service
-  `Local Image Input
   Filter <https://drupal.org/project/filter_html_image_secure>`__ -
   Avoids CSRF attacks through external image references
-  `Login Security <https://drupal.org/project/login_security>`__ - Set
   access control to restrict access to login forms by IP address
-  `Paranoia <https://drupal.org/project/paranoia>`__ Limits PHP
   functionality and other controls
-  `Password Policy <https://drupal.org/project/password_policy>`__ -
   Enforces your user password policy
-  `Session Limit <https://drupal.org/project/session_limit>`__ - limit
   the number of simultaneous sessions per user
-  `Settings Audit
   Log <https://drupal.org/project/settings_audit_log>`__ - Logs who did
   what, when
-  `Security Kit <https://drupal.org/project/seckit>`__ - Hardens
   various pieces of Drupal
-  `Secure Login <https://drupal.org/project/securelogin>`__ - Provides
   secure HTTPS access, without mixed-mode capability
-  [HTTP Strict Transport Security]
   (https://www.drupal.org/project/hsts) - To be used together with
   Secure Login, to prevent ssl strip attacks. Alternatively, directly
   enforce through web-server settings (see
   http://opentodo.net/2012/10/enable-http-strict-transport-security-in-apache-nginx/)
-  `Secure Pages <https://drupal.org/project/securepages>`__ - Manages
   mixed-mode (HTTPS and HTTP) authenticated sessions for enhanced
   security (note required core patches)
-  `Secure
   Permissions <https://drupal.org/project/secure_permissions>`__ -
   Disables the UI to set/change file permissions
-  `Security Review <https://drupal.org/project/security_review>`__ -
   Produces a quick review of your site's security configuration
-  `Shield <https://drupal.org/project/shield>`__ - Protects your
   non-production environment from being accessed
-  `Restrict IP <https://drupal.org/project/restrict_ip>`__ - Restrict
   access to an administrator defined set of IP addresses
-  `Username Enumeration
   Prevention <https://drupal.org/project/username_enumeration_prevention>`__
   - Stop brute force attacks from leveraging discoverable usernames

7) Modules to Avoid on Shared Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Many Drupal modules intended to help developers develop code also
disclose sensitive information about Drupal and/or the webserver, or
allow users to perform dangerous operations (e.g.: run arbitrary PHP
code or trigger long-running operations that could be used to deny
service).
| These modules can be used to debug locally (and many are essential
tools for Drupal developers), but should never be installed on a shared
environment (e.g.: a production, staging, or testing server).

| To limit the damage a malicious user can do if they gain privileged
access to Drupal, it's not sufficient for a development module to be
simply disabled: the files that make up the module should be removed
from the filesystem altogether.
| Doing so prevents a malicious user from enabling it and gaining more
data about the system than they would be able to otherwise.
| Note that it is difficult to automatically enforce that these modules
are not deployed to shared systems: developers need to understand why
they should not commit these modules and take care to double-check what
they're about to deploy.

Some popular development modules which should not be present on any
shared website include:

-  `Delete all <https://www.drupal.org/project/delete_all>`__ — This
   module allows someone with sufficient privileges to delete all
   content and users on a site.
-  `Devel <https://www.drupal.org/project/devel>`__ — Besides letting
   users run arbitrary PHP from any page, Devel can be configured to
   display backtraces, raw database queries and their results, display
   raw variables, and disable caching, among other things.
-  `Drupal for
   Firebug <https://www.drupal.org/project/drupalforfirebug>`__ — Drupal
   for Firebug outputs the contents of most variables, raw database
   queries and their results, display PHP source code, and can be used
   to run arbitrary PHP. Furthermore, it does all this by interfacing
   with browser developer tools, making it difficult to determine if
   this module is enabled by glancing at the site.
-  `Theme Developer <https://www.drupal.org/project/devel_themer>`__ —
   This module, which depends on the Devel module mentioned earlier, is
   very useful for determining which theme files / functions are used to
   output a particular section of the site, but it displays raw
   variables and slows down the site significantly.
-  `Trace <https://www.drupal.org/project/trace>`__ — This module can be
   used to display backtraces and raw variables, among other things.

| Note that most "normal" modules can be dangerous if a malicious user
gains privileged access to Drupal.
| You should evaluate each new module you install to determine what it
does and whether the features it brings are worth the risks.
| Some modules to take into special consideration are:

-  `Backup and
   Migrate <https://www.drupal.org/project/backup_migrate>`__ allows you
   to download a copy of the site's database. If restrictions placed
   upon you by your hosting provider prevents you from being able to
   make backups, this module will allow you to do so; but a malicious
   user with privileged access would be able to download a copy of the
   whole Drupal database, including usernames, passwords, and depending
   on your site, access keys to the services you use.
-  `Coder <https://www.drupal.org/project/coder>`__ — This module is
   very useful for ensuring your code conforms to coding standards but
   can be used to display the PHP that makes up modules.

8) Drupal Distributions
~~~~~~~~~~~~~~~~~~~~~~~

| Drupal distributions provide turnkey installations that have been
optimized for specific purposes, generally with a curated selection of
modules and settings.
| There are now two distributions which have been specifically built for
security, `Guardr <https://drupal.org/project/guardr>`__ and `Hardened
Drupal <https://drupal.org/project/hardened_drupal>`__.
| Guardr is built to follow the `CIA information security
triad <https://en.wikipedia.org/wiki/Information_security>`__:
confidentiality, integrity and availability.
| It is worth watching the evolution of these distributions and
installing them from time to time if only to have a comparison of
modules and configuration options.

9) Miscellaneous
~~~~~~~~~~~~~~~~

| Review the discussion in Section K and decide if you are going to
remove the CHANGELOG.txt file.
| Ensure that you can keep up security upgrades on a weekly basis and
**do not hack core**!
| If you plan to distribute your live site so that you can do testing or
development outside of a controlled environment, consider building a
`sanitized version of the
database <http://drupalscout.com/knowledge-base/creating-sanitized-drupal-database-backup>`__.
| This is especially important if you have user information stored in
the database.
| For many government sites this may not be necessary.
