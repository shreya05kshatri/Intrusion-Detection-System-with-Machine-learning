import time
import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Dataset location
train_url = "KDDTrain+.txt"

# Full column names
full_columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
    'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
    'label', 'difficulty'
]

# Selected features + label
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'count', 'target'
]

# Load and preprocess data
print("📥 Loading dataset...")
df = pd.read_csv(train_url, names=full_columns)
df.rename(columns={'label': 'target'}, inplace=True)
df.drop(columns=['difficulty'], inplace=True)

df = df[columns]
print(f"✅ Dataset shape: {df.shape}")

# Encode categorical variables
label_encoders = {}
for col in ['protocol_type', 'service', 'flag']:
    df[col] = df[col].astype(str).str.strip()
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Convert labels to binary
df['target'] = df['target'].apply(lambda x: 0 if x.strip() == 'normal' else 1)

# Split features and labels
X = df.drop('target', axis=1)
y = df['target']

# Remove rows with NaN
X = X.apply(pd.to_numeric, errors='coerce')
X.dropna(inplace=True)
y = y.loc[X.index]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🚀 Training model...")
start_time = time.time()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
end_time = time.time()
print(f"✅ Model trained in {end_time - start_time:.2f} seconds.")

# Evaluate
print("\n Evaluation Report:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "random_forest_ids_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
print("💾 Model and encoders saved successfully.")
