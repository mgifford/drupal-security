F) PHP
======

.. highlight:: ini

There are lots of good resources on how to tighten security for PHP. It is a
very commonly used scripting language and it is running some of the biggest and
most important sites on the Internet.

We recommend installing a PHP hardening tool called `Suhosin`_ which tightens up
PHP's existing configuration so that it is more robust. It is designed to
protect servers and users from known and unknown flaws in PHP applications and
the PHP core.

.. code-block:: bash

  # Ubuntu:
  # Enable "universe" repo
  $ vi /etc/apt/sources.list
  $ apt-get update ; apt-get install php5-suhosin

  # Debian:
  $ apt-get install php5-suhosin

  # CentOS:
  $ yum install php-suhosin

A good comprehensive list is from Justin C. Klein's blog post `Hardening PHP
from php.ini`_. Other than his comments on ``safe_mode``, we think he's got it
right. Drupal needs ``safe_mode`` disabled in PHP. PHP's Safe Mode isn't really
considered much of a security enhancement and it has been removed in recent
versions.

As with Apache modules, look for what you can remove. You can display a list of
enabled PHP modules and look for those which can be removed. From the command
line you can get a list of php modules with:

.. code-block:: bash

  $ php -m

Setting ini Variables
---------------------

Many PHP variables can be set via Apache as well as in the PHP configuration.
We recommend keeping PHP-specific security configuration centrally located in
the :file:`php.ini` file.

Another exploit is `Session fixation`_ where a user's browser session can be
hijacked by a third party.

`OWASP`_ goes into much more detail, but by using the `HttpOnly`_ flag when
generating a cookie you can reduce the risk of an :abbr:`XSS (Cross Site
Scripting)` attack by limiting access to protected cookies. It is advised to
stop Javascript from accessing cookie data. Session information should only ever
be passed to the server with the same domain. You can also set a `secure cookie
attribute`_ and restrict all transmission of cookie data to an HTTPS connection
to ensure that the cookie is less likely to be exposed to cookie theft via
eavesdropping. Furthermore, you can control the `hash algorithm`_ used to
generate the session ID and choose from a number of algorithms like the NSA's
`SHA-2`_ protocol or `whirlpool`_. Add the following to your php.ini file::

  session.cookie_httponly = 1
  session.use_only_cookies = 1
  session.cookie_secure = 1
  session.hash_function = whirlpool

You can obtain a list of the available hash functions on your system by
executing:

.. code-block:: bash

  $ php -r 'print_r(hash_algos())'

Limit your exposure to only the system resources you want to make available to a
PHP page. You can control your resources by limiting the
``upload_max_filesize``, ``max_execution_time``, ``max_input_time``,
``memory_limit`` variables so that a script isn't as likely to monopolize
resources::

  memory_limit = 128M
  max_input_time = 60
  max_execution_time = 30
  upload_max_filesize = 2M

By keeping up with security releases some will argue that there is no need to
hide which version of PHP you are running. There is a broader discussion of this
debate in Section L) Points of Debate under :ref:`debate-obscurity`. In the PHP setting you can also
`limit information about PHP`_ which is exposed by adding this to your
:file:`php.ini` file::

  expose_php = Off

You can also explicitly disable PHP functions which allow scripts to reference
other URLs::

  allow_url_include = Off
  allow_url_fopen = Off

You can also `disable PHP functions`_ which are considered dangerous. You will
want to test to see that your Drupal install doesn't require any of these
functions. You can grep from the Drupal root to find out if your site uses any
of these functions. Drupal's PHP filter leverages the :phpdoc:`exec` function,
however there are lots of good reasons not to use the PHP filter. You can add
this to your :file:`php.ini` file::

  disable_functions = php_uname, getmyuid, getmypid, passthru, leak, listen, diskfreespace, tmpfile, link, ignore_user_abord, shell_exec, dl, set_time_limit, exec, system, highlight_file, source, show_source, fpaththru, virtual, posix_ctermid, posix_getcwd, posix_getegid, posix_geteuid, posix_getgid, posix_getgrgid, posix_getgrnam, posix_getgroups, posix_getlogin, posix_getpgid, posix_getpgrp, posix_getpid, posix, _getppid, posix_getpwnam, posix_getpwuid, posix_getrlimit, posix_getsid, posix_getuid, posix_isatty, posix_kill, posix_mkfifo, posix_setegid, posix_seteuid, posix_setgid, posix_setpgid, posix_setsid, posix_setuid, posix_times, posix_ttyname, posix_uname, proc_open, proc_close, proc_get_status, proc_nice, proc_terminate, popen

Drupal's status page has a link to the output of :phpdoc:`phpinfo` and you
should decide whether or not you want to exclude that function in this list.
You want to be able to limit what PHP has access to in the file system. Note
that you may want to give slightly more access to PHP than just the Drupal root
directory as it can be beneficial to put some files (like a salt.txt file)
outside of the base directory. This can also be set in Apache, but I've tried to
keep the PHP specific information inside the :file:`php.ini` file::

  open_basedir = /var/www

Make sure the session path is outside the root web directory and not readable or
writable by any other system users. You will also want to set a temporary upload
file directory that is outside of the web root. This can be specified in the
php.ini file::

  session.save_path = "/tmp"
  upload_tmp_dir = "/tmp"

.. _Suhosin: http://www.suhosin.org/stories/index.html
.. _Hardening PHP from php.ini: http://www.madirish.net/199
.. _Session fixation: https://en.wikipedia.org/wiki/Session_fixation
.. _OWASP: https://www.owasp.org/index.php/HttpOnly
.. _HttpOnly: http://php.net/manual/en/function.setcookie.php
.. _secure cookie attribute: https://en.wikipedia.org/wiki/HTTP_cookie#Secure_cookie
.. _hash algorithm: http://www.php.net/manual/en/session.configuration.php#ini.session.hash-function
.. _SHA-2: https://en.wikipedia.org/wiki/SHA-1
.. _whirlpool: https://en.wikipedia.org/wiki/Whirlpool_%28cryptography%29
.. _limit information about PHP: http://simonholywell.com/post/2013/04/three-things-i-set-on-new-servers.html
.. _disable PHP functions: http://www.cyberciti.biz/faq/linux-unix-apache-lighttpd-phpini-disable-functions/
