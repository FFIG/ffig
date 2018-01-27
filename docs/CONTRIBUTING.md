Contributing to FFIG
====================
We are happy to accept contributions that fix a bug or implement a feature corresponding to an open ticket in our issue tracker. These should be thoroughly tested. We'll also accept contributions that add a new language binding template or generator.

If you plan to implement a larger feature, it's a good idea to get in touch to discuss it, and see how it may fit into the wider plans. For the most part, development on FFIG is done in the open, with tickets and milestones for major and minor features.

The information below describes the development workflow for FFIG. Contributors are advised to read it and follow it as closely as possible, since this will make it easier for us to review, test and approve your contribution.

Development Workflow
--------------------

 1. Open a new issue, if one does not already exist for the feature or bug you're working on. If you don't have the necessary permissions to create an issue, please get in touch with one of the FFIG maintainers and we will create a ticket for you.
 2. Clone the Git repository. Contributors with commit access to `FFIG/ffig` can clone the repository directly. Other contributors should first fork the repository on GitHub, then clone their fork.
 3. Create a branch with a name that contains the ticket number, e.g. `n100-fix-foo` to fix a bug logged as ticket #100. The branch name should include some hint as to the content of the branch, and should not rely solely on the ticket number..
 4. Develop your feature or bugfix. Write and execute tests as appropriate (see the section below on testing).
 5. Push the feature branch to GitHub; either directly to a branch in `FFIG/ffig`, or to your fork.
 6. Create a pull request from your branch to the `master` branch of `FFIG/ffig`. Assign one or more reviewers from the FFIG maintainers.
 7. Your branch will now be built and tested automatically by Travis CI (Linux) and AppVeyor (Windows). Failures will be reported in the pull request. The tests must pass before your branch can be merged.
 8. Once the tests pass, and your change has been reviewed by a FFIG maintainer, you will be able to merge the branch into `master` of the `FFIG/ffig` repository.
 9. At this point, you can close the corresponding issue, assuming no further work needs to be done for that feature or bugfix.

Testing
-------
The existing functionality of FFIG can be tested locally by running `./scripts/build.py -t`. New tests can be added to the `tests` directory, and should be enabled by adding a corresponding section to the `CMakeLists.txt` file.

The pull request and branch builds on Travis CI and AppVeyor run these tests inside a Docker container. They also check that Python files correspond to the PEP8 guidelines, using the `pep8` checker. You can use `autopep8` to ensure everything meets the requirements ahead of pushing your branch. This has been set up so that you can run `scripts/codechecks.py --reformat` to automatically apply any required changes.
