#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df1 = pd.read_csv("student-scores.csv")
df = df1.copy()
df.head()


# In[2]:


df.drop(columns=['id','first_name','last_name','email'],axis=1, inplace=True)


# In[3]:


df["total_score"] = df["math_score"] + df["history_score"] + df["physics_score"] + df["chemistry_score"] + df["biology_score"] + df["english_score"] + df["geography_score"]
df["average_score"] = df["total_score"] / 7
df.head()


# In[4]:


df['career_aspiration'].value_counts()


# In[5]:


df['career_aspiration'].unique()


# In[6]:


len(df['career_aspiration'].unique())


# In[7]:


df


# In[8]:


# from sklearn.preprocessing import LabelEncoder

# # Create a LabelEncoder object
# label_encoder = LabelEncoder()

# # Encode categorical columns using label encoder
# df['gender'] = label_encoder.fit_transform(df['gender'])
# df['part_time_job'] = label_encoder.fit_transform(df['part_time_job'])
# df['extracurricular_activities'] = label_encoder.fit_transform(df['extracurricular_activities'])
# df['career_aspiration'] = label_encoder.fit_transform(df['career_aspiration'])
# Define mapping dictionaries for categorical features
gender_map = {'male': 0, 'female': 1}
part_time_job_map = {False: 0, True: 1}
extracurricular_activities_map = {False: 0, True: 1}
career_aspiration_map = {
        'Lawyer': 0, 'Doctor': 1, 'Government Officer': 2, 'Artist': 3, 'Unknown': 4,
        'Software Engineer': 5, 'Teacher': 6, 'Business Owner': 7, 'Scientist': 8,
        'Banker': 9, 'Writer': 10, 'Accountant': 11, 'Designer': 12,
        'Construction Engineer': 13, 'Game Developer': 14, 'Stock Investor': 15,
        'Real Estate Developer': 16
    }
# Apply mapping to the DataFrame
df['gender'] = df['gender'].map(gender_map)
df['part_time_job'] = df['part_time_job'].map(part_time_job_map)
df['extracurricular_activities'] = df['extracurricular_activities'].map(extracurricular_activities_map)
df['career_aspiration'] = df['career_aspiration'].map(career_aspiration_map)


# In[9]:


df


# In[10]:


df.shape


# In[11]:


df['career_aspiration'].value_counts()


# In[12]:


from imblearn.over_sampling import SMOTE

# Create SMOTE object
smote = SMOTE(random_state=42)

# Separate features and target variable
X = df.drop('career_aspiration', axis=1)
y = df['career_aspiration']

# Apply SMOTE to the data
X_resampled, y_resampled = smote.fit_resample(X, y)


# In[13]:


y_resampled.value_counts()


# In[14]:


y_resampled.shape


# In[15]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_resampled,y_resampled,test_size=0.2, random_state=42)


# In[16]:


X_train.shape,y_train.shape, X_test.shape, y_test.shape


# In[17]:


X_train


# In[18]:


from sklearn.preprocessing import StandardScaler

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler to the training data and transform both training and testing data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# In[19]:


X_train_scaled


# In[20]:


from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# Define models
models = {
    "Logistic Regression": LogisticRegression(),
    "Support Vector Classifier": SVC(),
    "Random Forest Classifier": RandomForestClassifier(),
    "K Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree Classifier": DecisionTreeClassifier(),
    "Gaussian Naive Bayes": GaussianNB(),
    "AdaBoost Classifier": AdaBoostClassifier(),
    "Gradient Boosting Classifier": GradientBoostingClassifier(),
    "XGBoost Classifier": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
}

# Train and evaluate each model
for name, model in models.items():
    print("="*50)
    print("Model:", name)
    # Train the model
    model.fit(X_train_scaled, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Print metrics
    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_rep)
    print("Confusion Matrix:\n", conf_matrix)


# In[21]:


model = RandomForestClassifier()

model.fit(X_train_scaled, y_train)
# Predict on test set
y_pred = model.predict(X_test_scaled)

# Calculate metrics
print("Accuracy: ",accuracy_score(y_test, y_pred))
print("Report: ",classification_report(y_test, y_pred))
print("Confusion Matrix: ",confusion_matrix(y_test, y_pred))


# In[22]:


X_test_scaled[10]


# In[23]:


X_test_scaled[10].reshape(1,-1)


# In[24]:


model.predict(X_test_scaled[10].reshape(1,-1))


# In[25]:


print("Pridicated Label:", model.predict(X_test_scaled[10].reshape(1,-1)))
print("Actual:", y_test.iloc[10])


# In[26]:


print("Pridicated Label:", model.predict(X_test_scaled[45].reshape(1,-1)))
print("Actual:", y_test.iloc[45])


# In[27]:


print("Pridicated Label:", model.predict(X_test_scaled[4].reshape(1,-1)))
print("Actual:", y_test.iloc[4])


# In[28]:


print("Pridicated Label:", model.predict(X_test_scaled[98].reshape(1,-1)))
print("Actual:", y_test.iloc[98])


# In[29]:


# test 1
print("Actual Label :", y_test.iloc[10])
print("Model Prediction :",model.predict(X_test_scaled[10].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")


# In[30]:


# test 2
print("Actual Label :", y_test.iloc[300])
print("Model Prediction :",model.predict(X_test_scaled[300].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")


# In[31]:


# test 3
print("Actual Label :", y_test.iloc[23])
print("Model Prediction :",model.predict(X_test_scaled[23].reshape(1,-1))[0])
if y_test.iloc[10]==model.predict(X_test_scaled[10].reshape(1,-1)):
    print("Wow! Model doing well.....")
else:
    print("not sure......")


# In[32]:


import pickle

# SAVE FILES
pickle.dump(scaler,open("Models/scaler.pkl",'wb'))
pickle.dump(model,open("Models/model.pkl",'wb'))


# In[33]:


# Load the scaler, label encoder, and model
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))


# In[34]:


import pickle
import numpy as np

# Load the scaler, label encoder, model, and class names
scaler = pickle.load(open("Models/scaler.pkl", 'rb'))
model = pickle.load(open("Models/model.pkl", 'rb'))
class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']

def Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score,average_score):
    
    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0
    
    # Create feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, absence_days, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score,total_score,average_score]])
    
    # Scale features
    scaled_features = scaler.transform(feature_array)
    
    # Predict using the model
    probabilities = model.predict_proba(scaled_features)
    
    # Get top five predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:5]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]
    
    return top_classes_names_probs


# In[35]:


# Example usage 1
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=7,
                                        math_score=65,
                                        history_score=60,
                                        physics_score=97,
                                        chemistry_score=94,
                                        biology_score=71,
                                        english_score=81,
                                        geography_score=66,
                                        total_score=534,
                                        average_score=76.285714)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")


# In[36]:


# Example usage 2
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=4,
                                        math_score=87,
                                        history_score=73,
                                        physics_score=98,
                                        chemistry_score=91,
                                        biology_score=79,
                                        english_score=60,
                                        geography_score=77,
                                        total_score=583,
                                        average_score=83.285714)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")


# In[38]:


# Example usage 3
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=5,
                                        math_score=88,
                                        history_score=63,
                                        physics_score=88,
                                        chemistry_score=95,
                                        biology_score=80,
                                        english_score=80,
                                        geography_score=70,
                                        total_score=564,
                                        average_score=80.571428)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")


# In[39]:


# Example usage 4
final_recommendations = Recommendations(gender='female',
                                        part_time_job=False,
                                        absence_days=2,
                                        extracurricular_activities=False,
                                        weekly_self_study_hours=6,
                                        math_score=90,
                                        history_score=89,
                                        physics_score=98,
                                        chemistry_score=53,
                                        biology_score=60,
                                        english_score=22,
                                        geography_score=70,
                                        total_score=583,
                                        average_score=68.857142)

print("Top recommended studies with probabilities:")
print("="*50)
for class_name, probability in final_recommendations:
    print(f"{class_name} with probability {probability}")


# In[37]:


# sklear version in pychar production 
import sklearn
print(sklearn.__version__)
# in pycharm env install
# pip install scikit-learn==1.0.2


# In[ ]:




