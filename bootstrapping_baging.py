from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=500, n_features=10, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

bagging_model1 = BaggingClassifier(estimator=RandomForestClassifier(), n_estimators=10, random_state=42)
bagging_model2 = BaggingClassifier(estimator=LogisticRegression(), n_estimators=10, random_state=42)

bagging_model1.fit(X_train, y_train)
bagging_model2.fit(X_train, y_train)

y_pred1 = bagging_model1.predict(X_test)
y_pred2 = bagging_model2.predict(X_test)

accuracy1 = accuracy_score(y_test, y_pred1)
accuracy2 = accuracy_score(y_test, y_pred2)
print(f"Bagging RandomForestClassifier Accuracy: {accuracy1:.2f}")
print(f"Bagging LogisticRegressionClassifier Accuracy: {accuracy2:.2f}")