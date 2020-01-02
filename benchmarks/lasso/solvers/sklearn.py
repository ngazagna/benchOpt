import warnings
from benchopt.base import BaseSolver
from benchopt.util import safe_import


with safe_import() as solver_import:
    from sklearn.linear_model import Lasso
    from sklearn.exceptions import ConvergenceWarning


class Solver(BaseSolver):
    name = 'sklearn'

    install_cmd = 'pip'
    package_name = 'scikit-learn'
    package_import = 'sklearn'

    def set_loss(self, loss_parameters):
        self.X, self.y, self.lmbd = loss_parameters

        n_samples = self.X.shape[0]
        self.clf = Lasso(alpha=self.lmbd/n_samples, fit_intercept=False, tol=0)
        warnings.filterwarnings('ignore', category=ConvergenceWarning)

    def run(self, n_iter):
        self.clf.max_iter = n_iter
        self.clf.fit(self.X, self.y)

    def get_result(self):
        return self.clf.coef_.flatten()
