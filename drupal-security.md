#Drupal Security Best Practices

##A Guide for Governments and Nonprofits

[OpenConcept Consulting Inc.](http://openconcept.ca)

for Public Safety Canada

**Author:** Mike Gifford <mike@openconcept.ca>

Contributors: [Mike Mallett](mailto:mike.mallett@openconcept.ca), [Matt Parker](https://drupal.org/user/536298), [Michael Richardson](http://www.sandelman.ottawa.on.ca), [Colan Schwartz](http://colans.net), [Mack Hardy](http://affinitybridge.com), [Peter Cruickshank](http://spartakan.wordpress.com), [David Norman](http://dkn.me)

Editor: [Lee Hunter](http://streamoflight.com)
Copyright

All of the documentation will be licensed under a Open Government Licence as specified [http://www.data.gc.ca/eng/open-government-licence-canada](http://www.data.gc.ca/eng/open-government-licence-canada)

##Executive summary

This document describes best practices for setting up and maintaining a Drupal site. It was written for the Government of Canada, but nothing in it is specific to this government and it is very applicable to other institutions.

Drupal is a very popular, open source Content Management System (CMS). This software has a strong security model, but when considering the security of a site an organization needs to be aware of the dangers of not following a good process. Furthermore, Drupal is only one piece of software that is required to run your site, and one needs to consider the security of the entire server ecosystem. 

This is not a comprehensive document, as IT security is a complex field. We have tried to focus on broad areas to help explain the importance and approaches to improving security. We have included many great many links and expect that people will learn more about the tools that we have listed here. 

We do not believe that there will ever be a 100% secure system. There are always bugs in software and we know that new types of exploits are being found all of the time. We are listing options to consider, but each organization will need to weigh which combination they are going to use. 

* * *

Table of Contents

[A) Introduction](#h.19qn4o9ywl2m)
[B) Principles of Security](#h.ukqsl2tynfw0)
[C) Security Concerns for Managers](#h.s50irw3ya70g)
[D) Server Security](#h.nvjrk93bljm)
[1) Server Procurement](#h.rg9d8qfce5zg)
[2) Immediately After Receiving Root Access](#h.wxcaky74d4hy)
[3) Create a baseline](#h.eqsmgza24y5y)
[4) Limit Access from Outside](#h.1jvwdjrtfu3q)
[5) Initial Installs](#h.he6xlv2uh62u)
[6) Server Maintenance](#h.uyeqdvv49frk)
[7) Rough Server Ecosystem Image](#h.vloxxge9ctm6)
[E) Web Servers](#h.24gyzut4g23k)
[1) Restricting Access](#h.b37vrs21nf1u)
[2) Removing Code](#h.p4ggcy9w42g3)
[3) HTTP Headers](#h.5ol237ynhdat)
[4) Everything Else](#h.hadcq2by8twm)
[F) PHP](#h.3odnlb3ajk67)
[G) Database (MySQL or PostgreSQL)](#h.i3kbhcef0ahy)
[H) Drupal](#h.vad7g6avxqyl)
[1) Files](#h.6rwu2kak7ahu)
[2) Drush](#h.et4rtt4kce1d)
[3) Errors](#h.25i5f3e5hd40)
[4) Administration](#h.hxl2rx59qwwq)
[5) Modules](#h.cta0oynqirm9)
[6) Drupal Distributions](#h.p5vmcjoul74n)
[7) Miscellaneous](#h.ah6yjrglmjxx)
[I) Development, Staging and Production](#h.uyfzjzo2ltbd)
[J) Regular Maintenance](#h.6ahtub6x6lew)
[K) Additional Resources](#h.luzvx0idfxkl)
[1) General guidelines](#h.atocboqzzej2)
[Drupal security](#h.ar888adv4p3t)
[Secure hosting](#h.qdfmqlcqriuw)
[2) Videos](#h.m3pikacc9uej)
[3) Third party tools](#h.5u8uaasc0pcz)
[4) Books](#h.ljars6xxqnnx)

* * *

# <a name="h.19qn4o9ywl2m"></a>A) Introduction

Drupal 7 is a leading Content Management System, particularly in the Government of Canada. It is widely used by governments around the world who are looking to meet increasing citizen demands, larger challenges with accessibility and mobile requirements, and ever smaller budgets.

With governments increasingly targeted for cyber attacks, it is important that best practices are kept up-to-date so that personal information and government assets are protected.

This guide provides an overview of important security principles, best practices for basic security; plus extra steps to be considered, if budget allows. Where possible we will be providing some detailed instructions. Managers should read sections B and C. System Administrators will need to focus on sections D, E, F, G, I & J. Drupal developers can focus on section H, but should be familiar with the impact of the other sections too. 

It should be clear that not all of the steps outlined here will need to be taken on all sites. The principles should be followed but not all of the security suggestions described will need to be followed by all organizations. Each practice or tool should be carefully evaluated to understand the potential costs, risks and benefits. 

This document raises issues to consider before you procure a server and when you first gain access to your server. It provides suggestions on what additional software you can add to your site which can help improve it’s security. It also highlights configuration options that you can add to Apache, PHP & MySQL to improve the initial defaults. Finally we talk about things that you can do to enhance Drupal’s security.

The code snippets which are included are not always a comprehensive guide, but there are always links in the descriptive paragraph with more information which you should consult before installing programs on your live server. 

For information on building secure modules and themes, see the documentation on Drupal.org. This document strongly recommends against the use of Microsoft Windows servers for Internet-facing web sites. Windows security will not be addressed.

Security cannot be just a buzzword, [it is a process](https://www.schneier.com/essay-062.html). There needs to be clear understanding about lines of responsibility and ultimately management needs to provide the budget required to ensure that systems can be maintained and regularly re-evaluated. 

Eternal vigilance is important as those searching for your vulnerabilities are working around the clock and are well financed. This document will, itself, need to evolve to keep pace with new vulnerabilities. 

* * *

# <a name="h.ukqsl2tynfw0"></a>B) Principles of Security

1. There is Safety in the Herd: Leverage large, well maintained open source libraries (packages) with a critical mass of users and developers. Use compiled packages and check data integrity of downloaded code. Start with a standard Debian/Ubuntu or RedHat/CentOS installation. 
3. Order Matters: Don’t open up services to the Internet before your server is properly secured.
5. Limit Exposure: Only install and maintain what is necessary. Reduce the amount of code installed. Review server configuration regularly to see if it can be streamlined.
7. Deny Access by Default: Only allow access where it is needed, and make all access policies deny by default. 
9. Use Well Known Security Tools:There are well supported libraries that limit exposure, and check for intrusion. Suggestions are provided later.
11. Avoid Writing Custom Code: Even large government departments don’t invest properly in regular, ongoing code reviews. Minimize the use of any custom code.
13. Contribute Back: No software is ever perfect. There is always room for improvement. Make the code you use better and give it back to the community.If you do it it properly you won’t have to rewrite your code with the next security release and you will get free peer review and ongoing maintenance.
15. Limit Access: There need to be clear, documented roles of who has access to what. Only use setup and use sudo when root access is required. Isolate distinct roles where possible. Everyone with access needs their own account, shared accounts are insecure.
17. Make Your Application Happy: When running smoothly your server should not be generating errors. Monitor your server then investigate and resolve errors.
19. Document Everything: Make sure you have an overview of any customizations which may have been done or any additional software that may have been added. 
21. Limit Use of Passwords:Have sane organizational policies on password requirements. Keep track of your passwords in controlled, encrypted programs. Where possible use passwordless approaches such as ssh key pairs which are more secure.<sup>[[a]](#cmnt1)</sup>
23. Don’t Trust Your Backup: Define, review procedures and do test that you can restore your site regularly. 
25. Obscurity isn’t Security: Organizations need to have their security policies well documented and internally transparent. Section K discusses this issue in detail.
27. Security is Big: It is a mistake to assume that one person can do it well in isolation. Having access to a team (even outside of the organization) will help. 
29. Remember, You’re Still Not Safe:Have an audit trail stored on another system. If your site is compromised, take the time to find out how. Use proper version control for all code and configuration.
31. Not Just for Techs: Upper management needs to take the time to understand these general principles of IT security as they have profound implications to the work of the whole organization.

# <a name="h.s50irw3ya70g"></a>C) Security Concerns for Managers

There are many assumptions about IT security that need to be fundamentally rethought in the era of the Internet. Government is struggling to come to terms with this at the same time as working to understand the implication of cloud based services. What we can be certain of is that this field is accelerating and government departments need to keep up. 

The first principle is to understand that time corrodes security and on the Internet time moves very fast. You can’t assume that any service you buy or develop is currently secure or will remain that way for long. It is critical to understand what investments have been made and how they are maintained.

Web hosting and application development are different fields and one cannot simply outsource security upgrades to someone else to do. Neither Shared Services Canada (SSC) nor a private web hosting company can simply take care of your server in isolation of the application that is running on it. Ultimately, someone familiar with your website and it’s content needs to be involved in performing upgrades.

One person working in isolation cannot be expected to be an expert in all aspects of security.<sup>[[b]](#cmnt2)</sup> It’s important that your security person has ongoing training and is engaged with both the Drupal and wider security communities to keep up with the latest threats, vulnerabilities and mitigation strategies.

Schedule time for a skilled security expert outside the core team to double check the server/Drupal configuration every quarter. This doesn’t have to be a consultant, but it should be someone outside of the website development team. 

Everyone wants security to be simple, it isn’t. It’s a matter of determining, as an organization, how much risk you want to be exposed to. You can invest as much or as little on security as you want, but the risks are generally inversely proportional to resources spent on tightening your system. Security has costs as well as benefits. Complex systems are usually less secure because it costs relatively so much more to secure them.<sup>[[c]](#cmnt3)</sup>

As with most work, a great deal of security work lies in identifying and eliminating assumptions. Document what is done, and be transparent in your work so that your organization knows that it has the level of risk it wants to maintain. 

A great deal of security work begins before anything is installed. Properly considering security first is important because it removes the security evaluation of the base system from the critical path later in deployment. When setup is rushed, bad practices are often used and become patterns which are continued long after the site is launched. 

* * *

# <a name="h.nvjrk93bljm"></a>D) Server Security

Any website is a complex ecosystem of software. Each aspect can be tightened down more through proper configuration and additional software than it comes with initially. This document provides some examples, but mostly relies on links so that you can read the specific details on how this should be done. There are other lists of considerations for Server Security, like Robert Hansen’s list of [10 major tenants of a secure hosting model](http://drupalwatchdog.com/2/2/securing-your-environment), but where possible I will be referring back to the list above.

## <a name="h.rg9d8qfce5zg"></a>1) Server Procurement

Start server documentation with the information about the original parameters of your server contract. There are often technical details and notes about who to contact when things go wrong.

It is important to determine that there is a strong security community behind the distribution you choose, and that you have the necessary human resources in your department to maintain it. OpenConcept prefers either Debian/Ubuntu, but RedHat/CentOS are really solid as well. The advantage of a Debian- or RedHat-based solution is that there is extensive documentation and large communities of users who’ve shared their experiences through forums, issue trackers, and blog posts. Ubuntu is based on Debian, CentOS is based on RedHat, any references to one or the other should be interchangeable. 

If you use a Red Hat Enterprise Linux (RHEL) system, you will need to have subscription to their service in order to apply security upgrades and install the additional packages mentioned in this document. Before procuring a RedHat server, check that your package includes a subscription. 

In our opinion, distributions of Linux like SuSE simply do not have a critical mass of users and developers to maintain the code and documentation required for a secure environment. Microsoft Windows is not a standard platform for hosting Drupal and is generally frowned upon. Community support for hosting on Windows is sparse and is therefore not recommended. It is very difficult to limit exposure on a Windows Server since there are many unneeded pieces of the operating system which you cannot easily uninstall. 

If you are worried about the server’s physical security, you can also set up an [encrypted partition](https://wiki.archlinux.org/index.php/Disk_Encryption) on your hard drive. This may introduce performance issues which might cause problems for your server. This document will not be covering [how to set up an encrypted drive](https://help.ubuntu.com/community/EncryptedFilesystemHowto) but depending on the perceived threats, it may be worth implementing. 

When enabling encrypted traffic using HTTPS, it is important to know how many domain names you will be hosting on a single web server. Each domain needs its own certificate. Although it is [no longer required](https://www.digicert.com/ssl-support/apache-multiple-ssl-certificates-using-sni.htm), often each certificate will have its own IP address.It is common to have any number of unencrypted HTTP sites hosted on a single IP address.

Finally, don’t get a server that comes with a server admin control panel. They promise to make managing your site easier but present security problems. There are a number of commercial packages, like cPanel or PLESK, that do make it easier to change settings on your site. This seems particularly attractive if less technical users are responsible for server administration. Our recent experience with cPanel, made it difficult to apply many of the suggestions described here. Because you can’t simply disable cPanel, we had to reinstall the site on a new server. If you choose a server with one, you will need to experiment with which of the following suggestions you are able to implement. Some control panels are also known to overwrite settings that are made to config files. It is important to work to minimize the attack surface and as these dashboards are managed through the web, it is yet another point where your server can be compromised. Ultimately a control panel could prove convenient both for you and for those looking to hack into your system.<sup>[[d]](#cmnt4)</sup>

## <a name="h.wxcaky74d4hy"></a>2) Immediately After Receiving Root Access

Hopefully the root password wasn’t sent via an unencrypted email with the other login credentials. Very few people use [GPG to encrypt emails](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) because it is cumbersome, but confidential documents should be encoded/decoded with this type of protection. You can request that that the password not be sent using the same medium so it will be difficult to intercept. Minimally passwords can be sent in a separate email, but this provides only a slightly more obscure means to stop this information from being intercepted. 

Most web hosts send all of the credentials together, therefore, the first step after getting access is to log in and change the root password. Unencrypted email communications offers no security on the Internet and thus you must address this vulnerability immediately. 

Update the list of available software and perform system software upgrades. Most web hosts will use a pre-packaged distribution and there will frequently be updates that need to be applied. Make sure you’ve got them.

Debian: apt-get update && apt-get upgrade

CentOS: yum upgrade

You will inevitably have a number of passwords to maintain. We recommend storing these in a new [KeePass Password database](http://keepass.info/). It has a nice password generator which makes it very easy to generate long (20+ characters) and complex passwords and store them immediately. If you get any other passwords supplied via email, reset them immediately. Your email address is also a [point of vulnerability](http://drupalwatchdog.com/2/2/practical-security).

The most common account that crackers<sup class="c11">[[1]](#ftnt1)</sup> try to compromise is the root user, so disable root logins. Furthermore, set up user accounts with sudo access and [use ssh keys](https://wiki.archlinux.org/index.php/SSH_Keys) so that nobody accessing the site is using a password. Protect your ssh keys by ensuring that your private keys are [password protected and using 2048-bits](https://www.ssllabs.com/downloads/SSL_TLS_Deployment_Best_Practices_1.0.pdf). By disabling the use of passwords for ssh user logins a common server vulnerability is simply eliminated. When you turn off password logins [script kiddies](https://en.wikipedia.org/wiki/Script_kiddie) simply cannot compromise your server with common dictionary or bruit force attacks. There are explanations on how to [effectively disable password logins](http://lani78.wordpress.com/2008/08/08/generate-a-ssh-key-and-disable-password-authentication-on-ubuntu-server/) but check that /etc/ssh/sshd_config has the text PasswordAuthentication no

## <a name="h.eqsmgza24y5y"></a>3) Create a baseline

Record a baseline of your server that you can review, knowing that this is the minimum number of processes which are running with a clean system. Likewise record the baseline from a netstat report to see what ports are open:

ps afx

sudo netstat -l -p -n

The management of ports on the network is managed through IPTables. It is important to review and document them to see that they are properly restrictive. From the command line you can list them with:

iptables -L -v -n

You can load/save the IPTables easily using the iptables-persistent package `sudo apt-get install iptables-persistent`. With that you can simply save the existing IP tables from the command line:

Debian: service iptables-persistent save
CentOS: service iptables save

Record the list of installed packages on the server. Save this information in a text file in your management code repository. If your server is compromised it is useful to know what packages were installed and running when you started:

Debian: dpkg -l

CentOS: yum list installed

## <a name="h.1jvwdjrtfu3q"></a>4) Limit Access from Outside

In general you will want to allow traffic for port 22 (for known IPs), 80, 443 and reject other ports. It can also be useful to use firewall rules to restrict outgoing connections from the Apache user. The possible exception to this is drupal.org’s IP address as you will want to regularly use drush (Drupal’s command line shell and scripting interface) to update modules (see H2 below). You can easily see what ports are open by using a port scanner such as [nmap](http://nmap.org/) from an external machine:

nmap -sS SERVER_ADDRESS
We recommend running [periodic TCP port scans](https://en.wikipedia.org/wiki/Port_scanner) on your server. [MXToolbox](http://mxtoolbox.com/PortScan.aspx) offers an option to do this through their site, but you can also use tools like nmap which offers you more fine-grained controls.

Many servers come with [BIND](https://en.wikipedia.org/wiki/BIND) on UDP port 53\. This program can probably be removed in most instances or should be restricted with a firewall if required. There are some [detailed instructions here](http://askubuntu.com/questions/162371/what-is-the-named-daemon-and-why-is-it-running) on how to remove it, which are particularly important if you aren’t sure if you need it or not. To check if bind is running, run this from the command line:
ps -Al | grep bind

chkconfig | grep bind

You can obscure your SSH port by reassigning it to other than the default (22). This might fool a lazy cracker who isn’t using a port scanner first, but won’t stop the serious folks. 

One of the best ways to limit ssh access to a server is to restrict access to a dozen or so /24 networks where administrators actually work. Don't be afraid to add to this list; make it easy for your people to work wherever they need to. Security is not the enemy.

You can also [restrict who can ssh](http://apple.stackexchange.com/questions/34091/how-to-restrict-remote-login-ssh-access-to-only-certain-ip-ranges) into the server to a limited number of IP address. Be very careful when configuring this as you don’t want to block yourself from accessing the server. [Debian’s admin documentation](http://www.debian-administration.org/articles/87) offers the following changes which can be made to the iptables firewall:

# All connectsion from address 1.2.3.4 to SSH (port 22)
iptables -A INPUT -p tcp -m state --state NEW --source 1.2.3.4 --dport 22 -j ACCEPT

# Deny all other SSH connections
iptables -A INPUT -p tcp --dport 22 -j DROP

If you already have established a [Virtual Private Network](https://en.wikipedia.org/wiki/Virtual_private_network) (VPN) then you can restrict SSH access to within that private network. This way you need to first login to the VPN before being able to access the port. Leveraging an existing VPN has some additional costs but also some security advantages. If an organization isn’t already using a VPN however, then the usability problems with forcing people to use it may encourage developers to find ways to circumvent it. 

## <a name="h.he6xlv2uh62u"></a>5) Initial Installs

There are some tools to harden your Linux system. The program [grsecurity](http://olex.openlogic.com/packages/grsecurity) addresses a number of memory and permissions issues with the Kernel. [SELinux](http://wiki.debian.org/SELinux/Setup) provides support for [mandatory access controls](https://en.wikipedia.org/wiki/Mandatory_access_control) (MAC) policies, such as those required by the [United States Department of Defense](https://en.wikipedia.org/wiki/United_States_Department_of_Defense).[BastilleLinux](https://help.ubuntu.com/community/BastilleLinux) guides the administrator through an interactive process to limit access on the server. NOTE: Ubuntu, which is a Debian-based distribution, relies on the [Debian SELinux policies](https://wiki.debian.org/SELinux). See the [Ubuntu Wiki](https://wiki.ubuntu.com/SELinux) for more information. 

Debian: apt-get install perl-tk bastille selinux-basics selinux-policy-default auditd

It isn’t currently recommended to add the security tool[AppArmour](https://wiki.ubuntu.com/AppArmor)as it often can interfere with other security enhancements. If it is not installed by default by your Linux distribution, adding it may conflict with other security programs. AppArmour is installed by default by Ubuntu and there is no need to uninstall it, but it is important to be aware that other security tools will probably be affected by AppArmour’s settings. 

Using an intrusion detection system such as [OSSEC](http://www.security-marathon.be/?p=544) Host-based Intrusion Detection System (HIDS) or [PHPIDS](http://www.phpids.org/) (PHP-Intrusion Detection System) is a good practice. There are good how-to documents available for both [PHPIDS](http://www.howtoforge.com/intrusion-detection-for-php-applications-with-phpids) and [OSSEC](http://www.ossec.net/?page_id=11). [Tripwire](http://www.tripwire.com/) and [Snort](http://www.snort.org/) are other IDS’s which monitor the integrity of core files and will alert you to suspicious activity (available for [CentOS](https://www.centos.org/docs/2/rhl-rg-en-7.2/ch-tripwire.html) and [Debian](http://penguinapple.blogspot.ca/2010/12/installing-configuring-and-using.html)). 

Crackers will often try to use a [brute force attack](http://en.wikipedia.org/wiki/Brute-force_attack) to guess usernames and passwords. Using a service like [Fail2ban](http://www.fail2ban.org/wiki/index.php/Main_Page) can block IP addresses that are making an unreasonable number of login attempts. This won’t prevent distributed attacks, but could be used in conjunction with OSSEC. [Fail2ban is also an effective measure for flood control](http://www.debian-administration.org/article/Blocking_a_DNS_DDOS_using_the_fail2ban_package) and can stop most denial of service attacks. Distributed denial of service attacks (DDoS) are more difficult to address, but there’s a great defense plan laid out on [StackOverflow](http://stackoverflow.com/questions/14477942/how-to-enable-ddos-protection).

Debian: apt-get install fail2ban

CentOS: yum install fail2ban

Place the /etc directory under Version Control so that you can easily track which configurations have changed. The program [etckeeper](https://help.ubuntu.com/12.04/serverguide/etckeeper.html) automates this process nicely and hooks into your package manager and cron to do its work when your server is upgraded or new software installed. 

Debian: apt-get install etckeeper bzr && etckeeper init && etckeeper commit "initial commit" 

CentOS: yum install etckeeper && etckeeper init && etckeeper commit "initial commit"

You will probably want to install [APC](http://php.net/manual/en/book.apc.php)and [Memcache](http://memcached.org/) (or [Redis](http://redis.io/)) to ensure that your site is responding quickly. APC is a PHP bytecode compiler and Memcached is a general-purpose distributed [memory caching](https://en.wikipedia.org/wiki/Memory_caching) system. Both work to make your server more responsive by minimizing the load on the server and improving caching. This will help when there is an unexpected server load. 

Aside from the performance advantages, there can be security improvements by using [Varnish](https://www.varnish-cache.org/) or Memcache to cache the public display. There are huge security advantages to restricting access to the rendering logic (Drupal’s admin) so that the public is only interacting with a cache serving front end content.

Note if you are going to be hosting several sites on the same server and want to give different clients access to their site on that server it would be worth investigating [FastCGI](http://www.fastcgi.com/drupal/) to isolate individual processes from a shared server. We expect most government departments to have access to either a virtual (ex: [Xen](http://www.xenserver.org/)) or cloud based (ex: [Amazon EC2](https://aws.amazon.com/ec2/)) server.

## <a name="h.uyeqdvv49frk"></a>6) Server Maintenance

Security requires constant vigilance. Someone should be tasked with ensuring that the server is kept up-to-date at least weekly. This isn’t usually a complex task, but it does require that someone subscribe to the security update mailing list for the distribution (e.g. [Ubuntu](http://www.ubuntu.com/usn/) and [CentOS](https://www.centos.org/modules/tinycontent/index.php?id=16)), apply the updates, and review the logs to ensure everything is still running properly. Upgrades can be done with the following commands:

Debian: apt-get update && apt-get upgrade 

CentOS: yum upgrade

It is very useful to have a service like [Nagios](http://www.nagios.org/documentation) monitoring your production server to alert you if any problems arise. The configuration of Nagios can be quite complex, but you can set it up easily enough on your staging server. You will need to grant access on your production environment to this server and you must enable CGI access on this server. To get the server installed in your staging environment, execute the following from the command line:

Debian: sudo apt-get install nagios3 nagios-nrpe-plugin

And for each server you wish to monitor with Nagios:

Debian: sudo apt-get install nagios-nrpe-plugin

[Munin](http://munin-monitoring.org/) can be run on the production environment to give you a sense of the relative load of various key elements over the past hour, day, week and month. This can be useful when debugging issues with your server. 

Debian: apt-get install munin munin-node

Access to this information is available through your web server but you will want to configure your site to [ensure that this data is not publicly available](http://www.howtoforge.com/server_monitoring_monit_munin). 

## <a name="h.u7nsyk6u932q"></a>

## <a name="h.hcnjqcsr28uu"></a>7) Rough Server Ecosystem Image

# <a name="h.roklumaqj9vx"></a>![](images/image01.png)<sup>[[e]](#cmnt5)</sup>

# <a name="h.a3bhnhop6kmk"></a>

# <a name="h.9t71nwz3xj04"></a>

* * *

# <a name="h.577rlnt69j06"></a>

# <a name="h.24gyzut4g23k"></a>E) Web Servers 

Apache has a number of modules that can be installed to tighten security of the web server. We recommend installing [ModSecurity and mod_evasive](http://www.thefanclub.co.za/how-to/how-install-apache2-modsecurity-and-modevasive-ubuntu-1204-lts-server). This can be set to leverage the Open Web Application Security Project's (OWASP) ModSecurity Core Rule Set. 

Debian: apt-get install libapache2-mod-evasive libapache2-modsecurity
CentOS: yum install mod_evasive mod_security

There are also Apache modules like [Project Honey Pot](https://www.projecthoneypot.org/httpbl_download.php) that make it harder for people to hack your system. Honey Pot can also be [installed on Drupal](https://drupal.org/project/httpbl), but Apache is often more efficient at addressing attacks like this before it hits PHP

Debian: apt-get install mod_httpbl

CentOS: yum install mod_httpbl

 All files and directories in your DocumentRoot should be editable by a non-root user, and should also not be writable by the Apache user, except the Drupal files/ directory. Please refer to Drupal’s [Securing file permissions and ownership](https://drupal.org/node/244924) for the complete discussion.

[suPHP](http://www.suphp.org/) is a tool which runs PHP scripts with the permissions of their owners; letting you "sandbox" a PHP application and simplifying file/folder permissions. Be careful to configure both the UNIX user account and suPHP properly. It should not be possible to CHOWN a file to another user with higher privileges, and you should restrict which users suPHP can run scripts as.

SSL versions 2 and 3 are no longer recommended according to the [SSL/TLS Deployment Best Practices](https://www.ssllabs.com/projects/best-practices/). Change the web server SSL configuration to permit only TLS v1.2 and higher. Check if the[ SSL services employ only AES](http://www.thinkwiki.org/wiki/AES_NI) with key lengths 128 bits and higher. You can install [GnuTLS](https://help.ubuntu.com/community/GnuTLS) from the command line to enable this:

Debian: sudo apt-get install gnutls-bin

There is a collection of configuration scripts on GitHub which provides examples of [hardened configuration files for SSL/TLS services](https://github.com/ioerror/duraconf). In the Apache config you can [set hardened SSL configurations for the HTTPS protocol](http://blog.ivanristic.com/2013/08/configuring-apache-nginx-and-openssl-for-forward-secrecy.html) with:

SSLProtocol All -SSLv2 -SSLv3

SSLHonorCipherOrder on
SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW BEAST attack!3DES !MD5 !EXP !PSK !SRP !DSS"

After restarting Apache, you can check the SSL information in a browser by double clicking on the lock icon in the address bar on https:// sites to get information on the encryption channel and confirm it’s using TLS.

At this point you can test your SSL configuration through [Qualys SSL Labs’ Server Test](https://www.ssllabs.com/ssltest/). This is a free online service performs a deep analysis of the configuration of any SSL web server on the public Internet. This will grade your SSL compliance and do things like confirm that you are using the latest version of TLS and verify that you are protected from [BEAST attacks](https://en.wikipedia.org/wiki/Transport_Layer_Security#BEAST_attack).

On your staging/dev server it is fine to provide a [self signed SSL certificate](https://en.wikipedia.org/wiki/Self-signed_certificate) to ensure that the traffic is encrypted. Setting up a 3rd party verified SSL certificate on your production environment will be important as otherwise your users will be asked to verify the exception when accessing the HTTPS version of your site. A listing of certificate authorities is available at the bottom of [this wikipedia page](https://en.wikipedia.org/wiki/Certificate_authority#External_links). You can review the validity of your SSL certificate through a free [SSL Test constructed by SSLLabs](https://www.ssllabs.com/ssltest/) or with the following openssl command:

openssl s_client -connect SERVER:443

To check a specific protocol using openssl:

openssl s_client -connect SERVER:443 -ssl2

openssl s_client -connect SERVER:443 -ssl3

## <a name="h.b37vrs21nf1u"></a>1) Restricting Access

Another useful Apache module is [mod_authz_host](https://httpd.apache.org/docs/2.2/mod/mod_authz_host.html) which can restrict access to /user , /admin and node/*/edit . It can also restrict access to non-production environments which should always be secured from both the search engines and especially from crackers. 

Example Apache configuration using mod_authz_host:

<Location ~ “/node/.*/edit”>

 Order Deny,Allow

 Deny from all

 Allow from 206.47.13.64 174.142.104.53 99.241.125.191

</Location>

Example Apache configuration using mod_rewrite:

<IfModule mod_rewrite.c>

 RewriteEngine on

 # Allow only internal access to admin

 RewriteCond %{REMOTE_ADDR} !^(206\.47\.13\.64|174\.142\.104\.53|99\.241\.125\.191)$

 RewriteRule ^admin/.* - [F]

</IfModule>

Drupal has a number of processes that can be triggered by URLs. You may wish to block some of these using Apache so that they simply cannot be loaded from the web browser. Common processes to secure are update, install and cron which can all be accomplished using drush:

Example Apache configuration:

RedirectMatch 403 "/(install|update|cron|xmlrpc).php"

## <a name="h.p4ggcy9w42g3"></a>2) Removing Code

>[CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface)s have been used extensively in web development and there are a great many good server executables that you may want to consider running. However, many CGIs that may be installed on a server are not actually needed and expose you to an additional security risk. If you are not running any CGIs, you should disable CGI access by removing LoadModule cgi_module and AddHandler cgi-script .cgi from your Apache config. You can also do this from the command line with:

Debian: sudo a2dismod cgi

If you don’t need it, remove it. All software is a source of potential risk, so list all Apache modules and look for unneeded modules. There are some [good discussions](https://groups.drupal.org/node/41320) on drupal.org about which modules are necessary and which are not.

Debian: apache2ctl -t -D DUMP_MODULES

CentOS: apachectl -t -D DUMP_MODULES

## <a name="h.5ol237ynhdat"></a>3) HTTP Headers

The Australian Government has produced an impressive report [Information Security Advice for All Levels of Government](http://www.dsd.gov.au/publications/csocprotect/protecting_web_apps.htm) which is sadly a bit out-dated as it hasn’t been updated since early 2012\. Most of that report is focused on content security policy, HTTP strict transport security and frame options. 

The [Security Kit](https://drupal.org/project/seckit) Drupal module addresses many security problems associated with HTTP Headers, but it is good to have them addressed at the Apache layer where possible. 

The [W3C](http://www.w3.org/TR/CSP/) is building a standard content security policy (CSP) to provide security controls which can mitigate attacks such as [Cross Site Scripting (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)). [Mozilla](https://developer.mozilla.org/en-US/docs/Security/CSP/Using_Content_Security_Policy) has produced a good description of how to write a [CSP](https://www.owasp.org/index.php/Content_Security_Policy) and and there are many commonalities with the Australian Government report above. To allow content from a trusted domain and all its subdomains, you can add the following to your Apache configuration:

Example Apache configuration:

Content-Security-Policy: default-src 'self' *.example.gc.ca

Your website and its visitors are going to be more secure if you use HTTPS to ensure that all information passing between the web server and the user’s browser is encrypted. There are performance implications for doing this as it does take additional processing power. You certainly want to ensure that all authentication happens through a secure HTTPS connection so that usernames and passwords cannot be intercepted. 

Example Apache configuration:

<VirtualHost *:80>

 ServerAlias *

 RewriteEngine On

 RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [redirect=301]

</VirtualHost>

This can be further enhanced by opting into the [HTTP Strict Transport Security (HSTS)](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security) enhancement which sends a special response header to the browser, which then prevents any communications from being sent over HTTP to the specified domain. 

Example HTTPS Apache configuration (see [example](https://www.owasp.org/index.php/HTTP_Strict_Transport_Security#Server_Side)):

Header set Strict-Transport-Security "max-age=16070400; includeSubDomains"

With the use of [Frame Options](https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options), users can be exposed to [Clickjacking](https://en.wikipedia.org/wiki/Clickjacking) when an iframe is injected in your site. If you know that you aren’t going to need to use iframes in your site you can disable it by modifying the Force X-Frame options in the Apache configuration. As usual, OWASP has an [extremely useful guide on avoiding Clickjacking.](https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet)

Example Apache configuration:

Header always append X-Frame-Options SAMEORIGIN

## <a name="h.hadcq2by8twm"></a>4) Everything Else

Modify the web server configuration to [disable the ](http://www.ducea.com/2007/10/22/apache-tips-disable-the-http-trace-method/)[TRACE/TRACK](http://www.ducea.com/2007/10/22/apache-tips-disable-the-http-trace-method/)methods either by employing the TraceEnable directive or by [adding the following lines](http://perishablepress.com/disable-trace-and-track-for-better-security/) to your Apache configuration: 

RewriteCond %{REQUEST_METHOD} ^(TRACE|TRACK)

RewriteRule .* - [F]

You should keep your server up-to date. Security by obscurity may delay some crackers, but not prevent them from accessing your system. Broadcasting information about your server environment isn’t likely to cause any harm, but if you choose to disable it you can simply add this to your Apache configuration:

ServerSignature Off

ServerTokens ProductOnly

One of the nice things about Ubuntu/Debian is that the Apache file structure is clean. By default it allows you store a variety of different configurations for sites or modules that are stored in logical directories. That’s not critical, but having a well defined Apache config file is. There should be inline comments about all changed variables explaining why they were added or modified.

It is possible to restrict the outgoing access of the web server by leveraging iptables’ “--uid-owner” option on the OUTPUT table. First you should know which user/UID your web server runs as. Typically this is “www-data” (uid 33) in Debian/Ubuntu and “nobody” (uid 65534) in CentOS. Double check by viewing the output of

Debian: ps aux | grep apache

CentOS: ps aux | grep http

In order to restrict Apache to connect only to https://drupal.org (with IP addresses 140.211.1