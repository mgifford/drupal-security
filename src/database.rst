G) Database Layer
-----------------

| With Drupal's database abstraction layer you can now run it on
`MySQL <https://www.mysql.com/>`__, `SQLite <https://www.sqlite.org/>`__
or `PostgreSQL <http://www.postgresql.org/>`__ out of the box.
| There are in fact a number of popular MySQL forks like
`MariaDB <https://mariadb.org/>`__ and
`Percona <http://www.percona.com/software/percona-server>`__.
| Drupal can run with MSSQL too, but there will be more support for
MySQL flavours of SQL.
| Oracle support for PHP is weak, so it is not recommended to use this
database.
| We are not aware of any security advantages of one over the other.

| The database for Drupal can run on the same server, but for
performance reasons it can be beneficial to set it up on another server.
| You want to ensure that your server environment is robust enough that
it cannot be easily brought down by a Denial of Service (DOS) attack.
| There are a few server side tools to help with this, but mostly it's
useful to have a buffer, even at your highest traffic times, so that
your site is always responsive.

| At the point where your server environment spreads on to more than one
system, it begins to make sense to have a second network behind the web
server, possibly including a VPN.
| It is quite likely that if the database is moved to an external server
that there may soon be other servers including more than one front-end
server too.

| There is a lot that can be done to `secure your
database <http://www.greensql.com/content/mysql-security-best-practices-hardening-mysql-tips>`__.
| Much of it comes down to reviewing `access permissions for the Drupal
user <https://drupal.org/documentation/install/create-database>`__ (set
in Drupal's settings.php), the backup user (which has read only access
to do regular backups) and the database's root user (which obviously has
access to everything) and verifying that they all have complex
passwords.
| These need to be unique passwords and the root password should not be
stored on the server, but rather in your encrypted Keepass database.

| If your server is running locally, you can disable access for MySQL to
the network and force it to only use the internal IP address.
| If your web server and database are on different servers, you won't be
able to do this, but you will be able to restrict what address MySQL
will listen on.
| If your web server and database server share a LAN, bind MySQL only to
the LAN IP address and not any Internet-facing ones.
| For a machine running both the web server and MySQL, you can add this
to your my.conf file:

::

    bind-address=127.0.0.1

| Be sure to `review your databases, users and
permissions <http://www.symantec.com/connect/articles/securing-mysql-step-step>`__
to see that there are not any sample users or old databases still
enabled on the server and that you are not giving greater access to a
user than they need.
| You should also review the file system to see that the database files
are restricted.

| If you need a graphical tool like
`phpMyAdmin <http://www.phpmyadmin.net/home_page/index.php>`__, disable
it after use.
| Web applications like this can also be tightened down by placing them
on a different port, firewall that port from other than 127.0.0.1, and
always access it via ssh port forwarding.
| Access to these tools can also be limited to IP addresses for extra
protection.
| Note that any software you use should be regularly updated to ensure
that it receives any security enhancements, particularly if stored on
the server.
| You can restrict access to phpMyAdmin via .htaccess or by configuring
Apache to request an HTTP username/password login.
| They can also be restricted to only allow access from certain trusted
IP addresses.
| This is an important vulnerability as it could give acracker full
access to your databases.
| It can be beneficial to put phpMyAdmin in its own VirtualHost and even
run it on a non-standard port.
| Force HTTPS connections to phpMyAdmin - do not use regular HTTP.
| Also consider the implications of allowing database access via the web
server: There is little benefit if you have restricted which interfaces
MySQL will listen on, as described above, but then allow control of the
database from an Internet-facing web page.
