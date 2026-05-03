from scipy import stats

sample = [20,22,19,24,25]

t_stat, p_value = stats.ttest_1samp(sample, 21)

print("t statistic:",t_stat)
print("p value:",p_value)