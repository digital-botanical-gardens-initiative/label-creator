# label-creator

[![Release](https://img.shields.io/github/v/release/edouardbruelhart/label-creator)](https://img.shields.io/github/v/release/edouardbruelhart/label-creator)
[![Build status](https://img.shields.io/github/actions/workflow/status/edouardbruelhart/label-creator/main.yml?branch=main)](https://github.com/edouardbruelhart/label-creator/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/edouardbruelhart/label-creator/branch/main/graph/badge.svg)](https://codecov.io/gh/edouardbruelhart/label-creator)
[![Commit activity](https://img.shields.io/github/commit-activity/m/edouardbruelhart/label-creator)](https://img.shields.io/github/commit-activity/m/edouardbruelhart/label-creator)
[![License](https://img.shields.io/github/license/edouardbruelhart/label-creator)](https://img.shields.io/github/license/edouardbruelhart/label-creator)

A tool to generate labels for the DBGI project.

- **Github repository**: <https://github.com/edouardbruelhart/label-creator/>
- **Documentation** <https://edouardbruelhart.github.io/label-creator/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:edouardbruelhart/label-creator.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version



---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
