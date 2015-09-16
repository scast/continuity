===============================
Continuity
===============================

.. image:: https://img.shields.io/travis/scast/continuity.svg
        :target: https://travis-ci.org/scast/continuity

.. image:: https://img.shields.io/pypi/v/continuity.svg
        :target: https://pypi.python.org/pypi/continuity


Continuity is a library to help doing continuous integration (CI) on
your codebase and continuous deployment (CD) of your deliverables
using Fabric. It proposes our philosophy that at any given moment,
`master` is a candidate release of your product. As such, it should be
building, passing tests and deployable at any moment.

* Free software: BSD license
* Documentation: https://continuity.readthedocs.org.

Features
--------

* Follows a `git-flow`-esque model of development philosophy.
* Easy to integrate with Jenkins.
* No assumptions made on your deploy model.
* Tools to simplify doing Docker based deploys and testing.

Philosophy
----------

We propose a `git flow` like model where development happens on
different branches. You can call your branches whatever you feel like,
but we like the following names:

- `master` for the current revision that is working as problem-free as
  possible.

- `development` where the development happens.

- `production` the current branch that production is tracking.

Like Git flow, developers make feature branches off `development` and
eventually merge them back there, when they are deemed to be ready to
ship. However, unlike `git flow` in which you eventually merge
`development` manually back into `production`, we add the `master`
release branch as intermediate step to ensure that the codebase is
*problem-free*.

We define *problem-free* as passing all tests. Of course, you can
define this as whatever suits you better, like passing code reviews,
or anything you feel like. Our philosophy proposes the following
invariant that is always held true:

"At any given moment, `master` is a candidate release of your product."

To ensure this, manually merging onto or changing `master` is
forbidden. Instead, making changes on `master` is done automatically
by your CI system (i.e. Jenkins) when `development` is considered to
be **problem-free**.

Deployment
----------

We make no assumptions about your deploy process, beyond that you use
Fabric to deploy your artifacts.

Pipeline
---------

Our generic pipeline is as follows:

1. **Build new artifacts, if necessary.** Checks into the new pushed
   files are performed to detect whether or not to trigger a build. If
   a build is necessary, it is performed and used in the following steps.

2. **Detect if changes are problem-free.** Depending on the results of
   this step, move to step 3, or stop the pipeline and don't merge the
   changes onto `master`. Trigger notifications to developers if
   enabled.

3. **Push changes.** Merge `development` into `master` (these changes
   are *problem-free*) and push to the `origin`.

4. **Deploy**. Deploy changes to all the environment you want. By
   default, we suggest automatically pushing into staging/development
   and manually pushing to production when desired.


Questions and Answers
----------------------

1. What about hotfixes?

   Like Git flow, just create your hotfix branch and when you fix the
   issue, merge back to `development` (to ensure the fix lives there)
   and `production` (to ensure your users see the fixed version). The
   next time `development` is pushed and determined to be
   *problem-free*, it will be merged against `master`. If it isn't
   problem-free, you shouldn't be merging it, right?

2. What about integrating and delivering feature branches or other
   development lines?

   Using fabric environments you can easily bootstrap continuity to
   continuously integrate and deliver different branches.

3. What do I need?

   You need a well defined `deploy` task and a definition of
   *problem-free*. Everything else is mostly configuration and pretty
   optional.
