import numpy as np
from flask import Flask, request, render_template
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd

app = Flask(__name__)


ridgemodel = pickle.load(open('ridgemodel.pkl','rb'))
lassomodel = pickle.load(open('lassomodel.pkl','rb'))
forestmodel = pickle.load(open('forestmodel.pkl','rb'))
xgbmodel = pickle.load(open('xgbmodel.pkl','rb'))
X_train_original = pd.read_csv('X_train_original.csv')
cat_attribs = ['GPU_Memory_Type', 'OS', 'RAM_DDR']

data_val = pd.read_csv("./train_val_test/test.csv", index_col = 'Unnamed: 0')
data_val.drop(['Year', 'CPU_Default_Clock', 'CPU_Transistor_Size(nm)', 'GPU clock(MHz)',
           'RAM_bus', 'CPU_Cores', 'GPU_Bus_Width(bit)', 'Display_Width(pixel)', 'Brand', 'CPU', 'GPU', 'Laptop_name'],
           axis = 1, inplace = True)
X_val = data_val.drop('Price(USD)', axis = 1)

num_attribs = list(set(X_train_original.columns).difference(set(cat_attribs)))
num_pipeline = Pipeline([
    ('std_scaler', StandardScaler())
])

full_pipeline = ColumnTransformer([
    ('num', num_pipeline, num_attribs),
    ('cat', OneHotEncoder(), cat_attribs)
])
full_pipeline.fit(X_train_original)


ridgemodel = pickle.load(open('ridgemodel.pkl','rb'))
input0 = pd.DataFrame([['Linux', 1, 1, 1, 1, 1, 'GDDR5', 1, 1, 3, 1, 1, 1, 1]], columns = X_val.columns)
input0 = full_pipeline.transform(input0)
print(ridgemodel.predict(input0))
output=np.exp(ridgemodel.predict(input0)) 
print(output)  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_features = []
    input_features.append(request.form['OS'])
    input_features.append(float(request.form['CPU_Threads']))
    input_features.append(float(request.form['CPU_Boosted_Clock']))
    input_features.append(float(request.form['CPU_L3']))
    input_features.append(float(request.form['CPU_TDP']))
    input_features.append(float(request.form['GPU_Memory']))
    input_features.append(request.form['GPU_Memory_Type'])
    input_features.append(float(request.form['GPU_memory_clock']))
    input_features.append(float(request.form['RAM']))
    input_features.append(float(request.form['RAM_DDR']))
    input_features.append(float(request.form['Storage']))
    input_features.append(float(request.form['Display_Inch']))
    input_features.append(float(request.form['Display_height']))
    input_features.append(float(request.form['Weight']))
    input_features = pd.DataFrame([input_features], columns = X_val.columns)
    input_features = full_pipeline.transform(input_features)
    if request.form['model'] == 'ridge':
        output=np.exp(ridgemodel.predict(input_features)) 
    if request.form['model'] == 'lasso':
        output=np.exp(lassomodel.predict(input_features)) 
    if request.form['model'] == 'random_forest':
        output=np.exp(forestmodel.predict(input_features)) 
    if request.form['model'] == 'xgb':
        output=np.exp(xgbmodel.predict(input_features)) 

    return render_template('index.html', prediction_text='The price is {} USD'.format(output))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)