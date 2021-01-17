import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import ensemble
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
# warnings.filterwarnings('ignore')

def trainAndTestModel(model_name, model, X_train, y_train, X_test, y_test, verbose = True):
  model.fit(X_train, y_train)        
  if verbose:
    try:
        print(f"{model_name}: Score (roc_auc) = {model.score(X_train, y_train)}, Best Parameters= {model.best_params_}")
    except:
        print(f"{model_name}: Score (roc_auc) = {model.score(X_train, y_train)}") 
    print(f"{model_name}: Test Score (roc_auc) = {model.score(X_test,y_test)} ")   
    print(classification_report(y_true=y_test,y_pred=model.predict(X_test))) 
    plot_confusion_matrix(model, X_test, y_test) 
    plt.show() 
  return model
      
class Classifier:
    def __init__(self, dataframe, featureNames, labelName, seed = 7, cross_fold = 5, scoring = 'roc_auc'):
      self.seed = seed
      self.cross_fold = cross_fold
      self.scoring = scoring              
      dfx = dataframe[featureNames]
      dfy = dataframe[[labelName]]
      x_features = dfx.values
      y_labels = dfy.values
      x_train, x_test, y_train, y_test = train_test_split(x_features, y_labels, test_size=0.33, random_state=seed, stratify=y_labels)
      self.x_train = x_train
      self.x_test = x_test
      self.y_train = y_train
      self.y_test = y_test
    
    def printFeatureRankings(self):
      # Build a forest and compute the feature importances
      forest = ensemble.RandomForestClassifier(n_estimators= 24,random_state=self.seed)
      forest.fit(self.x_train, np.ravel(self.y_train))
      importances = forest.feature_importances_
      std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
      indices = np.argsort(importances)[::-1]
      print("Feature rankings:")
      for f in range(self.x_train.shape[1]):
          print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
      
      # Plot the feature importances of the forest
      plt.figure()
      plt.title("Feature importances")
      plt.bar(range(self.x_train.shape[1]), importances[indices], color="r", yerr=std[indices], align="center")
      plt.xticks(range(self.x_train.shape[1]), indices)
      plt.xlim([-1, self.x_train.shape[1]])
      plt.show()
      print("Indices of features  :",indices)

    def makeModel(self, model_name = "AdaBoostClassifier"):
      print("Training",model_name)
      if model_name == "ExtraTreesClassifier":
        param_grid  = {'n_estimators': [2,4,8,16,32,64,128,256,400], 'criterion':["gini", "entropy"], 'random_state': [42]}
        grid_er1 = GridSearchCV(estimator=ensemble.ExtraTreesClassifier(),param_grid =param_grid ,cv=self.cross_fold, scoring=self.scoring, n_jobs= -1)
        model = trainAndTestModel(f"{model_name}", grid_er1, self.x_train, self.y_train, self.x_test, self.y_test)
      elif model_name == "RandomForestClassifier":
        param_grid  = {'n_estimators': [2,4,8,16,32,64,128,256,400], 'criterion':["gini", "entropy"], 'random_state': [42]}
        grid_er1 = GridSearchCV(estimator=ensemble.RandomForestClassifier(),param_grid =param_grid ,cv=self.cross_fold, scoring=self.scoring, n_jobs= -1)
        model = trainAndTestModel(f"{model_name}", grid_er1, self.x_train, self.y_train, self.x_test, self.y_test)
      elif model_name == "GradientBoostingClassifier":
        param_grid  = {'n_estimators': [2,4,8,16,32,64,128,256,400],  'learning_rate':[0.001,0.01,0.1,1,1.5,2] , 'criterion':['friedman_mse', 'mse', 'mae'], 'random_state': [42]}
        grid_er1 = GridSearchCV(estimator=ensemble.GradientBoostingClassifier(),param_grid =param_grid ,cv=self.cross_fold, scoring=self.scoring, n_jobs= -1)
        model = trainAndTestModel(f"{model_name}", grid_er1, self.x_train, self.y_train, self.x_test, self.y_test)
      elif model_name == "AdaBoostClassifier":
        param_grid  = {'n_estimators': [2,4,8,16,32,64,128,256,400], 'learning_rate':[0.001,0.01,0.1,0.2] ,  'random_state': [42]}
        grid_er1 = GridSearchCV(estimator=ensemble.AdaBoostClassifier(),param_grid =param_grid ,cv=self.cross_fold, scoring=self.scoring, n_jobs= -1)
        model = trainAndTestModel(f"{model_name}", grid_er1, self.x_train, self.y_train, self.x_test, self.y_test)
      elif model_name == "BaggingClassifier":
        param_grid  = {'n_estimators': [2,4,8,16,32,64,128,256,400], 'random_state': [42]}
        grid_er1 = GridSearchCV(estimator=ensemble.BaggingClassifier(),param_grid =param_grid ,cv=self.cross_fold, scoring=self.scoring, n_jobs= -1)
        model = trainAndTestModel(f"{model_name}", grid_er1, self.x_train, self.y_train, self.x_test, self.y_test)
      else:
        raise Exception("Unknown model name: "+model_name)
      return model



















