# Define decorators that can be used for pytest tests

from __future__ import absolute_import, division, print_function

import os
import zlib
import tempfile
from contextlib import contextmanager
from distutils.version import LooseVersion

import pytest


def make_skipper(module, label=None, version=None):
    label = label or module
    try:
        mod = __import__(module)
        if version:
            assert LooseVersion(mod.__version__) >= LooseVersion(version)
        installed = True
    except (ImportError, AssertionError):
        installed = False
    return installed, pytest.mark.skipif(str(not installed), reason='Requires %s' % label)


ASTROPY_INSTALLED, requires_astropy = make_skipper('astropy',
                                                   label='Astropy')

ASTROPY_GE_03_INSTALLED, requires_astropy_ge_03 = make_skipper('astropy',
                                                               label='Astropy >= 0.3',
                                                               version='0.3')

ASTROPY_GE_04_INSTALLED, requires_astropy_ge_04 = make_skipper('astropy',
                                                               label='Astropy >= 0.4',
                                                               version='0.4')

ASTRODENDRO_INSTALLED, requires_astrodendro = make_skipper('astrodendro')

SCIPY_INSTALLED, requires_scipy = make_skipper('scipy',
                                               label='SciPy')

PIL_INSTALLED, requires_pil = make_skipper('pil', label='PIL')

SKIMAGE_INSTALLED, requires_skimage = make_skipper('skimage',
                                                   label='scikit-image')

XLRD_INSTALLED, requires_xlrd = make_skipper('xlrd')

PLOTLY_INSTALLED, requires_plotly = make_skipper('plotly')

IPYTHON_GE_012_INSTALLED, requires_ipython_ge_012 = make_skipper('IPython',
                                                                 label='IPython >= 0.12',
                                                                 version='0.12')


requires_pil_or_skimage = pytest.mark.skipif(str(not SKIMAGE_INSTALLED and not PIL_INSTALLED),
                                             reason='Requires PIL or scikit-image')

GINGA_INSTALLED, requires_ginga = make_skipper('ginga')

H5PY_INSTALLED, requires_h5py = make_skipper('h5py')

PYQT4_INSTALLED, requires_pyqt4 = make_skipper('PyQt4')
PYQT5_INSTALLED, requires_pyqt5 = make_skipper('PyQt5')
PYSIDE_INSTALLED, requires_pyside = make_skipper('PySide')

QT_INSTALLED = PYQT4_INSTALLED or PYQT5_INSTALLED or PYSIDE_INSTALLED

requires_qt = pytest.mark.skipif(str(not QT_INSTALLED),
                                 reason='An installation of Qt is required')


@contextmanager
def make_file(contents, suffix, decompress=False):
    """Context manager to write data to a temporary file,
    and delete on exit

    :param contents: Data to write. string
    :param suffix: File suffix. string
    """
    if decompress:
        contents = zlib.decompress(contents)

    try:
        _, fname = tempfile.mkstemp(suffix=suffix)
        with open(fname, 'wb') as outfile:
            outfile.write(contents)
        yield fname
    finally:
        try:
            os.unlink(fname)
        except WindowsError:  # on Windows the unlink can fail
            pass