I) Writing Secure Code
======================

There are lots of great resources about how to write secure code. The `Drupal
handbook page`_ is a great place to start as it is focused directly on the best
practices defined by this community.

In Drupal 7 it is important to remember that the themes all have PHP in them and
that this is a potential place of a security breach. It isn't uncommon for
themers to put a lot of PHP inside of a theme rather than in a separate module.
It's also more difficult to keep up with security releases in themes, as they
are by their very nature customized.

OWASP has a good `PHP Security Cheat Sheet`_ with information on specific things
to watch out for when running PHP applications. They also have a more generic
document on `Secure Coding`_ and a more specific one on `HTML5 Security`_.

There are also lots of good blogs on writing secure code, `like this one,`_
highlighting general approaches to PHP coding.

Code review can be used in order to find flaws in existing code and discover
potential bugs.  OWASP offer a `free book`_ that can guide you on that process.
Basically, you can do it manually using the same guidelines as when writing
secure code, but you can as well use automated tools. Theses can be `installed
in a continuous integration system such as Jenkins`_ in order to periodically
checks for flaws. Common clarity and code style rules can spot weak code that is
not directly tied to security but can be an indicator on code quality, thus
giving a hint on security. Rare tools exists to find security related weaknesses
in PHP frameworks and PHP such as `phpcs-security-audit`_ that even support
Drupal, but like many tools they need manual follow up and tend to execute
slowly.

Common Drupal secure coding practices are:

* Never trust user input.

  With `sanitization functions`_ like :drupalapi:`check_plain`,
  :drupalapi:`filter_xss`, and :drupalapi:`filter_xss_admin` it is easy in
  Drupal to clean strings on output. Any variable in a template or HTML output
  should pass through one of these.

* Protect yourself from SQL Injection through leverage Drupal's
  `database abstraction layer`_. Drupal 6 should use `parameterization`_.

* Use :phpdoc:`preg_replace_callback` rather than :phpdoc:`preg_replace` as the
  latter can allow matches to be evaluated as PHP code although the ``\e``
  modifier that introduced this flaw is now deprecated in PHP.

* Always use the Drupal functions when possible instead of plain old PHP.

* Drupal comes with jQuery and leverages it extensively. However, do not rely on
  JavaScript for validation.

* If you are using :phpdoc:`eval` or :drupalapi:`drupal_eval` this is a
  potential security risk if PHP input provided contains malicious code.

  If you do this, you can add a new permission in your module so that an admin
  needs to explicitly assign permissions to a user role.

* Same precautions should be taken with functions such as :phpdoc:`exec`,
  :phpdoc:`system`, :phpdoc:`fopen`, :phpdoc:`delete` and others that execute
  external applications or interact directly with the file system.

As David Strauss wrote recently, `All Code is Debt`_. "All of the custom code
you've written yesterday, rewritten today, and what you'll write tomorrow ― you
will be burdened with maintaining, forever." Code needs to be maintained on a
regular basis to ensure that it is keeping up with the latest security best
practices.

When writing code, testing is important and security testing should be part of
the process. OWASP publishes a very complete `Testing Guide`_ as well as an
`Application Security Verification Standard`_ that goes deep into details. The
verification standard could also be used as a complete security requirement list
when designing new modules for your Drupal site. Open source tools such as
`OWASP ZAP`_ and `Subgraph Vega`_ provide graphical user interface to perform
dynamic scanning of Web sites. For complex Drupal sites they might have some
difficulties but they can still be used as a intercepting web proxy in order to
perform manual testing.

.. _Drupal handbook page: https://drupal.org/writing-secure-code
.. _PHP Security Cheat Sheet: https://www.owasp.org/index.php/PHP_Security_Cheat_Sheet
.. _Secure Coding: https://www.owasp.org/index.php/Secure_Coding_Cheat_Sheet
.. _HTML5 Security: https://www.owasp.org/index.php/HTML5_Security_Cheat_Sheet
.. _like this one,: http://www.addedbytes.com/articles/writing-secure-php/writing-secure-php-1/
.. _free book: https://www.owasp.org/index.php/Category:OWASP_Code_Review_Project
.. _installed in a continuous integration system such as Jenkins: http://jenkins-php.org/
.. _phpcs-security-audit: https://github.com/Pheromone/phpcs-security-audit
.. _sanitization functions: https://api.drupal.org/api/drupal/includes%21common.inc/group/sanitization/7
.. _database abstraction layer: https://api.drupal.org/api/drupal/includes%21database%21database.inc/group/database/7
.. _parameterization: https://drupal.org/node/101496
.. _All Code is Debt: https://www.getpantheon.com/blog/all-code-debt
.. _Testing Guide: https://www.owasp.org/index.php/OWASP_Testing_Project
.. _Application Security Verification Standard: https://www.owasp.org/index.php/Category:OWASP_Application_Security_Verification_Standard_Project
.. _OWASP ZAP: https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project
.. _Subgraph Vega: http://www.subgraph.com/products.html
