from sklearn.metrics import classification_report

y_true = [1,0,1,1]
y_pred = [1,0,0,1]

print(classification_report(y_true,y_pred))