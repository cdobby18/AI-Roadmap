p_disease = 0.01
p_positive_given_disease = 0.95
p_positive = 0.05

p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print(p_disease_given_positive)