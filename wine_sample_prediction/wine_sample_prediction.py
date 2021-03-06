# -*- coding: utf-8 -*-
"""
Wine_sample_prediction.ipynb

# **Using different ML Classifiers to Predict Quality of Wine Sample**

##Classifiers Used

*   Random Forest Classifier
*   Support Vector Classifier
*   Stochastic Gradient Descent Classifier

##Model Verification
*   Accuracy
*   F1 Score

# Skills
* ### Statistical Analysis
* ### Unsupervised Learning
* ### Predictive Analysis

* ### Programming
*   **Language :**   Python
*   **Libraries:** 
   * Scikit-learn
   * matplotlib
   * seaborn
   * pandas
   * numpy
"""

# import libraries

import numpy as np
import pandas as pd

# Data Processing
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

# Classifiers
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier

# Metrics
from sklearn.metrics import confusion_matrix, classification_report

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# Loading Data

wine_data = pd.read_csv('/content/winequality-red.csv')
wine_data.head(10)

#Information about the data columns
wine_data.info()

"""*Target: To predict the quality of wine*

**Target column: quality**

Let's view how each column varies with the target column i.e quality
"""

# Separating Train and Test Data
wine_train, wine_test = train_test_split(wine_data, test_size = 0.2, random_state = 42)


wine_train_x = wine_train.iloc[:,:-1]         #Droping the target column i.e 'Quality' from Train
wine_train_y = wine_train.iloc[:,11]          #Only the target column

wine_test_x = wine_test.iloc[:,:-1]           #Droping the target column i.e 'Quality' from Test
wine_test_y = wine_test.iloc[:,11]            #Only the target column

wine_train_x.head(5)

wine_train.columns

"""# Exploratory Data Analysis on Train Data"""

fig = plt.figure(figsize = (12,6))
plt.subplot(3, 1,1)
sns.barplot(x = 'quality', y = 'fixed acidity', data = wine_train)
plt.subplot(3, 1,2)
sns.barplot(x = 'quality', y = 'volatile acidity', data = wine_train)
plt.subplot(3, 1,3)
sns.barplot(x = 'quality', y = 'citric acid', data = wine_train)

fig1 = plt.figure(figsize = (12,16))
plt.subplot(4,1,1)
sns.boxplot(x = 'quality', y = 'alcohol',data = wine_train)

plt.subplot(4,1,2)
sns.boxplot(x = 'quality', y = 'volatile acidity',data = wine_train)

plt.subplot(4,1,3)
sns.boxplot(x = 'quality', y = 'citric acid',data = wine_train)

plt.subplot(4,1,4)
sns.boxplot(x = 'quality', y = 'residual sugar',data = wine_train)

fig2 = plt.figure(figsize = (12,16))
plt.subplot(4,1,1)
sns.boxplot(x = 'quality', y = 'chlorides',data = wine_train)

plt.subplot(4,1,2)
sns.boxplot(x = 'quality', y =  'free sulfur dioxide',data = wine_train)

plt.subplot(4,1,3)
sns.boxplot(x = 'quality', y = 'total sulfur dioxide',data = wine_train)

plt.subplot(4,1,4)
sns.boxplot(x = 'quality', y = 'density',data = wine_train)

fig3 = plt.figure(figsize = (12,16))
plt.subplot(3,1,1)
sns.boxplot(x = 'quality', y = 'pH',data = wine_train)

plt.subplot(3,1,2)
sns.boxplot(x = 'quality', y =  'sulphates',data = wine_train)

plt.subplot(3,1,3)
sns.boxplot(x = 'quality', y = 'alcohol',data = wine_train)

# Computiing Correlation
corr = wine_train.corr()
corr.loc['quality',:]

"""At a first glance the above Correlation between 'Quality' and other columns shows that
*residual sugar, chlorides, free sulphur dioxide and pH* 
have very less influence on target column *Quality*

Let's draw a colour heatmap
"""

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

"""Here we find that 
* **Residual sugar** shows minimum influence on Quality yet it has strongest *positive* influence on density. This is evident as a higher dense solution will have high *residual sugar*. So, *density* can explain effect of *residual sugar* on the *quality*. Therefore, *Residual Sugar* can safely be removed from predictive analysis as it won't add any information to the analysis.

* **Chlorides** shows very low *negative* influence on Target yet it needs to be kept iin analysis as it has consistent effect on all other columns. Therefore *Chlorides* is an integral part of the analysis.

* **Free Sulphur Dioxide** shows *positive* influence on *Total Sulphur Dioxide*. This is evident as higher Total Sulphur Dioxide will always increase Free Sulphur Dioxide. Therefore, *Free Sulphur Dioxide* can safely be removed from predictive analysis as it won't add any information to the analysis.

* **pH** is a metric of acidity of the solution. It's not independent and cannot be varied on it's own without changing other independent variables. Therefore,*pH* won't add any information to the analysis.


"""

'''
# Removing Residual Sugar, Free Sulphur Dioxide and pH from Train data.
try:
  wine_train_x = wine_train_x.drop(['residual sugar', 'free sulfur dioxide', 'pH'], axis = 1)
  
  
except KeyError:
  wine_test_x = wine_test_x.drop(['residual sugar', 'free sulfur dioxide', 'pH'], axis = 1)
'''
wine_train_x

"""## Data PreProcessing"""

# Checking Data Quality
wine_train_x.describe()

# Finding if any NA or NULL value is present or not
# wine_train_x_na = wine_train_x.notna()
for column in wine_train_x.columns:
  if wine_train_x[column].isnull().sum() > 0:
    print("Null Found in Column: ", column)
  else:
    print("NO Null Found in Column: ", column)

# Result: No null value

# Since it's a classification type,
# Normalizing data in each column
normal = StandardScaler()
normal.fit_transform(wine_train_x)

"""# Predictive Analysis

Random Forest Classifier
"""

rfc = RandomForestClassifier()

# With Default hyperparameters
rfc.fit( wine_train_x, wine_train_y)
wine_pred_y = rfc.predict(wine_test_x)

# Prediction Score
wine_test_y_array = np.asarray(wine_test_y)
rfc_report = classification_report(wine_test_y_array,wine_pred_y)
print(rfc_report)

print(confusion_matrix(wine_test_y_array,wine_pred_y, labels = [3,4,5,6,7,8]))

