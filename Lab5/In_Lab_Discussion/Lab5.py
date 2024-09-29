import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator

data = pd.read_csv("1.txt", delimiter="\t")  # Adjust delimiter if needed
print(data)

model = BayesianNetwork([
    ('EC100', 'EC160'), 
    ('IT101', 'IT161'), 
    ('MA101', 'PH100'), 
    ('PH100', 'PH160'), 
    ('MA101', 'HS101'), 
    ('IT101', 'HS101')
])

model.fit(data, estimator=MaximumLikelihoodEstimator)

for cpd in model.get_cpds():
    print(f"CPD of {cpd.variable}:\n{cpd}")
    
from pgmpy.inference import VariableElimination

inference = VariableElimination(model)

query_result = inference.map_query(['PH100'], evidence={'EC100': 'DD', 'IT101': 'CC', 'MA101': 'CD'})
print("Predicted grade for PH100:", query_result['PH100'])

grade_mapping = {'AA': 0, 'AB': 1, 'BB': 2, 'BC': 3, 'CC': 4, 'CD': 5, 'DD': 6, 'F': 7, 'y': 1, 'n': 0}
data = data.applymap(lambda x: grade_mapping.get(x, x))

features = data.drop(columns=['QP'])  
target = data['QP']
print("Unique values in each column:")
for column in data.columns:
    print(f"{column}: {data[column].unique()}")
# Conduct 20 iterations for accuracy calculation
accuracies = []
print(data.isnull().sum())
for i in range(20):
    X = data.drop(columns=['QP'])
    y = data['QP']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    X_train = X_train.astype(int)
    X_test = X_test.astype(int)

    model_nb = CategoricalNB(min_categories=8)
    model_nb.fit(X_train, y_train)

    try:
        y_pred = model_nb.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracies.append(accuracy)
    except IndexError as e:
        print(f"IndexError encountered: {e}")
        print("Test Data:\n", X_test.head())
        accuracy = accuracy_score(y_test, y_pred)
        print(accuracy)

average_accuracy = np.mean(accuracies)
print(f"Average accuracy over 20 runs: {average_accuracy * 100:.2f}%")

accuracies_dependent = []

for i in range(20):
    X = data.drop(columns=['QP'])
    y = data['QP']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    dependent_model = BayesianNetwork([
    ('EC100', 'QP'), 
    ('IT101', 'QP'), 
    ('MA101', 'QP'), 
    ('PH100', 'QP'), 
    ('MA101', 'QP'), 
    ('IT101', 'QP'),
    ('EC160', 'QP'),
    ('IT161', 'QP'),
    ('PH160', 'QP'),
    ('HS101', 'QP')
    
])

    print("yes")
    dependent_model.fit(pd.concat([X_train, y_train], axis=1), estimator=MaximumLikelihoodEstimator)
    X_train = X_train.astype(int)
    X_test = X_test.astype(int)
    print(i)
    dependent_model.fit(pd.concat([X_train, y_train], axis=1), estimator=MaximumLikelihoodEstimator)
    
    inference = VariableElimination(dependent_model)
    y_pred = [inference.map_query(['QP'], evidence=row.to_dict())['QP'] for _, row in X_test.iterrows()]
    
    accuracy = accuracy_score(y_test, y_pred)
    accuracies_dependent.append(accuracy)


average_accuracy_dependent = np.mean(accuracies_dependent)
print(f"Average accuracy over 20 runs (dependent model): {average_accuracy_dependent * 100:.2f}%")