D) Server Security
==================

.. image:: /_static/images/noun/noun_65895_cc.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: Server from the noun project. 

Any website is a complex ecosystem of software. Each aspect can be tightened
through proper configuration and through the addition of components beyond what
is found in a default installation. This document provides some examples, but
mostly relies on links so that you can read the specific details on how this
should be done. There are other lists of considerations for server security,
like Robert Hansen's list of `10 major tenets of a secure hosting model`_, but
where possible we will be referring back to Section :doc:`principles`.

1) Server Procurement
---------------------

Start server documentation with information from your server contract. There
are often technical details and notes about who to contact when things go
wrong.

It is important to determine that there is a strong security community behind
the Operating System (OS) distribution you choose, and that you have the
necessary human resources in your department to maintain it. Both Debian/Ubuntu
and Red Hat Enterprise Linux (RHEL)/CentOS/Fedora can be considered solid. The
advantage of a Debian or Red Hat based solution is that there is extensive
documentation and large communities of users who've shared their experiences
through forums, issue trackers, and blog posts. Ubuntu is based on
Debian. CentOS is almost a copy of RHEL and Fedora is the community edition of
RHEL. The Fedora edition often releases updates before RHEL which can be an
advantage for some security fixes.  Most references to one of these two groups
of distributions should be interchangeable. Note that Ubuntu and Debian have a
different development cycle and are not identical.

If you use a Red Hat Enterprise Linux (RHEL) system, you will need to subscribe
to their service in order to apply security upgrades and install the additional
packages mentioned in this document. Before procuring a Red Hat server, check
that your package includes a subscription.

In our opinion, distributions of Linux like SUSE simply do not have a critical
mass of users and developers (in the web server space) to maintain the code and
documentation required for a secure environment. Microsoft Windows is not a
standard platform for hosting Drupal and is generally not recommended since
community support is much less robust. Furthermore, it is very difficult to 
limit exposure on a Windows Server since there are many unneeded pieces of the 
operating system which you cannot easily uninstall.

If you are worried about the server's physical security, you can also set up an
`encrypted partition`_ on your hard drive. If you do this, be aware that it 
may introduce performance issues which might cause problems for your server. 
This document will not be covering `how to set up an encrypted drive`_ but 
depending on the perceived threats, it may be worth implementing.

Special consideration should be taken when enabling HTTPS for encrypted traffic
on "shared host"-type environments (any server hosting more than 1 domain).
Typically, due to the nature of the protocol, only one HTTPS website (domain
name) could be hosted per IP. However, with `Server Name Indication`_ (SNI), it is
now possible to host multiple HTTPS domains with distinct `TLS certificates`_ on
the same IP. It must be noted that SNI is dependent on both the client and the
server supporting the TLS extension, but most do nowadays. Another option,
which might be useful if your servers or clients do not support SNI, is using
`Subject Alternative Name`_ on certificates (also known as Unified
Communications Certificates). These certificates contain extra fields that list
other common names (domain names) for which that certificate is valid.

Finally, don't get a server that comes with a server admin control panel. It
promises to make managing your site easier but presents security problems. There
are a number of commercial packages, like cPanel or PLESK, that do make it
easier to change settings on your server. This seems particularly attractive if
less technical users are responsible for server administration. In our recent
experience with cPanel, it introduced many difficulties in applying many of the
suggestions and recommendations described here. If you choose a server with one,
you will need to experiment with which of the following suggestions you are able
to implement. Some control panels are also known to overwrite settings when
manual changes are made to configuration files. It is important to work to
minimize the attack surface and since these dashboards are managed through the
web, it is yet another point where your server can be compromised. Ultimately a
control panel could prove convenient both for an administrator and for someone
looking to hack into your system.

2) Immediately After Receiving Root Access
------------------------------------------

Hopefully the root password wasn't sent via an unencrypted email with the other
login credentials. Very few people use `GPG to encrypt emails`_ because it is
cumbersome, but confidential documents should be encoded/decoded with this type
of protection. You can request that the password not be sent using the same
medium so it will be difficult to intercept. At the very minimum, try to ensure
passwords are sent separately from the rest of the authentication data. This
provides a slightly more obscure means to stop this information from being
intercepted.  Ideally credentials would be sent with a tool similar to
NoteShred_ which can delete a password after it is viewed without leaving an
email archive of the information. However it is sent, change your password
immediately after receiving it.

Most web hosts send all of the credentials together, therefore, the first step
after getting access is to log in and change the root password. Unencrypted
email communications offers no security on the Internet and thus you must
address this vulnerability immediately.

Update the list of available software and perform system software upgrades.
Most web hosts will use a pre-packaged distribution and there will frequently be
updates that need to be applied immediately. Make sure you've got the updates
and that the new packages are running. If you update the Linux kernel you will
have to reboot the server for it to be applied. If you update Apache, you will
also need to restart it. Debian-style systems often restart the main daemon
instances on package updates automatically, where RHEL-style systems treat
daemon restarts as an administrator's responsibility.

::

  # Ubuntu/Debian
  $ apt-get update && apt-get dist-upgrade

  # CentOS
  $ yum upgrade

You will inevitably have a number of passwords to maintain. We recommend
storing these in a new `KeePass or KeePassX Password database`_. It has a nice
password generator which makes it very easy to generate long (25+ characters)
and complex passwords and store them immediately. If you get any other
passwords supplied via email, reset them immediately. Remember that your email 
address is also a `point of vulnerability`_.

The most common account that crackers try to compromise is the root user, so
disable root logins. Furthermore, set up user accounts with sudo access and `use
SSH keys`_ so that nobody accessing the server is using a password. Note: the
commands listed here assume you are using sudo access and but we have chosen not
to explicitly prefix them with sudo.

Protect your SSH keys by ensuring that your private keys are `password
protected and using at least 2048-bits encryption`_. Some people now think that 
the default should be 4096-bits, while really paranoid people may choose to use
8192-bits. Although theoretically there is nothing wrong with doing this, in 
practice there are `limitations` to what browsers and hosting companies provide. 
At the present time, 2048-bits seems sufficient for most use cases. 

By disabling the use of passwords for SSH user
logins, a common server vulnerability is simply eliminated. When you turn off
password logins, "`script kiddies`_\ " cannot compromise your server
with common dictionary or brute force attacks. There are explanations on how to
`effectively disable password logins`_ but check that
:file:`/etc/ssh/sshd_config` has the text

.. code-block:: ssh

  PasswordAuthentication no

Remember that when downloading important files there is a possibility that
they have been tampered with. Important security documents often come with a
`MD5`_ or `Secure Hash Algorithm`_ (SHA) code which allows a user to verify that
the file on a server is identical to the file that they have downloaded. You can
generate a `checksum`_ locally to determine equivalence using one of these::

  $ shasum -a 256 -/DrupalSecurity.epub
  $ md5sum -/DrupalSecurity.epub
  $ openssl sha1 -/DrupalSecurity.epub

3) Create a baseline
--------------------

Record a baseline of your server that you can review, knowing that this is the
minimum number of processes which are running with a clean system. Likewise,
record the baseline from a `netstat`_ report to see what ports are open::

  $ ps afx
  $ netstat -l -p -n

Record the list of installed packages on the server. Save this information in a
text file in your management code repository. If your server is compromised it
is useful to know what packages were installed and running when you started::

  # Ubuntu/Debian
  $ dpkg -l

  # CentOS
  $ yum list installed

Manage your ports through firewall settings: It is important to review and
document the firewall settings - open ports - to see that they are properly
restrictive. The firewall program for sysVinit OS versions (CentOS/RHEL <=6),
iptables, is still available for systemd OS versions (CentOS/RHEL >=7), which
by default uses firewalld.

Using iptables, the port settings can be listed from the command line with::

  $ iptables -L -vn

You can load/save the iptables easily using the iptables-persistent package
(installed on Debian/Ubuntu using ``apt-get install iptables-persistent``).
With that you can simply save the existing IP tables from the command line::

  # Ubuntu/Debian
  $ service iptables-persistent save

  # CentOS
  $ service iptables save

Install `Rootkit Hunter`_ (RKH) to help you "detect known rootkits, malware and
signal general bad security practices". You can set it up to `send you email
alerts`_, but can also do manual scans.

::

  # Ubuntu/Debian
  $ apt-get install rkhunter

  # CentOS
  $ yum install rkhunter

4) Limit Access from Outside
----------------------------

In general you will want to allow traffic for port 22 (for known IPs), 80, 443
and reject other ports. It can also be useful to use firewall rules to restrict
outgoing connections from the Apache user. The possible exception to this is
drupal.org's IP address as you will want to regularly use Drush (Drupal's
command line shell and scripting interface) to update modules (see H2 below).
You can easily see what ports are open by using a port scanner such as `nmap`_
from an external machine::

  $ nmap -sS SERVER_ADDRESS

We recommend running `periodic TCP port scans`_ on your server. `MXToolbox`_
offers an option to do this through their site, but you can also use tools like
nmap which offer more fine-grained controls.

Many servers come with `BIND`_ on UDP port 53. This program can probably be
removed in most instances or should be restricted with a firewall if required.
There are some `detailed instructions here`_ on how to remove it, which are
particularly important if you aren't sure if you need it or not. To check if
bind is running, run this from the command line::

  $ ps -Al | grep bind

  # sysVinit
  $ chkconfig grep bind

  # upstart
  $ service bind status

  # systemd
  $ systemctl is-enabled bind

You can obscure your SSH port by reassigning it to other than the default (22).
This might fool a lazy cracker who isn't using a port scanner first, but won't
stop the serious folks.

One of the best ways to limit SSH access to a server is to restrict access to a
handful of known subnets (ie. 192.168.1.0/24) where administrators actually
work. Don't be afraid to add to this list; make it easy for your people to work
wherever they need to. Security is not the enemy.

You can also `restrict who can SSH`_ into the server to a limited number of IP
addresses. Be very careful when configuring this as you don't want to block
yourself from accessing the server.

`Debian's admin documentation`_ offers the following changes which can be made
to the iptables firewall::

  # All connections from address 1.2.3.4 to SSH (port 22)
  $ iptables -A INPUT -p tcp -m state --state NEW --source 1.2.3.4 --dport 22 -j ACCEPT
  # Deny all other SSH connections
  $ iptables -A INPUT -p tcp --dport 22 -j DROP

There are many ways to do this. Debian uses `ufw`_, the sysVinit releases of
RHEL use `system-config-firewall-tui`_, `lokkit`_ is coming along nicely and
systemd releases RHEL 7 ship with `FirewallD`_ by default. Ultimately they all
do the same thing slightly differently. Make sure you understand your
configurations and review them regularly.

If you already have established a `virtual private network`_ (VPN) then you can
restrict SSH access to within that private network. This way you need to first
log in to the VPN before being able to access the port. Leveraging an existing
VPN has some additional costs but also some security advantages. If an
organization isn't already using a VPN however, then the usability problems
with forcing people to use it may encourage developers to find ways to
circumvent it. It is important to remember that a VPN is only as secure as the
individual servers on the VPN. If the VPN is shared with systems out of your
control, and the responsible Systems Administrators (Sysadmins) might be lax in
security, then your servers should be hardened as if on the public network.

5) Initial Installs
-------------------

There are some tools to harden your Linux system. The program `grsecurity`_
addresses a number of memory and permissions issues with the kernel.

`BastilleLinux`_ guides the administrator through an interactive process to
limit access on the server.

Mandatory Access Controls (MAC) policies can be managed through programs like
`SELinux`_ and `AppArmour`_, for high security environments. With Ubuntu, use
AppArmour as it comes installed by default. While AppArmour is often considered
inferior and less flexible than SELinux, there is no need to uninstall
it. AppArmour may impact other security tools and should not be used in
conjunction with SELinux.

With other distributions it is recommended to use SELinux (examples for
`SELinux on Debian`_ and
`SELinux on Red Hat`_)
as its rules were initially developed to meet NSA policies.

::

  # Debian (not Ubuntu)
  $ apt-get install perl-tk bastille selinux-basics selinux-policy-default auditd

Using a Host Based Intrusion Detection System (HIDS) such as the `OSSEC`_
HIDS is a good practice. You can find more information on the
projects, including tutorials and how-tos at `OSSEC's documentation`_. 
`Tripwire`_ and `Snort`_ are other IDSes which
monitor the integrity of core files and will alert you to suspicious activity
(see `Tripwire on CentOS`_ and `Tripwire on Debian`_). With any HIDS you
should make sure that secure IPs, such as your outgoing gateway, are whitelisted.

`Drupal monitoring can be set up to work with OSSEC`_ which would be more
efficient than using Drupal's `Login Security`_ module (6/7/8) as it would allow
you to use your existing HIDS infrastructure to alert you to these sorts of
attacks.

Crackers will often try to use a `brute force attack`_ to guess usernames and
passwords. Using a service like `Fail2ban`_ that can block IP addresses that 
are making an unreasonable number of login attempts. This won't prevent 
distributed attacks, but could be used in conjunction with OSSEC.

`Fail2ban is also an effective measure for flood control`_ and can stop most
denial of service (DoS) attacks. Drupal also has some built in flood control
options; The `Flood Control module`_ provides a UI to control them. Note that
some crackers are throttling their dictionary attacks to avoid tools like
Fail2ban, so it will still be important to use a monitoring tool like Nagios to
monitor if someone is methodically trying to guess bad passwords on your server.

::

  # Ubuntu/Debian
  $ apt-get install fail2ban

  # CentOS
  $ yum install fail2ban

`Distributed Denial of Service (DDoS)`_ attacks are more difficult to address,
but there's a great defence plan laid out on `StackOverflow`_.

Place the /etc directory under version control so that you can easily track
which configurations have changed. The program `etckeeper`_ automates this
process nicely and hooks into your package manager and cron to do its work when
your server is upgraded or new software is installed.

::

  # Ubuntu/Debian
  $ apt-get install etckeeper bzr && etckeeper init && etckeeper commit "initial commit"

  # CentOS
  $ yum install etckeeper && etckeeper init && etckeeper commit "initial commit"

Ubuntu comes with the `Ubuntu Popularity Contest`_ (popcon) to gather
statistics about which packages are used in the community. Although this is
anonymous, it can be a good idea to remove this package so that it is not a
potential weak link. This is an optional package that can be easily removed
without impacting your site's performance.

::

  # Ubuntu
  $ dpkg --purge popularity-contest ubuntu-standard

You will probably want to install an opcode cache and `Memcache`_ (or `Redis`_)
to ensure that your site is responding quickly. PHP 5.5+ now comes with built
in opcode cache, earlier versions of PHP can add this using `APC`_. Memcached
is a general-purpose distributed `memory caching`_ system. Both work to make
your server more responsive by minimizing the load on the server and improving
caching. This will help when there is an unexpected server load.

Aside from the performance advantages, there can be security improvements by
caching the public display. There are huge security advantages to restricting
access to the rendering logic (Drupal's admin) so that the public is only
interacting with a cache serving front end content. In using any caching
however, it is critical that only anonymous data is cached. A mis-configured
cache can easily `expose personal data to the public`_. This needs to be
carefully tested on sites which have private or confidential data.

There are a number of ways to cache the public display, including leveraging
Memcache and `Nginx`_ to extend Drupal's internal page cache. One of the most
powerful tools is `Varnish`_ which can provide incredible performance
enhancements. It can also be used effectively to deny all logins on your public
site by being configured to deny cookies on port 80. This is a line that can be
added to your Varnish vcl file in the `vcl_recv` subroutine to remove the
cookies so that it becomes impossible to login to Drupal directly:

.. code-block:: varnish

  if (req.http.host == "example.com") { unset req.http.Cookie;}

If you have a site which has only a few users and doesn't have any online forms
for anonymous users then you can configure Varnish to simply reject all HTTP
POST requests. Then in Apache you can whitelist the IP address you want to have
access to login to Drupal. Matt Korostoff documented this approach in his
`breakdown of the Drupalgeddon attacks`_ that affected many Drupal 7 sites.

Shared server environments provide a number of security challenges. Do not
expect it to be easy to securely host several sites on the same server with
direct shell access to different clients. If you need to do this, it is worth
investigating `FastCGI`_ which when used in conjunction with `suexec`_ or
`cgiwrap`_ to isolate individual processes on a shared server. We expect most
medium to large organizations to have access to either virtual (e.g. `VMware`_,
`Xen`_, `OpenVZ`_ or `KVM`_) or cloud-based (e.g. `Amazon`_ or `Rackspace`_)
servers. There is also `significant movement in the Drupal community`_ to use
`Linux Containers`_ to more efficiently distribute processing power without
compromising security.

.. image:: /_static/images/noun/noun_67380_cc.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: Shield from the noun project.

6) Server Maintenance
---------------------

Security requires constant vigilance. Someone should be tasked with ensuring
that the server is kept up-to-date at least weekly. This isn't usually a
complex task, but it does require that someone subscribe to the security update
mailing list for the distribution (e.g. `Ubuntu`_ and `CentOS`_), apply the
updates, and review the logs to ensure everything is still running properly.
Upgrades can be done with the following commands::

  # Ubuntu/Debian
  $ apt-get update && apt-get upgrade

  # CentOS
  $ yum upgrade

Note that this for Ubuntu/Debian you will want to manually use apt-get dist-upgrade
to address kernel updates. It is `more disruptive`_ than apt-get upgrade because 
it performs kernel upgrades, and may also install or remove packages. Important 
security fixes often occur in the kernel, and the server will require a reboot 
to take effect.  

It is very useful to have a service like `Nagios`_ monitoring your production
server to alert you if any problems arise. The configuration of Nagios can be
quite complex, but it can be setup alongside your web application or on a
dedicated monitoring server. You will need to grant access on your production
environment to this server and you must enable CGI access on this
server. Remember that if you enable this, you will also need to consider the
`security implications`_ that it presents. To get the server installed in your
environment, execute the following from the command line::

  # Ubuntu/Debian
  $ apt-get install nagios3 nagios-nrpe-plugin

And for each server you wish to monitor with Nagios::

  # Ubuntu/Debian
  $ apt-get install nagios-nrpe-plugin

`Munin`_ can be run on the production environment to give you a sense of the
relative load of various key elements over the past hour, day, week and month.
This can be useful when debugging issues with your server.

::

  # Ubuntu/Debian
  $ apt-get install munin munin-node

Access to this information is available through your web server but you will
want to configure your site to `ensure that this data is not publicly
available`_.

There are also many good reasons to use server `configuration management
software`_ like `Puppet`_ or `Chef`_. Initially, it will take you a lot more
time to configure it this way, but it will make it much easier to restore your
server when something does happen and and see you are back online quickly. It
also codifies the process to ensure that you don't miss critical setup steps.
This approach also makes it trivial to have essentially identical development,
staging and production environments.

7) Managing Server Logs
-----------------------

Your web server is a complex environment involving thousands of software
projects. Most of these will store log files in /var/log. If log files aren't
properly rotated and compressed they can become unmanageably large. If your
hard drive is filled up with old log files your site will simply stop
functioning. Most distributions of Linux come with `logrotate`_ configured
such that log files are segmented on a regular basis and the archive is
compressed so that space isn't a problem.

Most Linux distributions also come with syslog built in, which is critical for
doing security audits. You can also configure it to `send emergency messages to
a remote machine`_, or even send a duplicate of all log messages to an external
loghost. An experienced cracker will modify your log files to obscure their work,
once they have compromised your server.

There is a discussion in the Drupal section later on about how to
direct Watchdog messages to syslog. There are many tools to help system
administrators more effectively monitor their log files, and regular log
reviews can be an important part of early breach detection.

If your server is configured with a caching reverse proxy server or a load
balancer such as Varnish, Nginx or haproxy then you should ensure that Drupal is
made aware of the actual ``REMOTE_IP``. The common solution requires configuring
the ``X-Forwarded-For`` header in both Varnish and Apache, but as `Jonathan
Marcil's blog post points out`_, "X-Forwarded-For is actually a list that can be
a chain of multiples proxies and not just a single IP address". To that effect,
ensure that all IP addresses for your reverse proxies are identified in your
settings.php file (`configuration`_). Another solution would be to create a
custom HTTP header such as ``X-Remote-IP`` and tell Drupal to use it using the
configuration variable "reverse_proxy_header" in :file:`settings.php` under
"Reverse Proxy Configuration". Drupal itself will correctly manage a list of
trusted reverse proxies with this header. This is useful if you want to
correctly log IPs at a Web server, proxy or load balancer level. Note that the
reverse proxy should append the IP address of the client issuing the request
to this header.

.. code-block:: php

  $conf['reverse_proxy'] = TRUE;
  $conf['reverse_proxy_addresses'] = array('127.0.0.1','192.168.0.2');
  $conf['reverse_proxy_header'] = 'HTTP_X_REMOTE_IP';

Another approach to dealing with this is to simply use Apache's Reverse Proxy
Add Forward (RPAF) module. As Khalid Baheyeldin `writes in his blog`_, this
Apache module can be used for both Reverse Proxy and/or a Content Delivery
Network (CDN).

::

  # Ubuntu/Debian
  $ apt-get install libapache2-mod-rpaf

After editing :file:`/etc/apache2/mods-enabled/rpaf.conf` and setting your proxy
IP and restarting Apache, your access.log will show the real client IP rather
than that of your proxy.

The most important server logs to monitor are Apache's. If there is more than
one site on a given server, it is normal for each site to have its own log file
rather than using the default generic one. If you run more than one site or
have multiple web servers, log centralization can allow you to get an overall
view of site issues. Open-source tools such as `logstash`_ can be used to
simplify the process of searching all of your log files.

.. Neither of these attempts to insert a page break works, least with my tests.

.. raw:: html

   <div style="page-break-before:always;"></div>

.. raw:: latex

   \newpage

8) Rough Server Ecosystem Image
-------------------------------

   .. image:: _static/images/ServerEcosystem.*
     :alt: Generic server ecosystem 

.. _Ubuntu Popularity Contest: https://help.ubuntu.com/community/UbuntuPopularityContest
.. _10 major tenets of a secure hosting model: http://drupalwatchdog.com/2/2/securing-your-environment
.. _encrypted partition: https://wiki.archlinux.org/index.php/Disk_Encryption
.. _how to set up an encrypted drive: https://help.ubuntu.com/community/EncryptedFilesystemHowto
.. _Server Name Indication: http://en.wikipedia.org/wiki/Server_Name_Indication
.. _TLS certificates: https://en.wikipedia.org/wiki/Transport_Layer_Security
.. _Subject Alternative Name: https://en.wikipedia.org/wiki/SubjectAltName
.. _NoteShred: https://www.noteshred.com/
.. _GPG to encrypt emails: https://en.wikipedia.org/wiki/GNU_Privacy_Guard
.. _KeePass or KeePassX Password database: https://en.wikipedia.org/wiki/KeePass
.. _point of vulnerability: http://drupalwatchdog.com/2/2/practical-security
.. _use SSH keys: https://wiki.archlinux.org/index.php/SSH_Keys
.. _`password protected and using at least 2048-bits encryption`: https://www.ssllabs.com/downloads/SSL_TLS_Deployment_Best_Practices.pdf
.. _`limitations`: https://stackoverflow.com/questions/8453529/are-there-any-disadvantages-to-using-a-4096-bit-encrypted-ssl-certificate
.. _script kiddies: https://en.wikipedia.org/wiki/Script_kiddie
.. _Secure Hash Algorithm: https://en.wikipedia.org/wiki/Secure_Hash_Algorithm
.. _effectively disable password logins: http://lani78.wordpress.com/2008/08/08/generate-a-ssh-key-and-disable-password-authentication-on-ubuntu-server/
.. _MD5: http://www.electrictoolbox.com/article/linux-unix-bsd/howto-check-md5-file/
.. _checksum: https://en.wikipedia.org/wiki/Checksum
.. _netstat: https://en.wikipedia.org/wiki/Netstat
.. _Rootkit Hunter: http://sourceforge.net/apps/trac/rkhunter/wiki/SPRKH
.. _send you email alerts: http://www.tecmint.com/install-linux-rkhunter-rootkit-hunter-in-rhel-centos-and-fedora/
.. _nmap: http://nmap.org/
.. _periodic TCP port scans: https://en.wikipedia.org/wiki/Port_scanner
.. _MXToolbox: http://mxtoolbox.com/PortScan.aspx
.. _BIND: https://en.wikipedia.org/wiki/BIND
.. _detailed instructions here: http://askubuntu.com/questions/162371/what-is-the-named-daemon-and-why-is-it-running
.. _restrict who can SSH: http://apple.stackexchange.com/questions/34091/how-to-restrict-remote-login-ssh-access-to-only-certain-ip-ranges
.. _Debian's admin documentation: http://www.debian-administration.org/articles/87
.. _ufw: https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server
.. _system-config-firewall-tui: https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server
.. _lokkit: http://docs.saltstack.com/en/latest/topics/tutorials/firewall.html
.. _FirewallD: https://fedoraproject.org/wiki/FirewallD
.. _virtual private network: https://en.wikipedia.org/wiki/Virtual_private_network
.. _grsecurity: http://olex.openlogic.com/packages/grsecurity
.. _BastilleLinux: https://help.ubuntu.com/community/BastilleLinux
.. _SELinux: https://en.wikipedia.org/wiki/Security-Enhanced_Linux
.. _AppArmour: https://en.wikipedia.org/wiki/AppArmor
.. _SELinux on Debian: https://wiki.debian.org/SELinux
.. _SELinux on Red Hat: https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Security-Enhanced_Linux/
.. _OSSEC: http://www.ossec.net/
.. _OSSEC's documentation: http://www.ossec.net/?page_id=11
.. _Tripwire: http://www.tripwire.com/
.. _Snort: http://www.snort.org/
.. _Tripwire on CentOS: https://www.centos.org/docs/2/rhl-rg-en-7.2/ch-tripwire.html
.. _Tripwire on Debian: http://penguinapple.blogspot.ca/2010/12/installing-configuring-and-using.html
.. _Drupal monitoring can be set up to work with OSSEC: http://www.madirish.net/428
.. _Login Security: https://drupal.org/project/login_security
.. _brute force attack: http://en.wikipedia.org/wiki/Brute-force_attack
.. _Fail2ban: http://www.fail2ban.org/wiki/index.php/Main_Page
.. _Fail2ban is also an effective measure for flood control: http://www.debian-administration.org/article/Blocking_a_DNS_DDOS_using_the_fail2ban_package
.. _Flood Control module: https://drupal.org/project/flood_control
.. _Distributed Denial of Service (DDOS): https://en.wikipedia.org/wiki/Denial-of-service_attack
.. _StackOverflow: http://stackoverflow.com/questions/14477942/how-to-enable-ddos-protection
.. _etckeeper: https://help.ubuntu.com/12.04/serverguide/etckeeper.html
.. _Memcache: http://memcached.org/
.. _Redis: http://redis.io/
.. _APC: http://php.net/manual/en/book.apc.php
.. _memory caching: https://en.wikipedia.org/wiki/Memory_caching
.. _expose personal data to the public: https://speakerdeck.com/owaspmontreal/demystifying-web-cache-by-kristian-lyngstol#24%20
.. _Nginx: http://wiki.nginx.org/Main
.. _Varnish: https://www.varnish-cache.org/
.. _breakdown of the Drupalgeddon attacks: http://mattkorostoff.com/article/I-survived-drupalgeddon-how-hackers-took-over-my-site
.. _FastCGI: http://www.fastcgi.com/drupal/
.. _suexec: https://httpd.apache.org/docs/current/suexec.html
.. _cgiwrap: http://cgiwrap.sourceforge.net/
.. _VMware: http://www.vmware.com/
.. _Xen: http://www.xenserver.org/
.. _OpenVZ: http://openvz.org/
.. _KVM: http://www.linux-kvm.org/
.. _Amazon: https://aws.amazon.com/ec2/
.. _Rackspace: http://www.rackspace.com/cloud/
.. _significant movement in the Drupal community: https://www.getpantheon.com/blog/why-we-built-pantheon-containers-instead-virtual-machines
.. _Linux Containers: https://en.wikipedia.org/wiki/LXC
.. _Ubuntu: http://www.ubuntu.com/usn/
.. _CentOS: https://www.centos.org/modules/tinycontent/index.php?id=16
.. _Nagios: http://www.nagios.org/documentation
.. _`more disruptive` http://askubuntu.com/questions/81585/what-is-dist-upgrade-and-why-does-it-upgrade-more-than-upgrade
.. _security implications: http://nagios.sourceforge.net/docs/3_0/security.html
.. _Munin: http://munin-monitoring.org/
.. _ensure that this data is not publicly available: http://www.howtoforge.com/server_monitoring_monit_munin
.. _configuration management software: https://en.wikipedia.org/wiki/Software_configuration_management
.. _Puppet: http://projects.puppetlabs.com/projects/puppet
.. _Chef: https://www.chef.io/
.. _logrotate: http://www.cyberciti.biz/faq/how-do-i-rotate-log-files/
.. _send emergency messages to a remote machine: http://www.linuxvoodoo.com/resources/howtos/syslog
.. _Jonathan Marcil's blog post points out: https://blog.jonathanmarcil.ca/2013/09/remoteaddr-and-httpxforwardedfor-bad.html
.. _configuration: https://github.com/drupal/drupal/blob/7.x/sites/default/default.settings.php#L358
.. _writes in his blog: http://2bits.com/articles/correct-client-ip-address-reverse-proxy-or-content-delivery-network-cdn.html
.. _logstash: http://logstash.net/
