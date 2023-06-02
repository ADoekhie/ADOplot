import scipy
from scipy import stats


class Stats:

    @staticmethod
    def t_test(data, pm):
        result = scipy.stats.ttest_1samp(
            a=data,
            popmean=pm,
            nan_policy='raise')
        return result
