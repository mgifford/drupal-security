B) Principles of Security
=========================

.. image:: /_static/images/noun/noun_5983_cc.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: Shield from the noun project. 

**There is safety in the herd:**
  | Leverage large, well maintained open-source libraries (packages) with a critical mass of users and developers.

  | Use compiled packages and check data integrity of downloaded code.

  | Start with a popular and well maintained Linux distribution (Debian/Ubuntu or Red Hat/CentOS).

**Order matters:**
  | Don't open up services to the Internet before your server is properly secured.

**Limit exposure:**
  | Only install and maintain what is necessary.

  | Reduce the amount of code installed.

  | Review server configuration regularly to see if it can be streamlined.

**Deny access by default:**
  | Only allow access where it is needed, and make all access policies deny by default.

**Use well known security tools:**
  | There are well supported libraries that limit exposure, and check for intrusion.

  | Many suggestions are provided in the Server Security, PHP & Drupal sections.

**Avoid writing custom code:**
  | Even large organizations find it difficult to invest properly in regular, ongoing code reviews.

  | Minimize the use of any custom code.

**Contribute back: No software is ever perfect.**
  | There is always room for improvement.

  | Make the code you use better and give it back to the community.

  | If you do it properly you won't have to rewrite your code with the next security release and you will get free peer review and ongoing maintenance.

**Limit access:**
  | There needs to be clear, documented roles of who has access to what.

  | Only use root access when required and do so through sudo so people are not actually logging in as root.

  | Isolate distinct roles where possible. Each person with access requires a separate account as shared accounts are inherently insecure.

**Make your application happy:**
  | When running smoothly your server should not be generating errors.

  | Monitor your server then investigate and resolve errors.

**Document everything:**
  | Make sure you have an overview of any customizations which may have been done or any additional software that may have been added.

**Limit use of passwords:**
  | Have sane organizational policies on password requirements.

  | Keep track of your passwords in controlled, encrypted programs.

  | Where possible use password-less approaches such as SSH key pairs which are more secure.

.. image:: /_static/images/noun/noun_6482_cc.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: Minus from the noun project. 

**Don't trust your backup:**
  | Define and review backup procedures and regularly test that you can restore your site.

**Obscurity isn't security:**
  | Organizations need to have their security policies well documented and internally transparent.

  | Section :ref:`debate-obscurity` discusses this issue in detail.

**Security is big:**
  | It is a mistake to assume that one person can do it well in isolation.

  | Having access to a team (even outside of the organization) will help.

**Remember, you're still not safe:**
  | Have an audit trail stored on another system.

  | If your site is compromised, take the time to find out how.
  
  | Use proper version control for all code and configuration.

**Not just for techs:**
  | Upper management needs to take the time to understand these general principles of IT security as they have profound implications for the whole organization.
