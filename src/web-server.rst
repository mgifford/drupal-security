E) Web Servers
==============

.. highlight:: bash

.. image:: /_static/images/noun/noun_18141.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: A link from the noun project.

All files and directories in your DocumentRoot should be editable by a non-root
user (usually "www-data"), and should also not be writable by the Apache user, 
except the Drupal files/ directory. Please refer to Drupal's `Securing file 
permissions and ownership`_ for the complete discussion.

`PHP-FPM over FastCGI`_ allows your server to have `site-specific "pools" of
PHP`_. By giving each site unique PHP permissions you can effectively "sandbox"
a PHP application and simplify file/folder permissions by specifying the user
and group for the process pool. This reduces the points of failure in a shared
hosting environment, where the PHP on another site could be used to hijack the
server. There are also real `advantages to using PHP-FPM for managing server
load`_ as Apache's ``mod_php`` isn't very efficient.

Server or browser support for SSL versions 2 and 3 are not recommended. Despite
this, as Google noted in their blog post about the `POODLE Exploit`_, "SSL 3.0
is nearly 18 years old, but support for it remains widespread." Many older browsers 
still support this insecure version of SSL, but it is `easy to test`_ to ensure
if your browsers are vulnerable and the number of `exposed users is falling`_. 
Qualys SSL Labs also have a really `great tool to evaluate`_ if your server is 
still vulnerable.

On your web server, it is good to ensure that SSL configuration permits only TLS
version 1.2. unfortunately some common web browsers still do not support the
latest version of TLS. Fortunately, as of `September 2015`_, the latest version
of all major web browsers support only secure TLS 1.0, 1.1, and 1.2 by
default. Check if the `SSL services employ only AES`_ with key lengths 256 bits
and higher. You can install `GnuTLS`_ from the command line to enable this::

  # Ubuntu/Debian
  $ apt-get install gnutls-bin

It is also recommended to disable SSLCompression in Apache. As stated in the
`Apache documentation`_ "Enabling compression causes security issues in most
setups (the so called `CRIME attack`_ )." This is the default for Apache version
2.4.4+.

The **HeartBleed security bug** did a lot of damage in 2014. The
primary security practice we can recommend from this is to ensure that someone
is always paying attention to the security mailing lists for your operating
system. By the time you hear it from the media it is probably too late. The
other suggestion is one that is suggested by the `EFF`_ and others which
includes implementing `Perfect Forward Secrecy`_ (PFS). Although we didn't
explicitly refer to it as this in earlier versions of this document, the
hardened SSL configuration we recommended in the fall implements this.

The duraconf configuration scripts for `hardening SSL/TLS services`_ provided by
Jacob Appelbaum would have protected users from the HeartBleed bug. In the
Apache config you can `set hardened SSL configurations for the HTTPS protocol`_
(note that we're now using Hynek Schlawack configuration rather than `Ivan
Ristic's`_ because it is being updated more regularly) with:

.. code-block:: apache

  SSLProtocol ALL -SSLv2 -SSLv3
  SSLHonorCipherOrder On
  SSLCipherSuite ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS

After restarting Apache, you can check the SSL information in a browser by
double clicking on the lock icon in the address bar on HTTPS sites to get
information on the encryption channel and confirm it's using TLS.

There are other approaches like that suggested by `Remy van Elst`_, but
ultimately you need to test your SSL configuration through a tool like `Qualys
SSL Labs' Server Test`_. This is a free online service that performs a deep
analysis of the configuration of any SSL web server on the public Internet. This
will grade your SSL compliance and do things like confirm that you are using the
latest version of TLS and verify that you are protected from `BEAST attacks`_.
You want straight A's!

On your staging/development server it is fine to provide a `self signed SSL
certificate`_ to ensure that the traffic is encrypted. Setting up a third party
verified SSL certificate on your production environment will be important as
otherwise your users will be asked to verify the exception when accessing the
HTTPS version of your site. A listing of certificate authorities is available at
the bottom of `this Wikipedia page`_. You can review the validity of your SSL
certificate through a free `SSL Test constructed by SSLLabs`_ or with the
following openssl command::

  $ openssl s_client -connect SERVER:443

To check a specific protocol using openssl::

  $ openssl s_client -connect SERVER:443 -ssl2
  $ openssl s_client -connect SERVER:443 -ssl3

Note that SSL Certificate Authorities are depreciating the very popular SHA1
hashing function because of weakness in the algorithm. Qualys Labs recommends
`renewing with SHA256`_ as soon as possible.

1) Restricting Access
---------------------

Another useful Apache module is `mod_authz_host`_ which can restrict access to
specific pages such as ``/user`` and ``/admin/*`` - this can be useful if your
site is used just as a CMS with no user interaction. The example below is more
appropriate for sites which would have broader user authentication, but where
users are restricted from editing nodes - ``node/*/edit`` - this type of
approach can also be used to restrict access to non-production environments. If
you have a multi-lingual site using a language prefix, you may also want to 
check that sensitive paths are restricted with the language prefix. In Canada, 
many sites would need to add ``/fr/user`` and ``/en/user`` . It is a best practice 
to secure all pages on non-production environments from both search engines, but 
especially from crackers. The following are examples of how to do this with 
``mod_authz_host`` and also ``mod_rewrite``.

Example Apache configuration using ``mod_authz_host``:

.. todo::

  change ips to the documentation range

.. code-block:: apache

  <Location - "/node/.*/edit">
    Order Deny,Allow
    Deny from all
    Allow from 206.47.13.64 174.142.104.53 99.241.125.191
  </Location>

Example Apache configuration using ``mod_rewrite``:

.. code-block:: apache

  <IfModule mod_rewrite.c>
    RewriteEngine on
    # Allow only internal access to admin
    RewriteCond %{REMOTE_ADDR}
    !^(206\.47\.13\.64|174\.142\.104\.53|99\.241\.125\.191)$
    RewriteRule ^admin/.* - [F]
  </IfModule>

Drupal has a number of processes that can be triggered by URLs. You may wish to
block some of these using Apache so that they simply cannot be loaded from the
web browser. Common processes to secure are update, install and cron, tasks
which can all be triggered using Drush:

.. code-block:: apache

  RedirectMatch 403 "/(install|update|cron|xmlrpc|authorize).php"

2) Removing Code
----------------

`CGI`_\ s have been used extensively in web development and there are a great
many good server executables that you may want to consider running. However,
many CGIs that may be installed on a server are not actually needed and expose
you to an additional security risk. If you are not running any CGIs, you should
disable CGI access by removing ``LoadModule cgi_module`` and ``AddHandler
cgi-script .cgi`` from your Apache config. You can also do this from the command
line with::

  # Ubuntu/Debian
  $ a2dismod cgi

**If you don't need it, remove it.** All software is a source of potential risk, so
list all Apache modules and look for unneeded modules. There are some `good
discussions`_ on drupal.org about which modules are necessary and which are not.

::

  # Ubuntu/Debian
  $ apache2ctl -t -D DUMP_MODULES

  # CentOS
  $ apachectl -t -D DUMP_MODULES

If you are using ``mod_php`` with apache, it can be useful to enable
``php5-dev`` for Drupal so that you can enable tools like `PECL's
uploadprogress`_. However, after you've done that you will want to remove the
php5-dev module that you used to build it::

  # Ubuntu/Debian
  $ apt-get remove php5-dev

You can find other development packages on your server by::

  # Ubuntu/Debian
  $ apt-cache search ".-dev"

3) HTTP Headers
---------------

The Australian Government has produced an impressive report `Information
Security Advice for All Levels of Government`_ which is sadly a bit out-dated as
it hasn't been updated since early 2012. Most of that report is focused on
content security policy, HTTP strict transport security and frame options.

The `Security Kit`_ Drupal module addresses many security problems associated
with HTTP headers, but it is good to have them addressed at the Apache layer
where possible.

The `W3C`_ is developing a standard content security policy (CSP) to provide
security controls which can mitigate attacks such as `Cross Site Scripting
(XSS)`_.

`Mozilla`_ has produced a good description of how to write a `CSP`_ and there 
are many commonalities with the Australian Government report above. To allow 
content from a trusted domain and all its subdomains, you can add the following 
to your Apache configuration:

.. code-block:: apache

  Content-Security-Policy: default-src 'self' *.example.com

Your website and its visitors are going to be more secure if you use HTTPS to
ensure that all information passing between the web server and the browser is
encrypted. There is a `growing movement encrypt all web traffic`_, even to
brochure sites. Google announced in 2014 that HTTPS would be a `ranking signal`_. 
Doing so will have minor performance implications as it does
take some additional processing power. You certainly want to ensure that all
authentication happens through a secure HTTPS connection so that usernames and
passwords cannot be intercepted. Do ensure that all of your files are being
served from a HTTPS environment as mixed traffic introduces security problems.

.. code-block:: apache

  <VirtualHost *:80>
    ServerAlias *
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1[redirect=301]
  </VirtualHost>

This can be further enhanced by opting into the `HTTP Strict Transport Security
(HSTS)`_ enhancement which sends a special response header to the browser, which
then prevents any communications from being sent over HTTP to the specified
domain (see `HSTS example`_):

.. code-block:: apache

  Header set Strict-Transport-Security "max-age=16070400; includeSubDomains"

You can also submit your site to the `EFF's HTTPS Everywhere extension`_ which
will allows security conscious individuals to rewrite requests to these sites so
that they use HTTPS by default. As part of this extension, you can `submit new
public rules`_ for your site to ensure that it runs optimally with this browser
extension.

With the use of `Frame Options`_, users can be exposed to `Clickjacking`_ when
an iframe is injected in your site. If you know that you aren't going to need to
use iframes in your site you can disable it by modifying the Force X-Frame
options in the Apache configuration. As usual, `OWASP`_ has an `extremely useful
guide on avoiding Clickjacking`_. You must have the mod-headers module enabled
before adding this string to your Apache configuration but this is easy to add
through the command line -a2enmod headers - afterwards you can add this to your
configuration.

.. code-block:: apache

  Header always append X-Frame-Options SAMEORIGIN

4) HTTP Basic Authentication
----------------------------

Most webservers provide a way to restrict access to a site using `HTTP Basic
Authentication`_ — for example, using Apache HTTP Server's `htpasswd files or
Auth* directives`_, or nginx's `ngx_http_auth_basic_module`_ module.

While HTTP Basic Authentication is a good way to prevent search engines from
indexing your testing and staging sites, it is inherently insecure: traffic
between browsers and your site is not encrypted, and in fact, anyone can gain
access to the site simply by copying the "Authorization" HTTP header.

Furthermore, the username and password used for HTTP Basic Authentication are
not encrypted either (just base-64 encoded, which is trivial to decode), so do
not re-use credentials used elsewhere (e.g.: each unique login should have it's 
own unique password).

It is strongly recommended to store the htpasswd file outside the document root 
and to set it with read only permissions (444).

5) Web Application Firewall
---------------------------

Web Application Firewalls (WAFs) can be used to provide additional protection
over the Web server. It can be a standalone server that act as a reverse proxy
or a Web server modules.

Apache has a number of modules that can be installed to tighten security of the
web server. We recommend installing `ModSecurity and mod_evasive`_ as a `Web
Application Firewall (WAF)`_. This can be set to leverage the Open Web
Application Security Project's (OWASP) `ModSecurity Core Rule Set Project`_.

::

  # Ubuntu/Debian
  $ apt-get install libapache2-mod-evasive libapache2-modsecurity
  $ a2enmod mod-security; a2enmod mod-evasive

  # CentOS
  $ yum install mod_evasive mod_security

To engage ModSecurity in your Apache, you'll need to `set up the base files in
your Apache configuration`_ and then restart Apache.

Using default generic configurations such as the OWASP Core Rule Set can impact
the normal behaviour of Drupal and must be tested extensively before deployment.
Usually some rules are breaking rich content edition or modules that behave
differently than Drupal core. It is recommended to run the rules in a passive
manner in order to identify false positive when in production. Default
`configuration of ModSecurity`_ should do it with:

.. code-block:: apache

  SecRuleEngine DetectionOnly

You can then set it to "On" whenever you are ready. A server restart is needed
for changes to be effective. In that case the WAF will behave as a passive Web
application intrusion detection system and you can chose to never set it to "On"
if you wish to use it only for that purpose. In any cases, you'll want to
monitor the log files for alerts in order to detect malicious attempts and
potential false positives.

WAF software needs maintenance as well and rules should be updated periodically.
Tests for false positive should be made after each change of functionality
within the Drupal site.

At last but not least, WAFs are a great solution for `virtual patching`_ and
application flaw fixing, but they can be bypassed. It is discouraged to rely
solely on that technology to keep up with security: fixing flaw and applying
patch on the back-end applications should not be replaced with WAF utilization.

6) Managing the .htaccess file
------------------------------

Mike Carper has suggested a clean way of cleanly incorporating the `.htaccess file
within the Apache config`. Using Apache includes to incorporate the .htaccess
file provided by Drupal.org makes routine security upgrades much easier. When 
the .htaccess file changes, this will automatically be included by Apache. 
Unfortunately, Apache will need to be restarted before this will come into 
effect. There will be performance improvements by not loading the .htaccess file
with every page load.  You can also force some security rules right in the 
configuration. 

7) Everything Else
------------------

Modify the web server configuration to `disable the TRACE/TRACK`_ methods either
by employing the TraceEnable directive or by `adding the following lines`_ to
your Apache configuration:

.. code-block:: apache

  RewriteEngine On
  RewriteCond %{REQUEST_METHOD} ^(TRACE|TRACK)
  RewriteRule .* - [F]

You should keep your server up-to date. Security by obscurity may delay some
crackers, but not prevent them from accessing your system. Looking at the logs
for any popular site, you will notice thousands of fruitless attempts at
exploits that may not even exist (or have existed) on your system. Broadcasting
information about your server environment isn't likely to cause any harm, but if
you choose to disable it you can simply add this to your Apache configuration:

.. code-block:: apache

  ServerSignature Off
  ServerTokens ProductOnly

One of the nice things about Ubuntu/Debian is that the Apache file structure is
clean. By default it allows you to store a variety of different configurations for
sites or modules that are stored in logical directories. That's not critical,
but having a well defined Apache config file is. There should be inline comments
about all changed variables explaining why they were added or modified.

It is possible to restrict the outgoing access of the web server by leveraging
iptables' "--uid-owner" option on the OUTPUT table. This can also be done using
`containers and namespaces`_ on modern Linux kernels. In most cases, if you are
using containers, the UID of Apache will be the same inside the container as
outside of it.

You should make note of the user/UID of your web server. This is dependent on
the package installation order, but often this is "www-data" (uid 33) in
Debian/Ubuntu and "nobody" (uid 65534) in CentOS. If you are using PHP-FPM, then
you will need to search for the UID of that application rather than Apache's. 
Apache should never be run as your user login, although this is common in shared
hosting environments. 

Double check by viewing the output of::

  # Ubuntu/Debian
  $ ps aux grep apache

  # CentOS
  $ ps aux grep http

In order to restrict Apache to connect only to https://drupal.org (with IP
addresses 140.211.10.62 and 140.211.10.16 at the time of writing) insert the
following firewall rules::

  iptables -A OUTPUT -m owner --uid-owner ${APACHE_UID}
  -p udp --dport 53 -j ACCEPT

  iptables -A OUTPUT -d 140.211.10.62/32 -p tcp -m
  owner --uid-owner ${APACHE_UID} -m tcp --dport 443 -j ACCEPT

  iptables -A OUTPUT -d 140.211.10.16/32 -p tcp -m
  owner --uid-owner ${APACHE_UID} -m tcp --dport 443 -j ACCEPT

  iptables -A OUTPUT -m owner --uid-owner ${APACHE_UID}
  -m state --state NEW -j DROP

There are also Apache modules like `Project Honey Pot`_ that make it harder for
people to hack your system. Honey Pot can also be `installed on Drupal`_, but
Apache is often more efficient at addressing attacks like this before it hits
PHP::

  # Ubuntu/Debian
  $ apt-get install mod_httpbl

  # CentOS
  $ yum install mod_httpbl


.. _PECL's uploadprogress: http://pecl.php.net/package/uploadprogress
.. _Remy van Elst: https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html
.. _Qualys SSL Labs' Server Test: https://www.ssllabs.com/ssltest/
.. _BEAST attacks: https://en.wikipedia.org/wiki/Transport_Layer_Security#BEAST_attack
.. _self signed SSL certificate: https://en.wikipedia.org/wiki/Self-signed_certificate
.. _this Wikipedia page: https://en.wikipedia.org/wiki/Certificate_authority#External_links
.. _Securing file permissions and ownership: https://drupal.org/node/244924
.. _PHP-FPM over FastCGI: http://php-fpm.org/
.. _site-specific "pools" of PHP: http://www.howtoforge.com/php-fpm-nginx-security-in-shared-hosting-environments-debian-ubuntu
.. _advantages to using PHP-FPM for managing server load: https://phpbestpractices.org/#serving-php
.. _POODLE Exploit: http://googleonlinesecurity.blogspot.co.uk/2014/10/this-poodle-bites-exploiting-ssl-30.html
.. _easy to test: https://zmap.io/sslv3/
.. _exposed users is falling: https://www.trustworthyinternet.org/ssl-pulse/
.. _September 2015: https://en.wikipedia.org/wiki/Transport_Layer_Security#Web_browsers
.. _great tool to evaluate: https://www.ssllabs.com/ssltest/
.. _February 2014: https://en.wikipedia.org/wiki/Transport_Layer_Security#Web_browsers
.. _SSL services employ only AES: http://www.thinkwiki.org/wiki/AES_NI
.. _GnuTLS: https://help.ubuntu.com/community/GnuTLS
.. _Apache documentation: https://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcompression
.. _CRIME attack: https://en.wikipedia.org/wiki/CRIME
.. _EFF: https://www.eff.org/
.. _Perfect Forward Secrecy: https://www.eff.org/deeplinks/2013/08/pushing-perfect-forward-secrecy-important-web-privacy-protection
.. _hardening SSL/TLS services: https://github.com/ioerror/duraconf
.. _set hardened SSL configurations for the HTTPS protocol: https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
.. _Ivan Ristic's: https://community.qualys.com/blogs/securitylabs/2013/08/05/configuring-apache-nginx-and-openssl-for-forward-secrecy
.. _SSL Test constructed by SSLLabs: https://www.ssllabs.com/ssltest/
.. _renewing with SHA256: https://community.qualys.com/blogs/securitylabs/2014/09/09/sha1-deprecation-what-you-need-to-know
.. _mod_authz_host: https://httpd.apache.org/docs/2.2/mod/mod_authz_host.html
.. _CGI: https://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _good discussions: https://groups.drupal.org/node/41320
.. _Information Security Advice for All Levels of Government: http://www.dsd.gov.au/publications/csocprotect/protecting_web_apps.htm
.. _Security Kit: https://drupal.org/project/seckit
.. _W3C: http://www.w3.org/TR/CSP/
.. _Cross Site Scripting (XSS): https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29
.. _Mozilla: https://developer.mozilla.org/en-US/docs/Security/CSP/Using_Content_Security_Policy
.. _CSP: https://www.owasp.org/index.php/Content_Security_Policy
.. _growing movement encrypt all web traffic: http://chapterthree.com/blog/why-your-site-should-be-using-https
.. _ranking signal: http://googlewebmastercentral.blogspot.ca/2014/08/https-as-ranking-signal.html
.. _HTTP Strict Transport Security (HSTS): https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security
.. _HSTS example: https://www.owasp.org/index.php/HTTP_Strict_Transport_Security#Server_Side
.. _EFF's HTTPS Everywhere extension: https://www.eff.org/https-everywhere
.. _submit new public rules: https://www.eff.org/https-everywhere/rulesets
.. _Frame Options: https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options
.. _Clickjacking: https://en.wikipedia.org/wiki/Clickjacking
.. _OWASP: https://www.owasp.org/
.. _extremely useful guide on avoiding Clickjacking: https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet
.. _HTTP Basic Authentication: http://tools.ietf.org/html/rfc7235
.. _htpasswd files or Auth* directives: http://httpd.apache.org/docs/2.2/howto/auth.html
.. _ngx_http_auth_basic_module: http://nginx.org/en/docs/http/ngx_http_auth_basic_module.html
.. _disable the TRACE/TRACK: http://www.ducea.com/2007/10/22/apache-tips-disable-the-http-trace-method/
.. _adding the following lines: http://perishablepress.com/disable-trace-and-track-for-better-security/
.. _containers and namespaces: https://www.getpantheon.com/blog/containers-not-virtual-machines-are-future-cloud-0
.. _Project Honey Pot: https://www.projecthoneypot.org/httpbl_download.php
.. _installed on Drupal: https://drupal.org/project/httpbl
.. _ModSecurity and mod_evasive: http://www.thefanclub.co.za/how-to/how-install-apache2-modsecurity-and-modevasive-ubuntu-1204-lts-server
.. _Web Application Firewall (WAF): https://www.owasp.org/index.php/Web_Application_Firewall
.. _ModSecurity Core Rule Set Project: https://www.owasp.org/index.php/Category:OWASP_ModSecurity_Core_Rule_Set_Project
.. _set up the base files in your Apache configuration: https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#a-recommended-base-configuration
.. _configuration of ModSecurity: https://github.com/SpiderLabs/ModSecurity/blob/master/modsecurity.conf-recommended#L7
.. _virtual patching: https://www.owasp.org/index.php/Virtual_Patching_Cheat_Sheet
.. _`.htaccess file within the Apache config`: https://drupal.stackexchange.com/questions/108301/adding-htaccess-within-httpd-conf-correctly#answer-108346
