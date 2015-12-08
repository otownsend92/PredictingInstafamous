#import scipy
from scipy.stats import spearmanr

x = [5.05, 6.75, 3.21, 2.66]
y = [1.65, 26.5, -5.93, 7.96]
z = [1.65, 2.64, 2.64, 6.95]

def cal_correlation(x,y):
	rank_correlation = spearmanr(x, y)[0]
	return rank_correlation


if __name__ == '__main__':
	print cal_correlation(x,y)
