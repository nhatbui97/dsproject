import numpy as np
from flask import Flask, request, render_template
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

ridgemodel = pickle.load(open('ridgemodel.pkl','rb'))
lassomodel = pickle.load(open('lassomodel.pkl','rb'))
forestmodel = pickle.load(open('forestmodel.pkl','rb'))
xgbmodel = pickle.load(open('xgbmodel.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    input_features = []
    input_features.append(request.form['RAM'])
    input_features.append(request.form['CPU_Threads'])
    input_features.append(request.form['Display_Inch'])
    input_features.append(request.form['CPU_TDP'])
    input_features.append(request.form['GPU_Memory'])
    input_features.append(request.form['Display_height'])
    input_features.append(request.form['Weight'])
    input_features.append(request.form['CPU_L3'])
    input_features.append(request.form['CPU_Boosted_Clock'])
    input_features.append(request.form['GPU_memory_clock'])
    input_features.append(request.form['Storage'])


    input1 = [float(x) for x in input_features]
    std_scaler = StandardScaler()
    input1 = list(std_scaler.fit_transform([input1])[0])

    input2 = []
    if request.form['GPU_Memory_Type'] == 'GDDR5':
        input2 += [1,0,0,0]
    if request.form['GPU_Memory_Type'] == 'GDDR6':
        input2 += [0,1,0,0]
    if request.form['GPU_Memory_Type'] == 'LPDDR4X':
        input2 += [0,0,1,0]
    if request.form['GPU_Memory_Type'] == 'NoGPU':
        input2 += [0,0,0,1]
    if request.form['OS'] == 'Linux':
        input2 += [1,0,0]
    if request.form['OS'] == 'MacOS':
        input2 += [0,1,0]    
    if request.form['OS'] == 'Window':
        input2 += [0,0,1]   
    if request.form['RAM_DDR'] == 'DDR1':
        input2 += [1,0,0,0]
    if request.form['RAM_DDR'] == 'DDR3':
        input2 += [0,1,0,0]
    if request.form['RAM_DDR'] == 'DDR4':
        input2 += [0,0,1,0]
    if request.form['RAM_DDR'] == 'DDR5':
        input2 += [0,0,0,1]
    

    input = input1 + input2
    if request.form['model'] == 'ridge':
        output=np.exp(ridgemodel.predict([input])) 
    if request.form['model'] == 'lasso':
        output=np.exp(lassomodel.predict([input])) 
    if request.form['model'] == 'random_forest':
        output=np.exp(forestmodel.predict([input])) 
    if request.form['model'] == 'xgb':
        output=np.exp(xgbmodel.predict([input])) 

    return render_template('index.html', prediction_text='The price is {} USD'.format(output))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)