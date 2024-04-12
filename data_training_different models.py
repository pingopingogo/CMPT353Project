import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB



data = pd.read_csv('final_data.csv', index_col = 'id')

# Balancing the data
bots = data[data['account_type'] == 'bot']
not_bot = data[data['account_type'] == 'human'].sample(n=bots.shape[0])
balanced_data = pd.concat([not_bot, bots])

# Splitting the data into features and target
X = balanced_data.drop('account_type', axis=1)
y = balanced_data['account_type']

# Splitting the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)


#Scale the Numeric Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_valid_scaled = scaler.transform(X_valid)


#Train and Evaluate multiple models
# Initialize the models
models = {
    'RF1': RandomForestClassifier(n_estimators=200, min_samples_leaf=10),
    'RF2': RandomForestClassifier(n_estimators=200, max_depth=100, min_samples_leaf=2),
    'RF3': RandomForestClassifier(n_estimators=50, max_depth=25, min_samples_leaf=20),
    'GBC': GradientBoostingClassifier(n_estimators = 200, min_samples_leaf = 10),
    'MLP': MLPClassifier(solver = 'lbfgs', activation = 'logistic', max_iter = 10000, random_state=42),
    'Reg': LogisticRegression(max_iter=1000),
    'SVM': SVC(random_state=42),
    'KNN1': KNeighborsClassifier(n_neighbors=5),
    'KNN2': KNeighborsClassifier(n_neighbors=10),
    'KNN3': KNeighborsClassifier(n_neighbors=3),
    'NB': GaussianNB()
}

# Dictionary to store the accuracy of each model
accuracy_scores = {}

# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_valid_scaled)
    accuracy_scores[name] = accuracy_score(y_valid, y_pred)

# Print the accuracy scores
for name, score in accuracy_scores.items():
    print(f'{name}: {score}')

# Create a bar chart to compare the accuracy of each model
plt.figure(0)
plt.bar(accuracy_scores.keys(), accuracy_scores.values())
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Comparison of Classifier Models')

plt.savefig('model_comparison_chart.png')


# Data fitted to PCA analysis 
# Dictionary to store the accuracy of each model (pca)
accuracy_scores_pca = {}

# Train and evaluate each model (pca)
for name, model in models.items():
    ml_model = make_pipeline(
        PCA(10),
        model
    )
    ml_model.fit(X_train_scaled, y_train)
    y_pred = ml_model.predict(X_valid_scaled)
    accuracy_scores_pca[name] = accuracy_score(y_valid, y_pred)

# Print the accuracy scores (pca)
for name, score in accuracy_scores_pca.items():
    print(f'{name}: {score}')

# Create a bar chart to compare the accuracy of each model
plt.figure(1)
plt.bar(accuracy_scores_pca.keys(), accuracy_scores_pca.values())
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Comparison of Classifier Models with PCA(10)')

plt.savefig('model_comparison_chart_pca.png')
