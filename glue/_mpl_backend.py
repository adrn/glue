class MatplotlibBackendSetter(object):
    """
    Import hook to make sure the proper Qt backend is set when importing
    Matplotlib.
    """

    enabled = True

    def find_module(self, mod_name, pth):
        if self.enabled and 'matplotlib' in mod_name:
            self.enabled = False
            set_mpl_backend()
        return


def set_mpl_backend():

    from matplotlib import rcParams, rcdefaults

    # standardize mpl setup
    rcdefaults()

    from glue.external.qt import is_pyqt5
    if is_pyqt5():
        rcParams['backend'] = 'Qt5Agg'
    else:
        rcParams['backend'] = 'Qt4Agg'

    # The following is a workaround for the fact that Matplotlib checks the
    # rcParams at import time, not at run-time. I have opened an issue with
    # Matplotlib here: https://github.com/matplotlib/matplotlib/issues/5513
    from matplotlib import get_backend
    from matplotlib import backends
    backends.backend = get_backend()
