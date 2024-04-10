from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd

data = pd.read_csv('final_data.csv')
#data['created_at'] = pd.to_datetime(data['created_at'])
list = ['account_type', 'id', 'displayname', 'rawDescription', 'location', 'username', 'created_at']

# balancing the data
bots = data[data['account_type'] == 'bot']
not_bot = data[data['account_type'] == 'human'].sample(n = bots.shape[0])
balanced_data = pd.concat([not_bot,bots])

X_train, X_valid, y_train, y_valid = train_test_split(balanced_data.drop(list, axis = 1), balanced_data['account_type'])

model = RandomForestClassifier(n_estimators = 100, max_depth = 50, min_samples_leaf = 5)

model.fit(X_train, y_train)

print(model.score(X_train, y_train))
print(model.score(X_valid, y_valid))