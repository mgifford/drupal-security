C) Security Concerns for Managers
=================================

.. image:: /_static/images/noun/noun_43646_cc.*
   :width: 150px
   :align: right
   :scale: 50%
   :alt: A woman manager from the noun project. 

There are many assumptions about IT security that need to be fundamentally
rethought in the era of the Internet. Organizations are struggling to come to 
terms with this at the same time as working to understand the implication of
cloud-based services. What we can be certain of is that this field is
accelerating and organizations need to keep up.

The first principle is to understand that time corrodes security and on the
Internet time moves very fast. You can't assume that any service you buy or
develop is currently secure or will remain that way for long. It is critical to
understand what investments have been made and how they are maintained.

Web hosting and application development are different fields and one cannot
simply outsource security upgrades to someone else to do. No web hosting company
can "take care" of your server security in isolation of the application that is
running on it. Ultimately, someone familiar with your website and its content 
needs to be involved in performing upgrades.

Third-party agencies are ultimately going to be involved in supporting your site. 
The protocol for communicating with these agencies needs to be clear and well 
documented. This recently happened with a large Canadian municipal website that 
was redirected to an image of a `dancing banana`_ using an approach known as 
`social engineering`_. By leveraging human vulnerability, crackers were able 
to gain control of critical infrastructure. Properly documented procedures are 
important, as third-party services can often be manipulated phony email or 
telephone requests.

It is also important to remember that one person working in isolation cannot be
expected to be an expert in all aspects of Internet security. This is a vast
area of expertise and it is changing quickly. It's important that your security
person has ongoing training and is engaged with both the Drupal and wider
security communities to keep up with the latest threats, vulnerabilities and
mitigation strategies.

Schedule time for a skilled security expert outside the core team to double
check the server/Drupal configuration every quarter. This does not have to be a
consultant, but it should be someone outside of the website development team.

Everyone wants security to be simple, it isn't. It's a matter of determining, as
an organization, how much risk you want to be exposed to. You can invest as much
or as little on security as you want, but the risks are generally inversely
proportional to resources spent on tightening your system. Security has costs as
well as benefits. Complex systems are usually less secure because it costs
relatively so much more to secure them.

Many organizations have policies for `Threat and Risk Assessments`_. However, as
we've seen with the implementation of `Healthcare.gov`_ political pressures
associated with large projects often push security concerns into a post-launch
phase. It is highly recommended to go through a `Application Threat Modeling`_
process. `Threat Risk Modeling`_ is also a recommended process to help expand
understanding of potential threats by using processes like `STRIDE or DREAD`_. By
`identifying and classifying an organization's assets`_ one can begin to
prioritize where to focus resources.

Thinking through attack vectors and limiting exposure is really important. I'm
sure that many of the sites that were compromised by the Shellshock_ bash bug in
that hit in September of 2014 simply hadn't disabled services that they weren't
using. Bash is a command processor that runs in a terminal window, so for most 
Drupal sites there simply isn't a need to expose it anyone other than properly 
authenticated Linux users.

As with most work, a great deal of security work lies in identifying and
eliminating assumptions. Document what is done, and be transparent in your work
so that your organization knows that it has the level of risk it wants to
maintain.

Organizations should also consider if the software that they use is properly
resourced. The Internet is built on free software, but much of it is backed by
corporations who are also providing services built on the expertise that they 
have built by contributing to open-source software. The `Heartbleed bug`_
cost the economy billions, but was largely caused because the OpenSSL library
was under-resourced. Although this is just one example, consider donating to
project like the `OpenSSL Software Foundation`_ which supports the security
infrastructure your organization depends on. Likewise consider supporting
organizations who contribute to `Drupal's security team`_.

Much security work should begin before anything is installed. Properly
considering security before beginning a server implementation is important.
Addressing security issues later in a project makes it impossible to do a
security evaluation of the base system. When setup is rushed, bad practices are
often used which then become patterns that are followed long after the site is
launched.

Implementing and enforcing a policy of using very complex passwords and 
`two-factor authentication`_ for any critical service, like email. Proper use of 
a secure,redundant password manager is also something that should be key for all
employees. If someone is able to hack into your Google Mail or GitHub account,
they can often access much more than your communications. Most services on the
Internet are keyed to email addresses and passwords to third-party services are
often stored. Identity theft online is a huge problem for institutions.

The `UK's Government Service Design Manual`_ is an excellent resource for any
large institution and it has a great section that applies directly to web
security,
`Security as enabler: Using technological change to build secure services`_.
In particular, I like the point that security shouldn't degrade user experience.

Don't ignore minor bugs. As `Darren Mothersele`_ mentions in his blog, it is
possible for a number of minor vulnerabilities to be chained together in a way
which can become a major exploit. Sites as large as GitHub have been
successfully targeted this way. As he says, The cost of (in)security is high
and "investment in security review and penetration testing is a Good Thing".

`IBM suggestes`_ that organizations should spend between 6 and 14% of their IT 
budget on security. The less organizations spend on security, the greater the likelihood that there will be security breaches. How much of this should be spent on web security will depend on the relative number of assets and vulnerabilities which are contained in the website. Only with a good picture of your over-all risk can you determine where it is best to invest in skills, processes and technologies to mitigate it. Think about what percentage of your budget you presently spend on web security, and if that is sufficient to cover the risks to what has become mission critical for most organizations.

.. _`dancing banana`: http://www.ottawasun.com/2014/11/24/mayor-says-imposter-managed-to-redirect-ottawaca-website
.. _social engineering: https://en.wikipedia.org/wiki/Social_engineering_%28security%29
.. _Threat and Risk Assessments: https://www.owasp.org/index.php/Threat_Risk_Modeling
.. _Healthcare.gov: https://www.healthcare.gov/
.. _Application Threat Modeling: https://www.owasp.org/index.php/Application_Threat_Modeling
.. _Threat Risk Modeling: https://www.owasp.org/index.php/Threat_Risk_Modeling
.. _`STRIDE or DREAD`: https://en.wikipedia.org/wiki/STRIDE_%28security%29
.. _Shellshock: https://en.wikipedia.org/wiki/Shellshock_%28software_bug%29
.. _identifying and classifying an organization's assets: http://www.networkmagazineindia.com/200212/security2.shtml
.. _Heartbleed bug: http://heartbleed.com/
.. _OpenSSL Software Foundation: https://www.openssl.org/support/index.html
.. _Drupal's security team: https://www.drupal.org/security-team
.. _two-factor authentication: http://lifehacker.com/5938565/heres-everywhere-you-should-enable-two-factor-authentication-right-now
.. _UK's Government Service Design Manual: https://www.gov.uk/service-manual/
.. _Security as enabler\: Using technological change to build secure services: https://www.gov.uk/service-manual/technology/security-as-enabler.html
.. _Darren Mothersele: http://darrenmothersele.com/blog/2014/02/20/drupal-security/
.. _`IBM suggestes`: http://www-03.ibm.com/industries/ca/en/healthcare/documents/IDC_Canada_Determining_How_Much_to_spend_on_Security_-_Canadian_Perspective_2015.pdf
