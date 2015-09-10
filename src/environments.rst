J) Development, Staging and Production
======================================

Any formalized development process should have three distinct server
environments. The development environment can simply be a developer's computer
(or perhaps several developers' computers). The staging and production servers
should be essentially identical. The role of the staging server is to document
and test the migration process to verify that the code and configuration can
move onto the production server. For more information refer to OpenConcept's
blog post on the `path of code vs content`_. The code for your Drupal site should
be stored in a central repository. The Drupal community has generally adopted

`Git`_, but there are other valid options for version control. A developer will
pull/push/clone/branch to/from that repository. New code is committed and pushed
from the development environment into the central repository, and can then be
pulled onto the staging environment. If it passes testing there, it can then be
pulled into production. The database on the staging server can simply be cloned
from the production server using Drush. Assuming that the new code works well
with the production database, you can be reasonably certain that you will be
able to migrate that code and configuration to the production site.  This is
definitely more complicated, but both the staging and production environments
will need to be accessible via Drush and the Git repository.

You will need to set up an SSH user with its own SSH keys to allow you to use
Drush aliases to transfer databases between staging and production. You may also
want to have another account to be able to transfer uploaded files which
probably would not be managed under version control. Using an external site like
`GitHub`_ for storing your repository provides access to some great additional
tools like `Travis`_ and

`SauceLabs`_ which can help you deliver a more reliable site. You can also set
it up on your staging or development server. Limit access between servers.
There is a potential risk from having a semi-porous boundary between these
environments, but the risks are far outweighed by the benefits. Having a central
Git repository gives you control across all environments at one time.  Being
able to diff any change allows you to quickly identify where changes have been
made and know why. Drush is certainly powerful, but only experienced users
should have access to it. With a solid backup plan, even if this is compromised,
it can be quickly restored.

.. _path of code vs content: http://openconcept.ca/blog/mgifford/flow-content-code
.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/
.. _Travis: http://docs.travis-ci.com/user/getting-started/
.. _SauceLabs: https://saucelabs.com/builder
