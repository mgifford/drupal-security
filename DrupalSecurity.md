# Drupal Security Best Practices

A Guide for Governments and Nonprofits

**By [OpenConcept Consulting Inc.](http://openconcept.ca/)**, originally written for Public Safety Canada

**Principal Author:** [Mike Gifford](mailto:mike@openconcept.ca)

**Contributors:**

*   [Mike Mallett](mailto:mike.mallett@openconcept.ca) (OpenConcept Consulting Inc.),
*   [Matt Parker](https://drupal.org/user/536298) (OpenConcept Consulting Inc.),
*   [Xavier Landreville](mailto:xavier@openconcept.ca) (OpenConcept Consulting Inc.),
*   [Michael Richardson](http://www.sandelman.ottawa.on.ca/),
*   [Colan Schwartz](http://colans.net/),
*   [Mack Hardy](http://affinitybridge.com/),
*   [Peter Cruickshank](http://spartakan.wordpress.com/),
*   [David Norman](https://deekayen.net/),
*   [Lee Rowlands](http://rowlandsgroup.com/),
*   [David Timothy Strauss](https://linkedin.com/in/davidstrauss),
*   [Ben Hosmer](http://www.radarearth.com/),
*   [Ursula Pieper](http://upsitesweb.com/),
*   [Jonathan Marcil](https://blog.jonathanmarcil.ca/)

**Editor:** [Lee Hunter](http://streamoflight.com/)

## Foreword

**Version:** 1.0 (December 15, 2014)
_This is a living document, sign up for updates on http://openconcept.ca/drupal-security-guide._

This document describes best practices for setting up and maintaining a Drupal site.
It was initially written for the Government of Canada, but it is equally applicable to other organizations.

Drupal is a popular, open source content management system (CMS).
It has a strong security model, but like any application, requires adherence to best practices.
Furthermore, Drupal is only one piece of the software that is required to run your site, and one needs to consider the security of the entire set of software.

This is not a comprehensive document, as IT security is a complex field.
We have tried to focus on fundamental principles that can improve security.
For more information on web server security, see the links at the end of this article.

We do not believe that there will ever be a 100% secure system.
There are always bugs in software and new exploits are being attempted all of the time.
We are listing options to consider, but each organization will need to weigh which combination they are going to use.

### Copyright

This document is made available under a [Attribution-ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/) Creative Commons License.
Feel free to distribute this, but please ensure to credit this original document, and its authors.

### Mike Gifford, Principal Author

Mike Gifford is the founder and president of OpenConcept Consulting Inc., headquartered in Ottawa Canada.
Long a prominent contributor to the Drupal community, Mike has been a member of the international group of developers that contribute to Drupal Core.
Mike is currently a Drupal 8 Core Accessibility Maintainer.
Led by Mike, OpenConcept contributed the first Drupal theme for the Government of Canada and has since been actively involved in the Drupal Web Experience Toolkit distribution within the Government of Canada.

To contact Mike, email [mike@openconcept.ca](mailto:mike@openconcept.ca), call 1-613-686-6736, or visit [http://openconcept.ca](http://openconcept.ca/).

### Table of Contents

A) Introduction

B) Principles of Security

C) Security Concerns for Managers

D) Server Security

D-1) Server Procurement

D-2) Immediately After Receiving Root Access

D-3) Create a baseline

D-4) Limit Access from Outside

D-5) Initial Installs

D-6) Server Maintenance

D-7) Managing Server Logs

D-8) Rough Server Ecosystem Image

E) Web Servers

E-1) Restricting Access

E-2) Removing Code

E-3) HTTP Headers

E-4) HTTP Basic Authentication

E-5) Everything Else

E-8) Web Application Firewall

F) PHP

G) Database Layer

H) Drupal

H-1) Files

H-2) Drush

H-3) Errors

H-4) Core and Contrib Hacks

H-5) Administration

H-6) Modules to Consider

H-7) Modules to Avoid on Shared Servers

H-8) Drupal Distributions

H-9) Miscellaneous

I) Writing Secure Code

J) Development, Staging & Production

K) Regular Maintenance

L) Points of Debate - Security by Obscurity

L-1) Make it Obscure

L-2) Make it Transparent

L-3) Be Consistent

M) Additional Resources

M-1) General guidelines

M-2) Videos

M-3) Third party tools

M-4) Books

## A) Introduction

Drupal 7 is a leading content management system in governments around the world.
It has been widely adopted by institutions around the world that are looking to meet increasing demands for service, larger challenges with accessibility and mobile requirements, and ever smaller budgets.

With governments increasingly targeted for cyber attacks, it is important that they remain up to date with best practices so that personal information and government assets are protected.

This guide provides an overview of important security principles, best practices for basic security; plus extra steps to be considered, if budget allows.
Where possible we will be providing some detailed instructions.
Managers should read sections B and C.
System administrators will need to focus on sections D, E, F, G, I, J and K.
Drupal developers can focus on section H and I, but should be familiar with the impact of the other sections too.

It should be clear that not all of the steps outlined here will need to be taken on all sites.
The principles should be followed but not all of the security suggestions described will need to be followed by all organizations.
Each practice or tool should be carefully evaluated to understand the potential costs, risks and benefits.

This document raises issues to consider before you procure a server and when you first gain access to your server.
It provides suggestions on what additional software you can add to your site which can help improve it's security.
It also highlights configuration options that you can apply to Apache, PHP and MySQL
to improve on the default settings.
Finally we talk about things that you can do to enhance Drupal security.

The code snippets which are included are not always a comprehensive guide, but there are always links in the descriptive paragraph with more information which you should consult before installing programs on your production server.
Section I has information on building secure modules and themes, but it is also worth consulting the [community documentation on Drupal.org](https://drupal.org/writing-secure-code).

Because this document strongly recommends against the use of Microsoft Windows servers for Internet-facing web sites, Windows security will not be addressed.

Security cannot be just a buzzword, [it is a process](https://www.schneier.com/essays/archives/2000/04/the_process_of_secur.html).
There needs to be
clear understanding about lines of responsibility and ultimately management needs to provide the budget required to ensure that systems can be maintained and regularly re-evaluated.

Eternal vigilance is important as those searching for your vulnerabilities are working around the clock and are well-financed.
This document will, itself, need to evolve to keep pace with new vulnerabilities.

## B) Principles of Security

*   **There is safety in the herd:**
    Leverage large, well maintained open source libraries (packages) with a critical mass of users and developers.
    Use compiled packages and check data integrity of downloaded code.
    Start with a standard Debian/Ubuntu or Red Hat/CentOS installation.
*   **Order matters:**
    Don't open up services to the Internet before your server is properly secured.
*   **Limit exposure:**
    Only install and maintain what is necessary.
    Reduce the amount of code installed.
    Review server configuration regularly to see if it can be streamlined.
*   **Deny access by default:**
    Only allow access where it is needed, and make all access policies deny by default.
*   **Use well known security tools:**
    There are well supported libraries that limit exposure, and check for intrusion.
    Suggestions are provided later.
*   **Avoid writing custom code:**
    Even large government departments find it difficult to invest properly in regular, ongoing code reviews.
    Minimize the use of any custom code.
*   **Contribute back: No software is ever perfect.**
    There is always room for improvement.
    Make the code you use better and give it back to the community.
    If you do it it properly you won't have to rewrite your code with the next security release and you will get free peer review and ongoing maintenance.
*   **Limit access:**
    There needs to be clear, documented roles of who has access to what.
    Only use root access when required and do so through sudo so people are not actually logging in as root.
    Isolate distinct roles where possible. Each person with access requires a separate account as shared accounts are inherently insecure.
*   **Make your application happy:**
    When running smoothly your server should not be generating errors.
    Monitor your server then investigate and resolve errors.
*   **Document everything:** Make sure you have an overview of any customizations which may have been done or any additional software that may have been added.
*   **Limit use of passwords:**
    Have sane organizational policies on password requirements.
    Keep track of your passwords in controlled, encrypted programs.
    Where possible use password-less approaches such as ssh key pairs which are more secure.
*   **Don't trust your backup:**
    Define and review backup procedures and regularly test that you can restore your site.
*   **Obscurity isn't security:**
    Organizations need to have their security policies well documented and internally transparent.
    Section K discusses this issue in detail.
*   **Security is big:**
    It is a mistake to assume that one person can do it well in isolation.
    Having access to a team (even outside of the organization) will help.
*   **Remember, you're still not safe:**
    Have an audit trail stored on another system.
    If your site is compromised, take the time to find out how.
    Use proper version control for all code and configuration.
*   **Not just for techs:**
    Upper management needs to take the time to understand these general principles of IT security as they have profound implications for the whole organization.

## C) Security Concerns for Managers

There are many assumptions about IT security that need to be fundamentally rethought in the era of the Internet.
Government is struggling to come to terms with this at the same time as working to understand the implication of cloud-based services.
What we can be certain of is that this field is accelerating and government departments need to keep up.

The first principle is to understand that time corrodes security and on the Internet time moves very fast.
You can't assume that any service you buy or develop is currently secure or will remain that way for long.
It is critical to understand what investments have been made and how they are maintained.

Web hosting and application development are different fields and one cannot simply outsource security upgrades to someone else to do.
No government server platform or private web hosting company can "take care" of your server security in isolation of the application that is running on it.
Ultimately, someone familiar with your website and it's content needs to be involved in performing upgrades.

Third party agencies are ultimately going to be involved, whether it the Domain Name Registrar or Content Delivery Network (CDN).
The communications paths with these agencies needs to be clear and well documented.
This recently happened with a large Canadian municipality who was redirected recently using an approach known as "social engineering".
By leveraging human vulnerability, crackers were able to gain control of critical infrastructure.
Properly documented procedures are important, as 3rd party services can often be manipulated phony email or telephone requests.

It is also important to remember that one person working in isolation cannot be expected to be an expert in all aspects of Internet security.
This is a vast area of expertise and it is changing quickly.
It's important that your security person has ongoing training and is engaged with both the Drupal and wider security communities to keep up with the latest threats, vulnerabilities and mitigation strategies.

Schedule time for a skilled security expert outside the core team to double check the server/Drupal configuration every quarter.
This does not have to be a consultant, but it should be someone outside of the website development team.

Everyone wants security to be simple, it isn't.
It's a matter of determining, as an organization, how much risk you want to be exposed to.
You can invest as much or as little on security as you want, but the risks are generally inversely proportional to resources spent on tightening your system.
Security has costs as well as benefits.
Complex systems are usually less secure because it costs relatively so much more to secure them.

Many organizations have policies for [Threat and Risk Assessments](https://www.dhs.gov/homeland-infrastructure-threat-and-risk-analysis-center).
However, as we've seen with the implementation of [Healthcare.gov](https://www.healthcare.gov/) political pressures associated with large projects often push security concerns into a post-launch phase.
It is highly recommended to go through a [Application Threat Modeling](https://www.owasp.org/index.php/Application_Threat_Modeling) process.
[Threat Risk Modeling](https://www.owasp.org/index.php/Threat_Risk_Modeling) is also a recommended process to help expand understanding of potential threats by using processes like STRIDE or DREAD.
By [identifying and classifying an organization's assets](http://www.networkmagazineindia.com/200212/security2.shtml) one can begin to prioritize where to focus resources.

Thinking through attack vectors and limiting exposure is really important.
I'm sure that many of the sites that were compromised by the Shellshock bash bug in that hit in September of 2014 simply hadn't disabled services like Apache's CGI module.
To run Drupal, you simply shouldn't need to expose bash to anyone other than properly authenticated Linux users.

As with most work, a great deal of security work lies in identifying and eliminating assumptions.
Document what is done, and be transparent in your work so that your organization knows that it has the level of risk it wants to maintain.

Organizations should also consider if the software that they use is properly resourced.
The Internet is built on free software, but much of it is backed by corporations who are also providing services built on the expertise that they use have built by contributing to open source software.
The [Heartbleed bug](http://heartbleed.com/) cost the economy billions, but was largely caused because the OpenSSL library was under resourced.
Although this is just one example, consider donating to project like the [OpenSSL Software Foundation](https://www.openssl.org/support/index.html) which supports the security infrastructure your organization depends on.
Likewise consider supporting organizations who contribute to [Drupal's security team](https://www.drupal.org/security-team).

A great deal of security work begins before anything is installed.
Properly considering security before beginning a server implementation is important.
Addressing security issues later in a project makes it impossible to do a security evaluation of the base system.
When setup is rushed, bad practices are often used which then become patterns that are followed long after the site is launched.

Implementing and enforcing a policy of using very complex passwords and [2 factor authentication](http://lifehacker.com/5938565/heres-everywhere-you-should-enable-two-factor-authentication-right-now) for any service that is responsible for delivering a critical service like email or code repositories.
Proper use of a secure, redundant password manager is also something that should be key for all employees.
If someone is able to hack into your Google Mail or GitHub account, they can often access much more than your communications.
Most services on the Internet are keyed to email addresses and passwords to 3rd party services are often stored.
Identity theft online is a huge problem for institutions.

The [UK's Government Service Design Manual](https://www.gov.uk/service-manual/) is an excellent resource for any large institution and it has a great section that applies directly to web security, [Security as enabler: Using technological change to build secure services](https://www.gov.uk/service-manual/technology/security-as-enabler.html).
In particular I like the point that security shouldn't degrade user experience.

Don't ignore minor bugs.
As [Darren Mothersele](http://darrenmothersele.com/blog/2014/02/20/drupal-security/) mentions in his blog, it is possible for a number of minor vulnerabilities to be
chained together in a way which can become a major exploit.
Sites as large as GitHub have been successfully targeted this way.
As he says, The cost of (in)security is high and "investment in security review and penetration testing is a Good Thing".

## D) Server Security

Any website is a complex ecosystem of software.
Each aspect can be tightened through proper configuration and through the addition of components beyond what is found in a default installation.
This document provides some examples, but mostly relies on links so that you can read the specific details on how this should be done.
There are other lists of considerations for server security, like Robert Hansen's list of [10 major tenets of a secure hosting model](http://drupalwatchdog.com/2/2/securing-your-environment), but where possible we will be referring back to the Principles of Security in Section B.

### 1) Server Procurement

Start server documentation with information from your server contract.
There are often technical details and notes about who to contact when things go wrong.

It is important to determine that there is a strong security community behind the OS distribution you choose, and that you have the necessary human resources in your department to maintain it.
Both Debian/Ubuntu and Red Hat Enterprise Linux(RHEL)/CentOS/Fedora can be considered solid.
The advantage of a Debian or Red Hat based solution is that there is extensive documentation and large communities of users who've shared their experiences through forums, issue trackers, and blog posts.
Ubuntu is based on Debian.
CentOS is almost a copy of RHEL and Fedora is the community edition of RHEL so is often somewhat ahead.
Most references to one of these two groups of distributions should be interchangeable.Note that Ubuntu and Debian have a different development cycle and are not identical.

If you use a Red Hat Enterprise Linux (RHEL) system, you will need to subscribe to their service in order to apply security upgrades and install the additional packages mentioned in this document.
Before procuring a Red Hat server, check that your package includes a subscription.

In our opinion, distributions of Linux like SUSE simply do not have a critical mass of users and developers (in the web server space) to maintain the code and documentation required for a secure environment.
Microsoft Windows is not a standard platform for hosting Drupal and is generally not recommended since community support is much less robust.
It is very difficult to limit exposure on a Windows Server since there are many unneeded pieces of the operating system which you cannot easily uninstall.

If you are worried about the server's physical security, you can also set up an [encrypted partition](https://wiki.archlinux.org/index.php/Disk_Encryption) on your hard drive.
This may introduce performance issues which might cause problems for your server.
This document will not be covering [how to set up an encrypted drive](https://help.ubuntu.com/community/EncryptedFilesystemHowto) but depending on the perceived threats, it may be worth implementing.

Special consideration should be taken when enabling HTTPS for encrypted traffic on "shared host"-type environments (any server hosting more than 1 domain).
Typically, due to the nature of the protocol, only one https website (domain name) could be hosted per IP.
However, with [Server Name Indication](http://en.wikipedia.org/wiki/Server_Name_Indication), it is now possible to host multiple https domains with distinct TLS certificates on the same IP.
It must be noted that SNI is dependent on both the client and the server supporting the TLS extension, but most do nowadays.
Another option, which might be useful if your servers or clients do not support SNI, is using [Subject Alternative Name](https://en.wikipedia.org/wiki/SubjectAltName) on certificates (also known as Unified Communications Certificates).
These certificates contain extra fields that list other common names (domain names) for which that certificate is valid.

Finally, don't get a server that comes with a server admin control panel.
They promise to make managing your site easier but present security problems.
There are a number of commercial packages, like cPanel or PLESK, that do make it easier to change settings on your site.
This seems particularly attractive if less technical users are responsible for server administration.
In our recent experience with cPanel, it introduced many difficulties in applying many of the suggestions and recommendations described here.
Because you can't simply disable cPanel, we had to reinstall the site on a new server.
If you choose a server with one, you will need to experiment with which of the following suggestions you are able to implement.
Some control panels are also known to overwrite settings when manual changes are made to configuration files.
It is important to work to minimize the attack surface and as these dashboards are managed through the web, it is yet another point where your server can be compromised.
Ultimately a control panel could prove convenient both for you and for those looking to hack into your system.

### 2) Immediately After Receiving Root Access

Hopefully the root password wasn't sent via an unencrypted email with the other login credentials.
Very few people use [GPG to encrypt emails](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) because it is cumbersome, but confidential documents should be encoded/decoded with this type of protection.
You can request that the password not be sent using the same medium so it will be difficult to intercept.
Minimally passwords can be sent in a separate email, but this provides only a slightly more obscure means to stop this information from being intercepted.

Most web hosts send all of the credentials together, therefore, the first step after getting access is to log in and change the root password.
Unencrypted email communications offers no security on the Internet and thus you must address this vulnerability immediately.

Update the list of available software and perform system software upgrades.
Most web hosts will use a pre-packaged distribution and there will frequently be updates that need to be applied.
Make sure you've got the updates and that the new packages are running.
If you update the Linux kernel you will have to reboot the server for it to be applied.
If you update Apache, you will also need to restart it.
Debian-style systems often restart the main daemon instances on package updates automatically, where RHEL-style systems treat daemon restarts as an administrator's responsibility.

```
Debian: apt-get update && apt-get upgrade
CentOS: yum upgrade
```

You will inevitably have a number of passwords to maintain.
We recommend storing these in a new [KeePass or KeePassX Password database](https://en.wikipedia.org/wiki/KeePass).
It has a nice password generator which makes it very easy to generate long (20+ characters) and complex passwords and store them immediately.
If you get any other passwords supplied via email, reset them immediately.
Your email address is also a [point of vulnerability](http://drupalwatchdog.com/2/2/practical-security).

The most common account that crackers try to compromise is the root user, so disable root logins.
Furthermore, set up user accounts with sudo access and [use ssh keys](https://wiki.archlinux.org/index.php/SSH_Keys) so that nobody accessing the site is using a password.
Note: the commands listed here assume you are using sudo access and but we have chosen not to explicitly prefix them with sudo.

Protect your ssh keys by ensuring that your private keys are [password protected and using 2048-bits](https://www.ssllabs.com/downloads/SSL_TLS_Deployment_Best_Practices.pdf).
By disabling the use of passwords for ssh user logins a common server vulnerability is simply eliminated.
When you turn off password logins "[script kiddies](https://en.wikipedia.org/wiki/Script_kiddie)" simply cannot
compromise your server with common dictionary or brute force attacks.
There are explanations on how to [effectively disable password logins](http://lani78.wordpress.com/2008/08/08/generate-a-ssh-key-and-disable-password-authentication-on-ubuntu-server/) but check that /etc/ssh/sshd_config has the text

```
PasswordAuthentication no
```

Remember that when downloading important files that there is a possibility that they have been tampered with.
Important security documents often come with a [MD5](http://www.electrictoolbox.com/article/linux-unix-bsd/howto-check-md5-file/) or SHA (secure hash algorithm) code which allows a user to verify that the file on a server is identical to the file that they have downloaded.You can generate a  [checksum](https://en.wikipedia.org/wiki/Checksum) to locally to determine equivalence using one of these:

```
shasum -a 256 ~/DrupalSecurity.pdf
md5sum ~/DrupalSecurity.pdf
openssl sha1  ~/DrupalSecurity.pdf
```

### 3) Create a baseline

Record a baseline of your server that you can review, knowing that this is the minimum number of processes which are running with a clean system.
Likewise record the baseline from a [netstat](https://en.wikipedia.org/wiki/Netstat) report to see what ports are open:

```
ps afx
netstat -l -p -n
```

Record the list of installed packages on the server.
Save this information in a text file in your management code repository.
If your server is compromised it is useful to know what packages were installed and running when you started:

```
Debian: dpkg -l
CentOS: yum list installed
```

Manage your ports through firewall settings: It is important to review and document the firewall settings - open ports - to see that they are properly restrictive.
The firewall program for sysVinit OS versions (CentOS/RHEL <=6), iptables, is still available for systemd OS versions (CentOS/RHEL >=7), which by default uses firewalld.

Using iptables, the port settings can be listed from the command line with:

```
iptables -L -v -n
```

You can load/save the iptables easily using the iptables-persistent package (installed on Debian/Ubuntu using `apt-get install iptables-persistent`).
With that you can simply save the existing IP tables from the command line:

```
Debian: service iptables-persistent save
CentOS: service iptables save
```

Install [Rootkit Hunter](http://sourceforge.net/apps/trac/rkhunter/wiki/SPRKH) (RKH) to help you "detect known rootkits, malware and signal general bad security practices".
You can set it up to [send you email alerts](http://www.tecmint.com/install-linux-rkhunter-rootkit-hunter-in-rhel-centos-and-fedora/), but can also do manual scans.

```
Debian: apt-get install rkhunter
CentOS: yum install rkhunter
```

### 4) Limit Access from Outside

In general you will want to allow traffic for port 22 (for known IPs), 80, 443 and reject other ports.
It can also be useful to use firewall rules to restrict outgoing connections from the Apache user.
The possible exception to this is drupal.org's IP address as you will want to regularly use drush (Drupal's command line shell and scripting interface) to update modules (see H2 below).
You can easily see what ports are open by using a port scanner such as [nmap](http://nmap.org/) from an external machine:

```
nmap -sS SERVER_ADDRESS
```

We recommend running [periodic TCP port scans](https://en.wikipedia.org/wiki/Port_scanner) on your server.
[MXToolbox](http://mxtoolbox.com/PortScan.aspx) offers an option to do this through their site, but you can also use tools like nmap which offers you more fine-grained controls.

Many servers come with [BIND](https://en.wikipedia.org/wiki/BIND) on UDP port 53.
This program can probably be removed in most instances or should be restricted with a firewall if required.
There are some [detailed instructions here](http://askubuntu.com/questions/162371/what-is-the-named-daemon-and-why-is-it-running) on how to remove it, which are particularly important if you aren't sure if you need it or not.
To check if bind is running, run this from the command line:

```
ps -Al | grep bind
sysVinit: chkconfig | grep bind
systemd: systemctl is-enabled bind
```

You can obscure your SSH port by reassigning it to other than the default (22).
This might fool a lazy cracker who isn't using a port scanner first, but won't stop the serious folks.

One of the best ways to limit ssh access to a server is to restrict access to a handful of known subnets (ie. 192.168.1.0/24) where administrators actually work.
Don't be afraid to add to this list; make it easy for your people to work wherever they need to.Security is not the enemy.

You can also [restrict who can ssh](http://apple.stackexchange.com/questions/34091/how-to-restrict-remote-login-ssh-access-to-only-certain-ip-ranges) into the server to a limited number of IP addresses.
Be very careful when configuring this as you don't want to block yourself from accessing the server.
[Debian's admin documentation](http://www.debian-administration.org/articles/87) offers the following changes which can be made to the iptables firewall:

```
  # All connections from address 1.2.3.4 to SSH (port 22) iptables -A INPUT -p tcp -m state --state NEW --source 1.2.3.4
  --dport 22 -j ACCEPT # Deny all other SSH connections iptables -A INPUT -p tcp --dport 22 -j DROP
```

There are many ways to do this.
Debian uses [ufw](https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server), the sysVinit releases of RHEL use [system-config-firewall-tui](https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server), [lokkit](http://docs.saltstack.com/en/latest/topics/tutorials/firewall.html) is coming along nicely and systemd releases RHEL 7 ship with [FirewallD](https://fedoraproject.org/wiki/FirewallD) by default.
Ultimately they all do the same thing slightly differently.
Make sure you understand your configurations and review them regularly.

If you already have established a [virtual private network](https://en.wikipedia.org/wiki/Virtual_private_network) (VPN) then you can restrict SSH access to within that private network.
This way you need to first log in to the VPN before being able to access the port.
Leveraging an existing VPN has some additional costs but also some security advantages.
If an organization isn't already using a VPN however, then the usability problems with forcing people to use it may encourage developers to find ways to circumvent it.
It is important to remember that a VPN is only as secure as the individual servers on the VPN.
If the VPN is shared with systems out of your control, and the responsible sysadmins are lax in security, then your servers should be hardened as if on the public network.

### 5) Initial Installs

There are some tools to harden your Linux system.
The program [grsecurity](http://olex.openlogic.com/packages/grsecurity) addresses a number of memory and permissions issues with the kernel.

[BastilleLinux](https://help.ubuntu.com/community/BastilleLinux) guides the administrator through an interactive process to limit access on the server.

Mandatory Access Controls (MAC) policies can be managed through programs like [SELinux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) and [AppArmour](https://en.wikipedia.org/wiki/AppArmor), for high security environments.
With Ubuntu, use AppArmour as it comes installed by default.
While AppArmour is often considered inferior and less flexible than SELinux, there is no need to uninstall it.AppArmour may impact other security tools and should not be used in conjunction with SELinux.

With other distributions it is recommended to use SELinux (examples for use in [Debian](https://wiki.debian.org/SELinux) and [Red Hat](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Security-Enhanced_Linux/)) as it's rules were initially developed to meet NSA policies.

```
Debian (not Ubuntu): apt-get install perl-tk bastille
selinux-basics selinux-policy-default auditd
```

Using an host based intrusion detection system (HIDS) such as the [OSSEC](http://www.security-marathon.be/?p=544) host-based intrusion detection system (HIDS) or [PHPIDS](http://www.phpids.org/) (PHP-intrusion detection system) is a good practice.
There are good how-to documents available for both [PHPIDS](http://www.howtoforge.com/intrusion-detection-for-php-applications-with-phpids) and [OSSEC](http://www.ossec.net/?page_id=11).
[Tripwire](http://www.tripwire.com/) and [Snort](http://www.snort.org/) are other IDS's which monitor the integrity of core files and will alert you to suspicious activity (available for [CentOS](https://www.centos.org/docs/2/rhl-rg-en-7.2/ch-tripwire.html) and [Debian](http://penguinapple.blogspot.ca/2010/12/installing-configuring-and-using.html)).
With any HIDS, you should make sure that secure IPs, such as your outgoing gateway is whitelisted.

[Drupal monitoring can be set up to work with OSSEC](http://www.madirish.net/428) which would be more efficient than using Drupal's [Login Security](https://drupal.org/project/login_security) module as it would allow you to use your existing HIDS infrastructure to alert you to these sorts of attacks.

Crackers will often try to use a [brute force attack](http://en.wikipedia.org/wiki/Brute-force_attack) to guess usernames and passwords.
Using a service like [Fail2ban](http://www.fail2ban.org/wiki/index.php/Main_Page) can block IP addresses that are making an unreasonable number of login attempts.
This won't prevent distributed attacks, but could be used in conjunction with OSSEC.
[Fail2ban is also an effective measure for flood control](http://www.debian-administration.org/article/Blocking_a_DNS_DDOS_using_the_fail2ban_package) and can stop most denial of service attacks.
Drupal also has some built in flood control options, the [Flood Control module](https://drupal.org/project/flood_control) provides a UI to control them.
[Distributed Denial of Service (DDOS)](https://en.wikipedia.org/wiki/Denial-of-service_attack) attacs are more difficult to address, but there's a great defence plan laid out on [StackOverflow](http://stackoverflow.com/questions/14477942/how-to-enable-ddos-protection).

```
Debian: apt-get install fail2ban
CentOS: yum install fail2ban
```

Place the /etc directory under version control so that you can easily track which configurations have changed.
The program [etckeeper](https://help.ubuntu.com/12.04/serverguide/etckeeper.html) automates this process nicely and hooks into your package manager and cron to do its work when your server is upgraded or new software is installed.

```
Debian: apt-get install etckeeper bzr && etckeeper init && etckeeper commit "initial commit"
CentOS: yum install etckeeper && etckeeper init && etckeeper commit "initial commit"
```

Ubuntu comes with the [Ubuntu Popularity Contest](https://help.ubuntu.com/community/UbuntuPopularityContest) (popcon) to gather statistics about which packages are used in the community.
Although this is anonymous, it can be a good idea to remove this package so that it is not a potential weak link.
This is an optional package that can be easily removed without impacting your site's performance.

```
Ubuntu: dpkg --purge popularity-contest ubuntu-standard
```

You will probably want to install an opcode cache and [Memcache](http://memcached.org/) (or [Redis](http://redis.io/)) to ensure that your site is responding quickly.
PHP 5.5+ now comes with built in opcode cache, earlier versions of PHP can add this using [APC](http://php.net/manual/en/book.apc.php).
Memcached is a general-purpose distributed [memory caching](https://en.wikipedia.org/wiki/Memory_caching) system.
Both work to make your server more responsive by minimizing the load on the server and improving caching.
This will help when there is an unexpected server load.

Aside from the performance advantages, there can be security improvements by caching the public display.
There are huge security advantages to restricting access to the rendering logic (Drupal's admin) so that the public is only interacting with a cache serving front end content.
In using any caching however, it is critical that only anonymous data is cached.
A mis-configured cache can easily [expose personal data to the public](https://speakerdeck.com/owaspmontreal/demystifying-web-cache-by-kristian-lyngstol#24%20).
This needs to be carefully tested on sites which have private or confidential data.

There are a number of ways to cache the public display, including leveraging Memcache and [Nginx](http://wiki.nginx.org/Main) to extend Drupal's internal page cache.
One of the most powerful tools is [Varnish](https://www.varnish-cache.org/) which can provide incredible performance enhancements.
It can also be used effectively to deny all logins on your public site by being configured to denying cookies on port 80\.
This is an example of what can be added to Varnish's vcl file to remove the cookies which are required to authenticate:

```
if (req.http.host == "example.com") { unset req.http.Cookie;}
```

If you have a site which has only a few users and doesn't have any online forms for anonymous users then you can configure Varnish to simply reject all HTTP POST requests.
Then in Apache you can whitelist the IP address you want to have access to login into Drupal.
Matt Korostoff documented this approach in his [breakdown of the Drupalgeddon attacks](http://mattkorostoff.com/article/I-survived-drupalgeddon-how-hackers-took-over-my-site) that affected many Drupal 7 sites.

Shared server environments provide a number of security challenges.
Do not expect it to be easy to securely host several sites on the same server with direct shell access to different clients.
If you need to do this, it is worth investigating [FastCGI](http://www.fastcgi.com/drupal/) which when used in conjunction with [suexec](https://httpd.apache.org/docs/current/suexec.html) or [cgiwrap](http://cgiwrap.sourceforge.net/) to isolate individual processes on a shared server.
We expect most government departments to have access to either a virtual (e.g.
[VMware](http://www.vmware.com/), [Xen](http://www.xenserver.org/), [OpenVZ](http://openvz.org/) or [KVM](http://www.linux-kvm.org/)) or cloud-based (e.g.
[Amazon](https://aws.amazon.com/ec2/) or [Rackspace](http://www.rackspace.com/cloud/)) servers.
There is also [significant movement in the Drupal
  community](https://www.getpantheon.com/blog/why-we-built-pantheon-containers-instead-virtual-machines) to use [Linux Containers](https://en.wikipedia.org/wiki/LXC) to more efficiently distribute processing power without compromising security.

### 6) Server Maintenance

Security requires constant vigilance.
Someone should be tasked with ensuring that the server is kept up-to-date at least weekly.
This isn't usually a complex task, but it does require that someone subscribe to the security update mailing list for the distribution (e.g. [Ubuntu](http://www.ubuntu.com/usn/) and [CentOS](https://www.centos.org/modules/tinycontent/index.php?id=16)), apply the updates, and review the logs to ensure everything is still running properly.
Upgrades can be done with the following commands:

```
Debian: apt-get update && apt-get upgrade
CentOS: yum upgrade
```

It is very useful to have a service like [Nagios](http://www.nagios.org/documentation) monitoring your production server to alert you if any problems arise.
The configuration of Nagios can be quite complex, but you can set it up easily enough on your staging server.
You will need to grant access on your production environment to this server and you must enable CGI access on this server.
Remember that if you enable this, you will also need to consider the [security implications](http://nagios.sourceforge.net/docs/3_0/security.html) that it presents.
To get the server installed in your staging environment, execute the following from the command line:

```
Debian: apt-get install nagios3 nagios-nrpe-plugin
```

And for each server you wish to monitor with Nagios:

```
Debian: apt-get install nagios-nrpe-plugin
```

[Munin](http://munin-monitoring.org/) can be run on the production environment to give you a sense of the relative load of various key elements over the past hour, day, week and month.
This can be useful when debugging issues with your server.

```
Debian: apt-get install munin munin-node
```

Access to this information is available through your web server but you will want to configure your site to [ensure that this data is not publicly available](http://www.howtoforge.com/server_monitoring_monit_munin).

There are also many good reasons to use server [configuration management software](https://en.wikipedia.org/wiki/Software_configuration_management) like [Puppet](http://projects.puppetlabs.com/projects/puppet) or [Chef](https://www.chef.io/).
Initially, it will take you a lot more time to configure it this way, but it will make it much easier to restore your server when something does happen and and see you are back online quickly.
It also codifies the process to ensure that you don't miss critical setup steps.
This approach also makes it trivial to have essentially duplicate development, staging and production environments.

### 7) Managing Server Logs

Your web server is a complex environment involving thousands of software projects.
Most of these will store log files in /var/log.
If log files aren't properly rotated and compressed they can become unmanageably large.
If your hard drive is filled up with old log files your site will simply stop functioning.
Most distributions of Linux come come with [logrotate](http://www.cyberciti.biz/faq/how-do-i-rotate-log-files/) configured such that log files are segmented on a regular basis and the archive is compressed so that space isn't a problem.

Most Linux distributions also come with syslog built in, which is critical for doing security audits.
You can also configure it to [send emergency messages to a remote machine](http://www.linuxvoodoo.com/resources/howtos/syslog), or even send a duplicate of all log messages to an external loghost.
There is a discussion in the Drupal section later on about how to direct Watchdog messages to syslog.
There are many tools to help system administrators more effectively monitor their log files, and regular log reviews can be an important part of early breach detection.

If your server is configured with a caching reverse proxy server or a load balancer such as Varnish, Nginx or haproxy then you should ensure that Drupal is made aware of the actual REMOTE_IP.
The common solution requires configuring the X-Forwarded-For in both Varnish and Apache, but as [Jonathan Marcil's blog post points out](https://blog.jonathanmarcil.ca/2013/09/remoteaddr-and-httpxforwardedfor-bad.html), "X-Forwarded-For is actually a list that can be a chain of multiples proxies and not just a single IP address".
To that effect, ensure that all IP addresses for your reverse proxies are identified in your settings.php file ([configuration](https://github.com/drupal/drupal/blob/7.x/sites/default/default.settings.php#L358)).
Another solution would be to create a custom HTTP header such as HTTP_X_FORWARDED_FOR and use it in your architecture and tell
Drupal to use it using the configuration variable "reverse_proxy_header" in settings.php under "Reverse Proxy Configuration".
Drupal itself will manage correctly a list of trusted reverse proxy with the standard "X-Forwarded-For" header, but this is useful if you want to correctly logs IP at a Web server, proxy or load balancer level.
Note that the front facing proxy should ignore if the custom header exists and replace it with it's own.

```
$conf['reverse_proxy'] = TRUE;
$conf['reverse_proxy_addresses'] = array('127.0.0.1','192.168.0.2');
$conf['reverse_proxy_header'] = 'HTTP_X_FORWARDED_FOR';
```

Another approach to dealing with this is to simply use Apache's Reverse Proxy Add Forward (RPAF) module.
As Khalid Baheyeldin [writes in his blog](http://2bits.com/articles/correct-client-ip-address-reverse-proxy-or-content-delivery-network-cdn.html), this Apache module can be used for both Reverse Proxy and/or a Content Delivery Network (CDN).

```
Debian: apt-get install libapache2-mod-rpaf
```

By editing the /etc/apache2/mods-enabled/rpaf.conf, set your proxy IP and restarting Apache your access.log will show the real client IP rather than that of your proxy.

The most important server logs to monitor are Apache's.
If there is more than one site on a given server, it is normal for each site to have it's own log file rather than using the default generic one.
If you run more than one site or have multiple web servers, log centralization can allow you to get an overall view of site issues.
Open source tools such as [logstash](http://logstash.net/) can be used to simplify the process of searching all of your log files.

### 8) Rough Server Ecosystem Image

![image for generic server ecosystem](http://openconcept.ca/sites/oc2014/files/drupal_security_best_practices_for_government.svg)

## E) Web Servers

All files and directories in your DocumentRoot should be editable by a non-root user, and should also not be writable by the Apache user, except the Drupal files/ directory.
Please refer to Drupal's [Securing file permissions and ownership](https://drupal.org/node/244924) for the complete discussion.

[PHP-FPM over FastCGI](http://php-fpm.org/) allows your server to have [site specific "pools" of PHP](http://www.howtoforge.com/php-fpm-nginx-security-in-shared-hosting-environments-debian-ubuntu).
By giving each site unique PHP permissions you can effectively "sandbox" a PHP application and simplify file/folder permissions by specifying the user and group for the process pool.
This reduces the points of failure in a shared hosting environment, where the PHP on another site could be used to hijack the server.
There are also real [advantages to using PHP-FPM for managing server load](https://phpbestpractices.org/#serving-php) as Apache's mod_php isn't very efficient.

Server or browser support for SSL versions 2 and 3 are not recommended.
Despite this, as Google noted in their blog post about the [POODLE Exploit](http://googleonlinesecurity.blogspot.co.uk/2014/10/this-poodle-bites-exploiting-ssl-30.html), "SSL 3.0 is nearly 18 years old, but support for it remains widespread." Web browsers still support this insecure version of SSL, but it is [easy to test](https://zmap.io/sslv3/) to ensure if your browsers are vulnerable.
Qualys SSL Labs also have a really [great tool to evaluate](https://www.ssllabs.com/ssltest/) if your server is still vulnerable.

On your web server, it is good to ensure that SSL configuration permits only TLS version 1.2.
unfortunately some common web browsers still do not support the latest version of TLS.
Fortunately, as of [February 2014](https://en.wikipedia.org/wiki/Transport_Layer_Security#Web_browsers), the latest version of all major web browsers support SSL 3.0, TLS 1.0, 1.1, and 1.2 enabled by default.
Check if the[ SSL services employ only AES](http://www.thinkwiki.org/wiki/AES_NI) with key lengths 256 bits and higher.
You can install [GnuTLS](https://help.ubuntu.com/community/GnuTLS) from the command line to enable this:

```
Debian: apt-get install gnutls-bin
```

It is also recommended to disable SSLCompression in Apache.
As stated in the [Apache documentation](https://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcompression) "Enabling compression causes security issues in most setups (the so called CRIME attack)." This is the default for Apache version 2.4.4+.

The **HeartBleed security bug** has gotten a lot of attention lately.
The primary security practice we can recommend from this is to ensure that someone is always paying attention to the security mailing lists for your operating system.
By the time you hear it from the media it is probably too late.
The other suggestion is one that is suggested by the [EFF](https://www.eff.org/) and others which includes implementing [Perfect Forward Secrecy](https://www.eff.org/deeplinks/2013/08/pushing-perfect-forward-secrecy-important-web-privacy-protection) (PFS).
Although we didn't explicitly refer to it as this in earlier versions of this document, the hardened SSL configuration we recommended in the fall implements this.

The duraconf configuration scripts for [hardening SSL/TLS services](https://github.com/ioerror/duraconf) provided by Jacob Appelbaum would have protected users from the HeartBleed bug.
In the Apache config you can [set hardened SSL configurations for the HTTPS protocol](https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/) (note that we're now using Hynek Schlawack configuration rather than [Ivan Ristic's](https://community.qualys.com/blogs/securitylabs/2013/08/05/configuring-apache-nginx-and-openssl-for-forward-secrecy) because it is being updated more regularly) with:

```
SSLProtocol ALL -SSLv2 -SSLv3
SSLHonorCipherOrder On
SSLCipherSuite
ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS
```

After restarting Apache, you can check the SSL information in a browser by double clicking on the lock icon in the address bar on https:// sites to get information on the encryption channel and confirm it's using TLS.

There are other approaches like that suggested by [Remy van Elst](https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html), but ultimately you need to test your SSL configuration through a tool like [Qualys SSL Labs' Server Test](https://www.ssllabs.com/ssltest/).
This is a free online service that performs a deep analysis of the configuration of any SSL web server on the public Internet.
This will grade your SSL compliance and do things like confirm that you are using the latest version of TLS and verify that you are protected from [BEAST attacks](https://en.wikipedia.org/wiki/Transport_Layer_Security#BEAST_attack).
You want straight A's!

On your staging/development server it is fine to provide a [self signed SSL certificate](https://en.wikipedia.org/wiki/Self-signed_certificate) to ensure that the traffic is encrypted.
Setting up a third party verified SSL certificate on your production environment will be important as otherwise your users will be asked to verify the exception when accessing the HTTPS version of your site.
A listing of certificate authorities is available at the bottom of [this Wikipedia page](https://en.wikipedia.org/wiki/Certificate_authority#External_links).
You can review the validity of your SSL certificate through a free [SSL Test constructed by SSLLabs](https://www.ssllabs.com/ssltest/) or with the following openssl command:

```
openssl s_client -connect SERVER:443
```

To check a specific protocol using openssl:

```
openssl s_client -connect SERVER:443 -ssl2
openssl s_client -connect SERVER:443 -ssl3
```

Note that SSL Certificate Authorities are depreciating the very popular SHA1 hashing function because of weakness in the algorithm.
Qualys Labs recommends [renewing with SHA256](https://community.qualys.com/blogs/securitylabs/2014/09/09/sha1-deprecation-what-you-need-to-know) as soon as possible.

### 1) Restricting Access

Another useful Apache module is [mod_authz_host](https://httpd.apache.org/docs/2.2/mod/mod_authz_host.html) which can restrict access to specific pages such as /user and /admin/* - this can be useful if your site is used just as a CMS with no user interaction.
The example below is more appropriate for sites which would have broader user authentication, but where users are restricted from editing nodes - node/*/edit - this type of approach can also be used to restrict access to non-production environments.
If you have a multi-lingual site, you may also want to check that access is denied for paths with the language prefix, in Canada, many sites would need to also add /fr/user and /en/user .
It is a best practice to secure all pages on non-production environments from both search engines, but especially from crackers.
The following are examples of how to do this with mod_authz_host and also mod_rewrite:

Example Apache configuration using mod_authz_host:

```
<Location ~ "/node/.*/edit">
  Order Deny,Allow
  Deny from all
  Allow from 206.47.13.64 174.142.104.53
  99.241.125.191
</Location>
```

Example Apache configuration using mod_rewrite:

```
<IfModule mod_rewrite.c>
  RewriteEngine on
  # Allow only internal access to admin
  RewriteCond %{REMOTE_ADDR}
  !^(206\.47\.13\.64|174\.142\.104\.53|99\.241\.125\.191)$
  RewriteRule ^admin/.* - [F]
</IfModule>
```

Drupal has a number of processes that can be triggered by URLs.
You may wish to block some of these using Apache so that they simply cannot be loaded from the web browser.
Common processes to secure are update, install and cron, tasks which can all be triggered using drush:

Example Apache configuration:

```
RedirectMatch 403
"/(install|update|cron|xmlrpc|authorize).php"
```

### 2) Removing Code

[CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface)s have been used extensively in web development and there are a great many good server executables that you may want to consider running.
However, many CGIs that may be installed on a server are not actually needed and expose you to an additional security risk.
If you are not running any CGIs, you should disable CGI access by removing LoadModule cgi_module and AddHandler cgi-script .cgi from your Apache config.
You can also do this from the command line with:

```
Debian: a2dismod cgi
```

If you don't need it, remove it.
All software is a source of potential risk, so list all Apache modules and look for unneeded modules.
There are some [good discussions](https://groups.drupal.org/node/41320) on drupal.org about which modules are necessary and which are not.

```
Debian: apache2ctl -t -D DUMP_MODULES
CentOS: apachectl -t -D DUMP_MODULES
```

If you are using mod_php with apache, it can be useful to enable php5-dev for Drupal so that you can enable tools like [PECL's uploadprogress](http://pecl.php.net/package/uploadprogress).
However, after you've done that you will want to remove the php module that you used to build it:

```
Debian: sudo apt-get remove php5-dev
```

You can find other development packages on your server by:

```
Debian: apt-cache search ".-dev"
```

### 3) HTTP Headers

The Australian Government has produced an impressive report [Information Security Advice for All Levels of Government](http://www.dsd.gov.au/publications/csocprotect/protecting_web_apps.htm) which is sadly a bit out-dated as it hasn't been updated since early 2012.
Most of that report is focused on content security policy, HTTP strict transport security and frame options.

The [Security Kit](https://drupal.org/project/seckit) Drupal module addresses many security problems associated with HTTP headers, but it is good to have them addressed at the Apache layer where possible.

The [W3C](http://www.w3.org/TR/CSP/) is developing a standard content security policy (CSP) to provide security controls which can mitigate attacks such as [Cross Site Scripting (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29).
[Mozilla](https://developer.mozilla.org/en-US/docs/Security/CSP/Using_Content_Security_Policy) has produced a good description of how to write a [CSP](https://www.owasp.org/index.php/Content_Security_Policy) and and there are many commonalities with the Australian Government report above.
To allow content from a trusted domain and all its subdomains, you can add the following to your Apache configuration:

Example Apache configuration:

```
Content-Security-Policy: default-src 'self' *.example.gc.ca
```

Your website and its visitors are going to be more secure if you use HTTPS to ensure that all information passing between the web server and the browser is encrypted.
There is a [growing movement encrypt all web traffic](http://chapterthree.com/blog/why-your-site-should-be-using-https), even to brochure sites.
Doing so will have minor performance implications as it does take some additional processing power.
You certainly want to ensure that all authentication happens through a secure HTTPS connection so that usernames and passwords cannot be intercepted.
Do ensure that all of your files are being served from a HTTPS environment as mixed traffic introduces security problems.

Example Apache configuration:

```
<VirtualHost *:80>
  ServerAlias *
  RewriteEngine On
  RewriteRule ^(.*)$ https://%{HTTP_HOST}$1[redirect=301]
</VirtualHost>
```

This can be further enhanced by opting into the [HTTP Strict Transport Security (HSTS)](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security) enhancement which sends a special response header to the browser, which then prevents any communications from being sent over HTTP to the specified domain.

Example HTTPS Apache configuration (see [example](https://www.owasp.org/index.php/HTTP_Strict_Transport_Security#Server_Side)):

```
Header set Strict-Transport-Security "max-age=16070400; includeSubDomains"
```

You can also submit your site to the [EFF's HTTPS Everywhere extension](https://www.eff.org/https-everywhere) which will allows security conscious individuals to rewrite requests to these sites so that they use HTTPS by default.
As part of this extension, you can [submit new public rules](https://www.eff.org/https-everywhere/rulesets) for your site to ensure that it runs optimally with this browser extension.

With the use of [Frame Options](https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options), users can be exposed to [Clickjacking](https://en.wikipedia.org/wiki/Clickjacking) when an iframe is injected in your site.
If you know that you aren't going to need to use iframes in your site you can disable it by modifying the Force X-Frame options in the Apache configuration.
As usual, [OWASP](https://www.owasp.org/) has an [extremely useful guide on avoiding Clickjacking](https://www.owasp.org/index.php/Clickjacking_Defense_Cheat_Sheet).
You must have the mod-headers module enabled before adding this string to your Apache configuration but this is easy to add through the command line -a2enmod headers - afterwards you can add this to your configuration.

Example Apache configuration:

```
Header always append X-Frame-Options SAMEORIGIN
```

### 4) HTTP Basic Authentication

Most webservers provide a way to restict access to a site using [HTTP Basic Authentication](http://tools.ietf.org/html/rfc7235) — for example, using Apache HTTP Server's [`htpasswd` files or `Auth*` directives](http://httpd.apache.org/docs/2.2/howto/auth.html), or nginx's [`ngx_http_auth_basic_module`](http://nginx.org/en/docs/http/ngx_http_auth_basic_module.html) module.

While HTTP Basic Authentication is a good way to prevent search engines from indexing your testing and staging sites, it is inherintly insecure: traffic between browsers and your site is not encrypted, and in fact, anyone can gain access to the site simply by copying the "Authorization" HTTP header.

Furthermore, the username and password used for HTTP Basic Authentication are not encrypted either (just base-64 encoded, which is trival to decode), so do not re-use credentials used elsewhere (e.g.: don't re-use the credentials someone uses to log into Drupal, SSH into the webserver; or hook HTTP Basic Authentication up to an LDAP database or the operating system's `/etc/passwd`).

### 5) Everything Else

Modify the web server configuration to [disable the TRACE/TRACK](http://www.ducea.com/2007/10/22/apache-tips-disable-the-http-trace-method/) methods either by employing the TraceEnable directive or by [adding the following lines](http://perishablepress.com/disable-trace-and-track-for-better-security/) to your Apache configuration:

```
RewriteEngine On
RewriteCond %{REQUEST_METHOD} ^(TRACE|TRACK)
RewriteRule .* - [F]
```

You should keep your server up-to date.
Security by obscurity may delay some crackers, but not prevent them from accessing your system.
Looking at the logs for any popular site, you will notice thousands of fruitless attempts at exploits that may not even exist (or have existed) on your system.
Broadcasting information about your server environment isn't likely to cause any harm, but if you choose to disable it you can simply add this to your Apache configuration:

```
ServerSignature Off
ServerTokens ProductOnly
```

One of the nice things about Ubuntu/Debian is that the Apache file structure is clean.
By default it allows you store a variety of different configurations for sites or modules that are stored in logical directories.
That's not critical, but having a well defined Apache config file is.
There should be inline comments about all changed variables explaining why they were added or modified.

It is possible to restrict the outgoing access of the web server by leveraging iptables' "--uid-owner" option on the OUTPUT table.
This can also be done using [containers and namespaces](https://www.getpantheon.com/blog/containers-not-virtual-machines-are-future-cloud-0) on modern Linux kernels.
In most cases, if you are using containers, the UID of Apache will be the same inside the container as outside of it.

You should make note of the user/UID of your web server.
This is dependent on the package installation order, but often this is "www-data" (uid 33) in Debian/Ubuntu and "nobody" (uid 65534) in CentOS.
If you are using PHP-FPM, then you will need to search for the UID of that application rather than Apache's.
Double check by viewing the output of:

```
Debian: ps aux | grep apache
CentOS: ps aux | grep http
```

In order to restrict Apache to connect only to https://drupal.org (with IP addresses 140.211.10.62 and 140.211.10.16 at the time of writing) insert the following firewall rules:

```
iptables -A OUTPUT -m owner --uid-owner ${APACHE_UID}
-p udp --dport 53 -j ACCEPT

iptables -A OUTPUT -d 140.211.10.62/32 -p tcp -m
owner --uid-owner ${APACHE_UID} -m tcp --dport 443 -j ACCEPT

iptables -A OUTPUT -d 140.211.10.16/32 -p tcp -m
owner --uid-owner ${APACHE_UID} -m tcp --dport 443 -j ACCEPT

iptables -A OUTPUT -m owner --uid-owner ${APACHE_UID}
-m state --state NEW -j DROP
```

There are also Apache modules like [Project Honey Pot](https://www.projecthoneypot.org/httpbl_download.php) that make it harder for people to hack your system.
Honey Pot can also be [installed on Drupal](https://drupal.org/project/httpbl), but Apache is often more efficient at addressing attacks like this before it hits PHP:

```
Debian: apt-get install mod_httpbl
CentOS: yum install mod_httpbl
```

### 8) Web Application Firewall

Web Application Firewalls (WAFs) can be used to provide additional protection over the Web server.
It can be a standalone server that act as a reverse proxy or a Web server modules.

Apache has a number of modules that can be installed to tighten security of the web server.
We recommend installing [ModSecurity and mod_evasive](http://www.thefanclub.co.za/how-to/how-install-apache2-modsecurity-and-modevasive-ubuntu-1204-lts-server) as a [Web Application Firewall (WAF)](https://www.owasp.org/index.php/Web_Application_Firewall).
This can be set to leverage the Open Web Application Security Project's (OWASP) [ModSecurity Core Rule Set Project](https://www.owasp.org/index.php/Category:OWASP_ModSecurity_Core_Rule_Set_Project).

```
Debian: apt-get install libapache2-mod-evasive
libapache2-modsecurity; a2enmod mod-security; a2enmod
mod-evasive CentOS: yum install mod_evasive mod_security
```

To engage ModSecurity in your Apache, you'll need to [set up the base files in your Apache configuration](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#a-recommended-base-configuration) and then restart Apache.

Using default generic configurations such as the OWASP Core Rule Set can impact the normal behaviour of Drupal and must be tested extensively before deployment.
Usually some rules are breaking rich content edition or modules that behave differently than Drupal core.
It is recommended to run the rules in a passive manner in order to identify false positive when in production.
Default [configuration of ModSecurity](https://github.com/SpiderLabs/ModSecurity/blob/master/modsecurity.conf-recommended#L7) should do it with:

```
SecRuleEngine DetectionOnly
```

You can then set it to "On" whenever you are ready.
A server restart is needed for changes to be effective.
In that case the WAF will behave as a passive Web application intrusion detection system and you can chose to never set it to "On" if you wish to use it only for that purpose.
In any cases, you'll want to monitor the log files for alerts in order to detect malicious attempts and potential false positives.

WAF software needs maintenance as well and rules should be updated periodically.
Tests for false positive should be made after each change of functionality within the Drupal site.

At last but not least, WAFs are a great solution for [virtual patching](https://www.owasp.org/index.php/Virtual_Patching_Cheat_Sheet) and application flaw fixing, but they can be bypassed.
It is discouraged to rely solely on that technology to keep up with security: fixing flaw and applying patch on the backend applications should not be replaced with WAF utilization.

## F) PHP

There are lots of good resources on how to tighten security for PHP.
It is a very commonly used scripting language and it is running some of the biggest and most important sites on the Internet.

We recommend installing a PHP hardening tool called [Suhosin](http://www.suhosin.org/stories/index.html) which tightens up PHP's existing configuration so that it is more robust.
It is designed to protect servers and users from known and unknown flaws in PHP applications and the PHP core.

Ubuntu (this may not work in their LTS releases).

Enable ‘universe' repo in /etc/apt/sources.list and `apt-get update ; apt-get install php5-suhosin`

```
Debian: apt-get install php5-suhosin
CentOS: yum install php-suhosin
```

A good comprehensive list is from Justin C. Klein's blog post [Hardening PHP from php.ini](http://www.madirish.net/199).
Other than his comments on safe_mode, we think he's got it right.
Drupal needs safe_mode disabled in PHP.
PHP's Safe Mode isn't really considered much of a security enhancement and it has been removed in recent versions.

As with Apache modules, look for what you can remove.
You can display a list of enabled PHP modules and look for those which can be removed.
From the command line you can get a list of php modules with:

```
php -m
```

#### Setting PHP.ini Variables

Many PHP variables can be set via Apache as well as in the PHP configuration.
We recommend keeping PHP-specific security configuration centrally located in the php.ini file.

Another exploit is [Session fixation](https://en.wikipedia.org/wiki/Session_fixation) where a user's browser session can be hijacked by a third party.
[OWASP](https://www.owasp.org/index.php/HttpOnly) goes into much more detail, but by using the [HttpOnly](http://php.net/manual/en/function.setcookie.php) flag when generating a cookie you can reduce the risk of an XSS attack by limiting access to protected cookies.
It is advised to stop Javascript from accessing cookie data.
Session information should only ever be passed to the server with the same domain.
You can also set a [secure cookie attribute](https://en.wikipedia.org/wiki/HTTP_cookie#Secure_cookie) and restrict all transmission of cookie data to an HTTPS connection to ensure that the cookie is less likely to be exposed to cookie theft via eavesdropping.
Furthermore, you can control the [hash algorithm](http://www.php.net/manual/en/session.configuration.php#ini.session.hash-function) used to generate the session ID and choose from a number of algorithms like the NSA's [SHA-2](https://en.wikipedia.org/wiki/SHA-1) protocol or [whirlpool](https://en.wikipedia.org/wiki/Whirlpool_%28cryptography%29).
Add the following to your php.ini file:

```
session.cookie_httponly = 1
session.use_only_cookies = 1
session.cookie_secure = 1
session.hash_function = whirlpool
```

You can obtain a list of the available hash functions on your system by executing:

```
php -r ‘print_r(hash_algos())'
```

Limit your exposure to only the system resources you want to make available to a PHP page.
You can control your resources by limiting the upload_max_filesize, max_execution_time, max_input_time, memory_limit variables so that a script isn't as likely to monopolize resources.

```
php_value memory_limit = 128M
php_value max_input_time = 60
php_value max_execution_time = 30
php_value upload_max_filesize = 2M
```

By keeping up with security releases some will argue that there is no need to hide which version of PHP you are running.
There is a broader discussion of this debate in Section K.
In the PHP setting you can also [limit information about PHP](http://simonholywell.com/post/2013/04/three-things-i-set-on-new-servers.html) which is exposed by adding this to your php.ini file:

```
expose_php = Off
```

You can also explicitly disable PHP functions which allow scripts to reference other URLs.

```
allow_url_include = Off
allow_url_fopen = Off
```

You can also [disable PHP functions](http://www.cyberciti.biz/faq/linux-unix-apache-lighttpd-phpini-disable-functions/) which are considered dangerous.
You will want to test to see that your Drupal install doesn't require any of these functions.
You can grep from the Drupal root to find out if your site uses any of these functions.
Drupal's PHP filter leverages the exec() function, however there are lots of good reasons not to use the PHP filter.
You can add this to your php.ini file:

```
disable_functions = php_uname, getmyuid, getmypid,
passthru, leak, listen, diskfreespace, tmpfile, link,
ignore_user_abord, shell_exec, dl, set_time_limit, exec, system,
highlight_file, source, show_source, fpaththru, virtual,
posix_ctermid, posix_getcwd, posix_getegid, posix_geteuid,
posix_getgid, posix_getgrgid, posix_getgrnam, posix_getgroups,
posix_getlogin, posix_getpgid, posix_getpgrp, posix_getpid, posix,
_getppid, posix_getpwnam, posix_getpwuid, posix_getrlimit,
posix_getsid, posix_getuid, posix_isatty, posix_kill,
posix_mkfifo, posix_setegid, posix_seteuid, posix_setgid,
posix_setpgid, posix_setsid, posix_setuid, posix_times,
posix_ttyname, posix_uname, proc_open, proc_close,
proc_get_status, proc_nice, proc_terminate, popen
```

Drupal's status page has a link to the output of phpinfo() and you should decide whether or not you want to exclude that function in this list.
You want to be able to limit what PHP has access to in the file system.
Note that you may want to give slightly more access to PHP than just the Drupal root directory as it can be beneficial to put some files (like a salt.txt file) outside of the base directory.
This can also be set in Apache, but I've tried to keep the PHP specific information inside the php.ini file:

```
open_basedir = /var/www
```

Make sure the session path is outside the root web directory and not readable or writable by any other system users.
You will also want to set a temporary upload file directory that is outside of the web root.
This can be specified in the php.ini file:

```
session.save_path = "/tmp"
upload_tmp_dir = "/tmp"
```

## G) Database Layer

With Drupal's database abstraction layer you can now run it on [MySQL](https://www.mysql.com/), [SQLite](https://www.sqlite.org/) or [PostgreSQL](http://www.postgresql.org/) out of the box.
There are in fact a number of popular MySQL forks like [MariaDB](https://mariadb.org/) and [Percona](http://www.percona.com/software/percona-server).
Drupal can run with MSSQL too, but there will be more support for MySQL flavours of SQL.
Oracle support for PHP is weak, so it is not recommended to use this database.
We are not aware of any security advantages of one over the other.

The database for Drupal can run on the same server, but for performance reasons it can be beneficial to set it up on another server.
You want to ensure that your server environment is robust enough that it cannot be easily brought down by a Denial of Service (DOS) attack.
There are a few server side tools to help with this, but mostly it's useful to have a buffer, even at your highest traffic times, so that your site is always responsive.

At the point where your server environment spreads on to more than one system, it begins to make sense to have a second network behind the web server, possibly including a VPN.
It is quite likely that if the database is moved to an external server that there may soon be other servers including more than one front-end server too.

There is a lot that can be done to [secure your database](http://www.greensql.com/content/mysql-security-best-practices-hardening-mysql-tips).
Much of it comes down to reviewing [access permissions for the Drupal user](https://drupal.org/documentation/install/create-database) (set in Drupal's settings.php), the backup user (which has read only access to do regular backups) and the database's root user (which obviously has access to everything) and verifying that they all have complex passwords.
These need to be unique passwords and the root password should not be stored on the server, but rather in your encrypted Keepass database.

If your server is running locally, you can disable access for MySQL to the network and force it to only use the internal IP address.
If your web server and database are on different servers, you won't be able to do this, but you will be able to restrict what address MySQL will listen on.
If your web server and database server share a LAN, bind MySQL only to the LAN IP address and not any Internet-facing ones.
For a machine running both the web server and MySQL, you can add this to your my.conf file:

```
bind-address=127.0.0.1
```

Be sure to [review your databases, users and permissions](http://www.symantec.com/connect/articles/securing-mysql-step-step) to see that there are not any sample users or old databases still enabled on the server and that you are not giving greater access to a user than they need.
You should also review the file system to see that the database files are restricted.

If you need a graphical tool like [phpMyAdmin](http://www.phpmyadmin.net/home_page/index.php), disable it after use.
Web applications like this can also be tightened down by placing them on a different port, firewall that port from other than 127.0.0.1, and always access it via ssh port forwarding.
Access to these tools can also be limited to IP addresses for extra protection.
Note that any software you use should be regularly updated to ensure that it receives any security enhancements, particularly if stored on the server.
You can restrict access to phpMyAdmin via .htaccess or by configuring Apache to request an HTTP username/password login.
They can also be restricted to only allow access from certain trusted IP addresses.
This is an important vulnerability as it could give acracker full access to your databases.
It can be beneficial to put phpMyAdmin in it's own VirtualHost and even run it on a non-standard port.
Force HTTPS connections to phpMyAdmin - do not use regular HTTP.
Also consider the implications of allowing database access via the web server: There is little benefit if you have restricted which interfaces MySQL will listen on, as described above, but then allow control of the database from an Internet-facing web page.

## H) Drupal

### 1) Files

[Verify Drupal file permissions on the server](https://drupal.org/node/244924).
You really need to restrict write access to the server and verify that the right users/groups have the access that they need for Drupal to operate effectively.
One can set all of Drupal's files to be read only, only allowing for file uploads, cached files, sessions and temporary directories with write permissions.
The major limitation of this approach is that it makes applying security upgrades more difficult.

By default, Drupal 7 disables execution of PHP in directories where you can upload PHP.
Check the .htaccess file in the files directory.
You can also add this to your Apache Virtual Host to ensure that no handlers have been overlooked.

```
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
```

Drupal needs to be able to write to the server to be able to perform certain tasks like managing file uploads and compressing/caching CSS/JS files.
Ensure that Apache has write access to /tmp and also to the public sites folder:

```
Debian: chown -R www-data:www-data
sites/default/files
CentOS: chown -R nobody:nobody sites/default/files
```

Make sure that you are only allowing users to upload file types that have limited security problems with them.
Text and images are usually quite safe.
There have been some exploits on PDF files, but they are quite rare.
Microsoft Office documents should be scanned if they are going to be uploaded onto the server.
[ClamAV](https://drupal.org/project/clamav) can be incorporated into Drupal to scan uploaded files for viruses and other malicious code.
Acquia recommends excluding the following file types: flv, swf, exe, html, htm, php, phtml, py, js, vb, vbe, vbs.


### 2) Drush

Drush is a command line shell and scripting interface for Drupal.
We strongly recommend using [Drush](https://github.com/drush-ops/drush) on both staging and production servers because it simplifies development and maintenance.
Note that the version of Drush packaged with your OS is likely to be extremely out of date.

Although Drush used to be installed best with [PHP's PEAR](http://pear.php.net/), the current best practice is with [Composer](https://getcomposer.org/doc/00-intro.md#system-requirements) (the dependency manager for PHP).
See install details on the [Drush git page](https://github.com/drush-ops/drush#installupdate---composer).

There is a [Security Check](https://drupal.org/project/security_check) module available for Drush which is a basic sanity test for your configuration.
When the module is added, you can run this against your site from Apache's document root (docroot) on the command line using:

```
drush secchk
```

As with the server configuration in general, document what you are using.
Drush makes this fairly straightforward as you can simply export a list from the command line:

```
drush pm-list --type=Module --status=enabled
```

Cron is the Linux time-based job scheduler and it is used for a lot of key Drupal functions.
Check to see that you are running cron several times a day.
For Drupal 7 and above, [if there is traffic to the site, cron jobs are run every 3 hours](https://drupal.org/cron).
The status page will tell you when the last time cron was run on the site.
You may want to set up a Linux cron job using using Drush if you have either a low traffic site or have special requirements.

To run cron on all of your sites in /home/drupal - from the command line enter crontab -e and then insert:

```
30 2,6,11,18 * * * cd /home/drupal && drush
@sites core-cron -y > /dev/null
```

You will need developer modules to help you build your site, but they are a security risk on your production site and need to be disabled.
Many modules (such as Views) have separate administration screens that can also be disabled in a production environment.
They are absolutely required when building the site, but can be disabled when they are not in use.It is always a good practice to see if there are any unnecessary modules can be disabled on your site.
This also offers performance benefits.
Views is an incredibly powerful query building tool.
Because of that, it is important that all Views have explicit access permissions set at /admin/build/views

### 3) Errors

Check the Status Report and Watchdog pages regularly and resolve issues - Drupal should be happy! This needs to be done regularly, even after launch.
Remember that you can more quickly scan your logs by filtering for PHP errors.
With the [Views Watchdog](https://drupal.org/project/views_watchdog) module you could also build custom reports to display on your website.
On your production server, make sure to disable the display of PHP errors.
These should be recorded to your logs, but not visible to your visitors.
On your staging site you will want to see those errors to help you debug PHP problems, but it is a potential vulnerability to have those exposed.This won't catch all PHP errors however, and so it is also useful to review the error log of the web server itself.

Watchdog is a good tool, but is [limited in a number of ways](http://www.asmallwebfirm.net/blogs/2013/04/achieving-drupal-log-bliss-splunk).
Simply because it is database dependent, even having a lot of 404 errors can affect performance.
Fortunately, logs can be easily directed to the server's syslog, with the [Syslog Access](https://drupal.org/project/syslog_access) module, which also allows you to leverage your favourite log management tool.
The Drupal Handbook also has a great resource for how to [send your logs to Syslog](https://drupal.org/documentation/modules/syslog) with integrated logging.

### 4) Core and Contrib Hacks

Before launching your site (and periodically afterwards) it is useful to run the [Hacked!](https://drupal.org/project/hacked) module to check what code differs from what was released on Drupal.org.
Particularly when the [diff](https://drupal.org/project/diff) module is enabled this is a powerful tool to evaluate your code.
There are millions of lines of code in a given Drupal site, so Hacked! is a really valuable analysis tool.
If you need to apply patches against the stable released version of the code, the patch should be in a clearly documented directory.
It is unfortunately a common practice for less experienced Drupal developers to cut corners and hack core to provide some functionality that is required.
There are lots of reasons why this is a bad idea and [why responsible developers don't hack core](http://drupal.stackexchange.com/questions/59054/why-dont-we-hack-core).
For the purposes of this document it is sufficient to say it makes it harder to secure.
The [same is true for contributed modules](http://www.bluespark.com/blog/youre-doing-it-wrong-dont-hack-drupal-core-change-text), you shouldn't have to alter the code to customize it most of the time.
The Hacked! module is very useful in identifying when modules no longer are the same as their releases on Drupal.org.
Being able to quickly scan through hundreds of thousands of lines of code and find differences against known releases is a huge security advantage.

You can also generate Drush make file from an existing Drupal site and then recreate a clean copy of the codebase which you can then diff (a command line comparison tool) to determine if your site has been hacked.

```
drush generate-makefile make-file.make
drush make make-file.make -y
```

It is recommended to run all modules you use through the [Coder](https://drupal.org/project/coder) module, but especially any custom built modules and themes.
This module [can give you suggestions](https://drupal.org/node/2135539) on how to follow the [Drupal communities coding standards](https://drupal.org/coding-standards).

It can also help you identify other coding errors that may affect your site.
Particularly when building custom modules the Coder module can help identify [unsanitized user input](https://drupal.org/node/101495), [SQL injection vulnerabilities](http://www.pixelite.co.nz/article/sql-injection-and-drupal-7-top-1-10-owasp-security-risks) and [Cross Site Request Forgery (CSRF)](http://drupalscout.com/knowledge-base/introduction-cross-site-request-forgery-csrf) problems.
It is unfortunately quite common for developers to extend Drupal by forking existing projects and not provide enhancements back to the community.
Doing this breaks assumptions within the Update module but more importantly makes upgrades much more difficult.
Even with a properly documented patch, it is a lot of work to upgrade, patch and re-write a function in a live website.

By contributing the improved code upstream, you can avoid that often painful process.
The peer review that comes with contributing your code back to the community is a secondary benefit: your codebase will become more robust because more people will understand it.
Your [bus count](http://www.thesalesengineer.com/2011/06/20/whats-your-se-bus-count/) (the number of people who can go missing from a project by either being hit by a bus or winning the lottery) will increase by releasing your code.
Publishing the code elsewhere forces you to actually think about what is required.
further, if someone tries to install your code/system, they might notice missing parts or for that matter parts that might be confidential.

### 5) Administration

Drupal has a very fine grained and customizable permissions model.
In its simplest form, users are assigned roles and each role is given permissions to various functions.
Take the time to review roles with access to any of Administer filters, Administer users, Administer permissions, Administer content types, Administer site, Administer configuration, Administer views and translate interface.
It is useful to review the permissions after upgrades to verify if any new permissions have been added.

Don't use "admin" as your user/1 admin name.
It's the first one that a cracker is going to try, so be a bit more unique.
Obscurity isn't the same as security, but no need to give them their first guess when choosing user names.
Another good practice with regards to user/1 is to [completely disable the account](https://www.drupal.org/node/947312#disable).
With the advent of Drupal 7 and drush, user/1 is not required to administer Drupal websites anymore, and thus can be simply blocked.
The account can be re-enabled as needed through drush or directly in the database.

As with other server user accounts, you will want to restrict who has access to servers.
Make sure to delete any test or developer accounts on the production server.

Don't run Drupal without enabling the Update module that comes with core.
Drupal core and contributed modules use a structured release process that allows your administrators to be proactively alerted when one of those modules has a security release.
Any piece of code is susceptible to a security issue, and having a central repository that a Drupal site can compare against is key to the security paradigm.
Aside from the releases that have fixes for known security problems, some modules (or a version of that module) may become unsupported.
This is also a security problem, in that you will not receive updates if there are security problems that are identified with the module.
The Update module also allows you to get a daily or weekly email if there are security upgrades that need to be applied.

Drupal's input filters are very powerful, but can provide a vulnerability.
Don't enable the PHP filter which is available in Drupal core.
Installing the [Paranoia](https://drupal.org/project/paranoia) module can really help enforce this practice.
The PHP filter makes debugging more difficult and exposes your site to a greater risk than it is worth.
All PHP code should be written to the file system and not stored in the database.
Another input filter that is problematic is Full HTML which should only be granted to administrator roles. Anyone with the Full HTML filter can craft malicious JavaScript and gain full admin access to any website on the same domain as the Drupal website.
If needed, you can add some additional tags to the Filtered HTML input format but be cautious.

### 6) Modules to Consider

There are [a lot of Drupal security modules](https://github.com/wet-boew/wet-boew-drupal/issues/248).
Depending on your needs you will want to add more or less than those listed here.

*   [Automated Logout](https://drupal.org/project/autologout) - ability to log users out after a specified time of inactivity
*   [Clear Password Field](https://drupal.org/project/clear_password_field) - Stops forms from pre-populating a password
*   [Drupal Tiny-IDS](https://drupal.org/project/tinyids) - An alternative to a server-based intrusion detection service
*   [Local Image Input Filter](https://drupal.org/project/filter_html_image_secure) - Avoids CSRF attacks through external image references
*   [Login Security](https://drupal.org/project/login_security) - Set access control to restrict access to login forms by IP address
*   [Paranoia](https://drupal.org/project/paranoia) Limits PHP functionality and other controls
*   [Password Policy](https://drupal.org/project/password_policy) - Enforces your user password policy
*   [Session Limit](https://drupal.org/project/session_limit) - limit the number of simultaneous sessions per user
*   [Settings Audit Log](https://drupal.org/project/settings_audit_log) - Logs who did what, when
*   [Security Kit](https://drupal.org/project/seckit) - Hardens various pieces of Drupal
*   [Secure Login](https://drupal.org/project/securelogin) - An alternative to Secure Pages above to provide secure HTTPS access, but without the mixed-mode capability
*   [Secure Pages](https://drupal.org/project/securepages) - Manages mixed-mode (HTTPS and HTTP) authenticated sessions for enhanced security (note required core patches)
*   [Secure Permissions](https://drupal.org/project/secure_permissions) - Disables the UI to set/change file permissions
*   [Security Review](https://drupal.org/project/security_review) - Produces a quick review of your site's security configuration
*   [Shield](https://drupal.org/project/shield) - Protects your non-production environment from being accessed
*   [Restrict IP](https://drupal.org/project/restrict_ip) - Restrict access to an administrator defined set of IP addresses
*   [Username Enumeration Prevention](https://drupal.org/project/username_enumeration_prevention) - Stop brute force attacks from leveraging discoverable usernames

### 7) Modules to Avoid on Shared Servers

Many Drupal modules intended to help developers develop code also disclose sensitive information about Drupal and/or the webserver, or allow users to perform dangerous operations (e.g.: run arbitrary PHP code or trigger long-running operations that could be used to deny service).
These modules can be used to debug locally (and many are essential tools for Drupal developers), but should never be installed on a shared environment (e.g.: a production, staging, or testing server).

To limit the damage a malicious user can do if they gain privileged access to Drupal, it's not sufficient for a development module to be simply disabled: the files that make up the module should be removed from the filesystem altogether.
Doing so prevents a malicious user from enabling it and gaining more data about the system than they would be able to otherwise.
Note that it is difficult to automatically enforce that these modules are not deployed to shared systems: developers need to understand why they should not commit these modules and take care to double-check what they're about to deploy.

Some popular development modules which should not be present on any shared website include:

* [Delete all](https://www.drupal.org/project/delete_all) — This module allows someone with sufficient privileges to delete all content and users on a site.
* [Devel](https://www.drupal.org/project/devel) — Besides letting users run arbitrary PHP from any page, Devel can be configured to display backtraces, raw database queries and their results, display raw variables, and disable caching, among other things.
* [Drupal for Firebug](https://www.drupal.org/project/drupalforfirebug) — Drupal for Firebug outputs the contents of most variables, raw database queries and their results, display PHP source code, and can be used to run arbitrary PHP. Furthermore, it does all this by interfacing with browser developer tools, making it difficult to determine if this module is enabled by glancing at the site.
* [Theme Developer](https://www.drupal.org/project/devel_themer) — This module, which depends on the Devel module mentioned earlier, is very useful for determining which theme files / functions are used to output a particular section of the site, but it displays raw variables and slows down the site significantly.
* [Trace](https://www.drupal.org/project/trace) — This module can be used to display backtraces and raw variables, among other things.

Note that most "normal" modules can be dangerous if a malicious user gains privileged access to Drupal.
You should evaluate each new module you install to determine what it does and whether the features it brings are worth the risks.
Some modules to take into special consideration are:

* [Backup and Migrate](https://www.drupal.org/project/backup_migrate) allows you to download a copy of the site's database. If restrictions placed upon you by your hosting provider prevents you from being able to make backups, this module will allow you to do so; but a malicious user with privileged access would be able to download a copy of the whole Drupal database, including usernames, passwords, and depending on your site, access keys to the services you use.
* [Coder](https://www.drupal.org/project/coder) — This module is very useful for ensuring your code conforms to coding standards but can be used to display the PHP that makes up modules.

### 8) Drupal Distributions

Drupal distributions provide turnkey installations that have been optimized for specific purposes, generally with a curated selection of modules and settings.
There are now two distributions which have been specifically built for security, [Guardr](https://drupal.org/project/guardr) and [Hardened Drupal](https://drupal.org/project/hardened_drupal).
Guardr is built to follow the [CIA information security triad](https://en.wikipedia.org/wiki/Information_security): confidentiality, integrity and availability.
It is worth watching the evolution of these distributions and installing them from time to time if only to have a comparison of modules and configuration options.

### 9) Miscellaneous

Review the discussion in Section K and decide if you are going to remove the CHANGELOG.txt file.
Ensure that you can keep up security upgrades on a weekly basis and **do not hack core**!
If you plan to distribute your live site so that you can do testing or development outside of a controlled environment, consider building a [sanitized version of the database](http://drupalscout.com/knowledge-base/creating-sanitized-drupal-database-backup).
This is especially important if you have user information stored in the database.
For many government sites this may not be necessary.

## I) Writing Secure Code

There are lots of great resources about how to write secure code.
The [Drupal handbook page](https://drupal.org/writing-secure-code) is a great place to start as it is focused directly on the best practices defined by this community.
In Drupal 7 it is important to remember that the themes all have PHP in them and that this is a potential place of a security breach.
It isn't uncommon for themers to put a lot of PHP inside of a theme rather than in a separate module.
It's also more difficult to keep up with security releases in themes, as they are by their very nature customized.
OWASP has a good [PHP Security Cheat Sheet](https://www.owasp.org/index.php/PHP_Security_Cheat_Sheet) with information specific things to watch out for when running PHP applications.
They also have a more generic document on [Secure Coding](https://www.owasp.org/index.php/Secure_Coding_Cheat_Sheet) and a more specific one on [HTML5 Security](https://www.owasp.org/index.php/HTML5_Security_Cheat_Sheet).
There are also lots of good blogs on writing secure code, [like this one,](http://www.addedbytes.com/articles/writing-secure-php/writing-secure-php-1/) highlighting general approaches to PHP coding.
Code review can be used in order to find flaws in existing code and discover potential bugs.
OWASP offer a [free book](https://www.owasp.org/index.php/Category:OWASP_Code_Review_Project) that can guide you on that process.
Basically, you can do it manually using the same guidelines as when writing secure code, but you can as well use automated tools.
Theses can be [installed in a continuous integration system such as Jenkins](http://jenkins-php.org/) in order to periodically checks for flaws.
Common clarity and code style rules can spot weak code that is not directly tied to security but can be an indicator on code quality, thus giving a hint on security.
Rare tools exists to find security related weaknesses in PHP frameworks and PHP such as [phpcs-security-audit](https://github.com/Pheromone/phpcs-security-audit) that even support Drupal, but like many tools they need manual follow up and tend to execute slowly.

Common Drupal secure coding practices are:

*   Never trust user input.
    With [sanitization functions](https://api.drupal.org/api/drupal/includes%21common.inc/group/sanitization/7) like check_plain(), filter_xss(), and filter_xss_admin() it is easy in Drupal to clean strings on output.
    Any variable in a template or HTML output should pass through one of these.
*   Protect yourself from SQL Injection through leverage Drupal's [database abstraction layer](https://api.drupal.org/api/drupal/includes%21database%21database.inc/group/database/7).
    Drupal 6 should use [parameterization](https://drupal.org/node/101496).
*   Use preg_replace_callback() rather than preg_replace() as the latter can allow matches to be evaluated as PHP code although the \e modifier that introduce this flaw is now deprecated in PHP.
*   Always use the Drupal functions when possible instead of plain old PHP.
*   Drupal comes with jQuery and leverages it extensively.
    Do not rely on JavaScript for validation.
*   If you are using eval() or drupal_eval() this is a potential security risk if PHP input provided contains malicious code.
    If you do this, you can add a new permission in your module so that an admin needs to explicitly assign permissions to a user role.
*   Same precautions should be taken with functions such as exec(), system(), fopen(), delete() and others that execute external applications or interact directly with the file system.

As David Strauss wrote recently, [All Code is Debt](https://www.getpantheon.com/blog/all-code-debt).
"All of the custom code you've written yesterday, rewritten today, and what you'll write tomorrow ― you will be burdened with maintaining, forever." Code needs to be maintained on a regular basis to ensure that it is keeping up with the latest security best practices.
When writing code, testing is important and security testing should be part of the process.
OWASP publish a very complete [Testing Guide](https://www.owasp.org/index.php/OWASP_Testing_Project) as well as an [Application Security Verification Standard](https://www.owasp.org/index.php/Category:OWASP_Application_Security_Verification_Standard_Project) that goes deep into details.
The verification standard could also be used as a complete security requirement list when designing new modules for your Drupal site.
Open source tools such as [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) and [Subgraph Vega](http://www.subgraph.com/products.html) provide graphical user interface to perform dynamic scanning of Web sites.
For complex Drupal sites they might have some difficulties but they can still be used as a intercepting web proxy in order to perform manual testing.

## J) Development, Staging and Production

Any formalized development process should have three distinct server environments.
The development environment can simply be a developer's computer (or perhaps several developers' computers).
The staging and production servers should be essentially identical.
The role of the staging server is to document and test the migration process to verify that the code and configuration can move onto the production server.
For more information refer to OpenConcept's blog post on the [path of code vs content](http://openconcept.ca/blog/mgifford/flow-content-code).The code for your Drupal site should be stored in a central repository.
The Drupal community has generally adopted [Git](http://git-scm.com/), but there are other valid options for version control.
A developer will pull/push/clone/branch to/from that repository.
New code is committed and pushed from the development environment into the central repository, and can then be pulled onto the staging environment.
If it passes testing there, it can then be pulled into production.
The database on the staging server can simply be cloned from the production server using Drush.
Assuming that the new code works well with the production database, you can be reasonably certain that you will be able to migrate that code and configuration to the production site.
This is definitely more complicated, but both the staging and production environments will need to be accessible via Drush and the Git repository.

You will need to set up an SSH user with its own SSH keys to allow you to use Drush aliases to transfer databases between staging and production.
You may also want to have another account to be able to transfer uploaded files which probably would not be managed under version control.
Using an external site like [GitHub](https://github.com/) for storing your repository provides access to some great additional tools like [Travis](http://docs.travis-ci.com/user/getting-started/) and [SauceLabs](https://saucelabs.com/builder) which can help you deliver a more reliable site.
You can also set it up on your staging or development server.
Limit access between servers.
There is a potential risk from having a semi-porous boundary between these environments, but the risks are far outweighed by the benefits.
Having a central Git repository gives you control across all environments at one time.
Being able to diff any change allows you to quickly identify where changes have been made and know why.
Drush is certainly powerful, but only experienced users should have access to it.
With a solid backup plan, even if this is compromised, it can be quickly restored.

## K) Regular Maintenance

No security plan is foolproof.
You need regular backups to ensure that you can restore your system quickly if required.
With both the database and file system it is important to have both local and remote backups.
You want the local backup because that allows you to quickly restore the site if there is a problem.
You want a remote backup in case of total system failure.
There are many ways to setup and configure this.
Some helpful backup solutions include:

*   [Bacula](http://www.bacula.org/)
*   [rsync](https://rsync.samba.org/) / [rsnapshot](http://www.rsnapshot.org/)
*   [mysqldump](https://dev.mysql.com/doc/refman/5.1/en/mysqldump.html)
*   [xtrabackup](http://www.percona.com/doc/percona-xtrabackup)

Remember that a backup is only good if it can be restored.
It's a best practice to make use of [RAID drives](https://en.wikipedia.org/wiki/RAID), but RAID should be used as a failsafe and not considered a backup strategy.
Backups should be stored regularly locally, but there also need to be regular, long-term backups stored off-site.
Make sure to evaluate your backup procedures and test your restores to verify that they are working effectively.
Drupal.org releases [security updates](https://drupal.org/security) on Wednesdays when needed which are broadcast by an email list, [RSS feeds](https://drupal.org/security/psa/rss.xml) and [Twitter](https://twitter.com/drupalsecurity).
Subscribe to the security newsletter for updates (you will need a Drupal.org account and the instructions are on the sidebar of the previous link).
It is also useful to check the Status page and Watchdog pages in your Drupal site.

[SELinux provides auditing services](http://drupalwatchdog.com/volume-2/issue-2/using-apache-and-selinux-together) which are worth monitoring.
You should be watching your server logs, particularly your Apache error log:

```
tail -f /var/log/httpd/error_log
grep 'login.php' /var/log/httpd/error_log
egrep -i "denied|error|warn"
/var/log/httpd/error_log
```

Security best practices are constantly changing.
OWASP has released their [Top 10 for 2013](https://www.owasp.org/index.php/Top_10_2013-Introduction) and it is somewhat similar to the 2010 list.
The Top 10 for 2010 was leveraged to look at [how it applies to Drupal](http://www.cameronandwilding.com/blog/pablo/10-most-critical-drupal-security-risks).
This needs to be updated, and reviewed, particularly if you are writing any custom code.
It's a simple idea, but it can be good to search [Google for test data](https://www.google.com/search?q=site:healthcare.gov%20intext:%22test%22) that might have been left in development or exposed in an upgrade.
Anything in a draft mode should never be exposed to the Internet.
[Acquia's Insights](https://www.acquia.com/products-services/acquia-network/cloud-services/insight) provides a useful tool to get regular insights on how to improve your website.
Their security section will be able to do a quick review of your website to check on a number of security related issues.
They also address performance, best practices, SEO and code analysis.
With the [Acquia Network Connector](https://drupal.org/project/acquia_connector) module, this can be easily and securely done on any website accessible to the Internet.
Their dashboard provides an easy way for you to regularly monitor important elements of your site.
[Qualys](https://www.qualys.com/) and [Rapid7](http://www.rapid7.com/) both offer a number of other security monitoring and risk assessment services.
These are included in Acquia's hosting.

## L) Points of Debate - Security by Obscurity

There is a bit of a division within the security community as to whether one should expose information about what versions of software are being used.

### 1) Make it Obscure

Leaving a CHANGELOG.txt file visible does nothing to improve security, rather it only helps inform an attacker how to focus their research efforts to find a zero day attack, a contrib module vulnerability even faster, or just disable any scripted attacks that aren't relevant to your stack.
Justin C. Klein Keane in his blog Open Source Software Security strongly [recommends hiding both the Drupal and server identification](http://www.madirish.net/242).

### 2) Make it Transparent

In many cases where the CHANGELOG.txt has been removed, it is because the webmaster hasn't done a Drupal core upgrade and they are looking for a way to obscure that fact.
By keeping the CHANGELOG.txt up-to-date at the very least it indicates that someone is paying attention to security updates.
There are [easy ways to fingerprint Drupal](https://drupal.org/comment/3481992#comment-3481992) and the security team could hide access to this file in the .htaccess file that comes with Drupal core if they were concerned.
By making it transparent, there is an additional reason for developers to make it a priority to upgrade core when there is a security release.

### 3) Be Consistent

While there is some discussion on the benefits of hiding CHANGELOG.txt there is agreement that when security releases are announced, that developers must apply them quickly so that the site cannot be compromised.
By default, the Linux distribution, Apache and PHP also announce information that can be turned off in their configuration files.
It is good to be consistent and have your reasoning documented so that it is clearly understood.

## M) Additional Resources

### 1) General guidelines

#### Drupal security

*   [Standards, security and best practices - Drupal.org wiki](https://drupal.org/node/360052)
*   [Writing secure code - Drupal.org wiki](https://drupal.org/writing-secure-code)
*   [Securing your site - Drupal.org wiki](https://drupal.org/security/secure-configuration)
*   [Drupal Security Group Discussion](https://groups.drupal.org/security)
*   [Drupal Security Report - Acquia](http://drupalsecurityreport.org/)
*   [Drupal Security - Acquia](https://docs.acquia.com/cloud/arch/drupal-security)
*   [Security: How the world's largest open source CMS combines open and security - Acquia](https://www.acquia.com/blog/keeping-drupal-secure)
*   [Drupal, SSL and Possible Solutions - Acquia](http://drupalscout.com/knowledge-base/drupal-and-ssl-multiple-recipespossible-solutions-https)
*   [Drupal Watchdog Magazine - Security Edition](http://drupalwatchdog.com/issue/toc/2/2)

#### Secure hosting

*   [Linux: 25 PHP Security Best Practices For Sys Admins - Nixcraft](http://www.cyberciti.biz/tips/php-security-best-practices-tutorial.html)
*   [Hardening an SSL server against the NSA - xin.at](http://wp.xin.at/archives/1359)
*   [LinuxSecurity.com](http://www.linuxsecurity.com/)
*   [COTS Security Guidance (CSG) (CSG-09\G) Intrusion Prevention System (IPS) - CSEC](https://www.cse-cst.gc.ca/en/node/288/html/12807)
*   [COTS Security Guidance (CSG) (CSG-10\G) Overview of OS Security Features - CSEC](https://www.cse-cst.gc.ca/en/node/289/html/3356)
*   [How to Deploy HTTPS Correctly - EFF.org](https://www.eff.org/https-everywhere/deploying-https)

#### Organizaitonal Security

*   [Communities @ Risk: Targeted Digital Threats Against Civil Society](https://targetedthreats.net/)
*   [Security in a Box - Tactical Technology Collective](https://securityinabox.org/)
*   [SocialEngineer.org](http://www.social-engineer.org/)

### 2) Videos

*   [Doing Drupal Security Right - DrupalCon London](http://london2011.drupal.org/conference/sessions/doing-drupal-security-right)
*   [Building and Securing Government Drupal Sites in the Cloud - DrupalCon Denver](http://denver2012.drupal.org/program/sessions/building-and-securing-government-drupal-sites-cloud)
*   [Securing Drupal Sites for Government Agencies - Acquia](https://www.acquia.com/resources/acquia-tv/conference/securing-drupal-sites-government-agencies-september-5-2012)
*   [Drupal Videos About Security on Archive.org](http://archive.org/search.php?query=drupal%20security%20AND%20mediatype%3Amovies&amp;sort=-date)
*   [Semantic Forgeries in Drupal's Form API - Greg Knaddison](https://vimeo.com/8741925)
*   [Drupal Security by Ben Jeavons from Acquia](https://www.youtube.com/watch?v=dC-TjZkMTk8)

### 3) Third party tools

*   [Retina Network Security Scanner - beyondtrust.com](http://www.beyondtrust.com/Products/RetinaNetworkSecurityScanner/)
*   [N-stalker Web Application Security Scanner](http://www.nstalker.com/)
*   [Syhunt Web Security Audits](http://www.syhunt.com/)
*   [Greensql Database Security](http://www.greensql.com/)

### 4) Books

*   [Cracking Drupal by Greg Knaddison](http://crackingdrupal.com/)
*   [O'Reilly.com's Linux Server Security by Michael D. Bauer](http://shop.oreilly.com/product/9780596006709.do)
*   [Hacking Linux Exposed by Bri Hatch and James Lee](http://www.hackinglinuxexposed.com/)
*   [Announcement of New Cyber Security Books published by scitech](http://scitechconnect.elsevier.com/elsevier-publishes-seven-new-cyber-security-books/)
*   [SELinux System Administration by Sven Vermeulen](https://www.packtpub.com/networking-and-servers/selinux-system-administration)
*   [OWASP Application Security Guide For CISOs](https://www.owasp.org/index.php/OWASP_Application_Security_Guide_For_CISOs_Project)
