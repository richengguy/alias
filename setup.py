# Used to trigger an import error when not building the package correctly.
# See https://scikit-hep.org/developer/packaging#git-tags-official-pypa-method

import setuptools_scm  # noqa: F401
import toml  # noqa: F401

import setuptools
setuptools.setup()
