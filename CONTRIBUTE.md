# How to Contribute

* Create a fork of the repository on GitHub
* Make your changes
* Create a pull request on GitHub against the main project

## Anatomy of a Successful Patch

A patch with any chance of being accepted must contain, at a minimum:

* A GitHub Issue describing the bug or feature being addressed
* Unit tests covering all paths through the code
    * Test coverage is currently at 100%. Keep it that way
    * Tests must pass!
    * If creating a totally new feature, create a new test file in the `tests`
      directory, using `py.test`-style tests
* No new violations reported by `pylint` or `pep8`
    * The current `pylint` score (using our `.pylintrc` config) is 10.0/10. Keep
      it that way
    * Run `pylint --rcfile=.pylintrc sandman` from the project root and verify
    * If you need to insert a `pyling` `pragma` to disable an erronous check,
      explain why in the pull request
* Properly documented modules, classes, methods, and attributes
    * Documentation coverage is currently at 100%. Keep it that way
    * Documentation should be Sphinx-style and in ReStructuredText format
* The author's name in the `CONTRIBUTORS.md` file
* Commits of logical units with appropriate messages

## Additional Resources

* [General GitHub documentation](http://help.github.com/)
* [GitHub pull request documentation](http://help.github.com/send-pull-requests/)
