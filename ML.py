# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset
final_visualization_data = pd.read_csv("final_visualization_data.csv")

final_visualization_data['Exam Period'] = final_visualization_data['Exam Count'].apply(lambda x: 1 if x > 0 else 0)

search_count_median = final_visualization_data['Search Count'].median()
final_visualization_data['High Search Count'] = final_visualization_data['Search Count'].apply(
    lambda x: 1 if x > search_count_median else 0
)

# Define features (X) and target (y)
X = final_visualization_data[['Exam Period']]
y = final_visualization_data['High Search Count']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Logistic Regression model
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Make predictions
y_pred = log_reg.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print results
print("Accuracy:", accuracy)
print("\nConfusion Matrix:\n", conf_matrix)
print("\nClassification Report:\n", class_report)
