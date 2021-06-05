from flask import Flask, render_template,request,redirect,flash
import sqlite3,requests
from model import *
from PIL import Image 
import numpy as np,os,glob,pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/classification')
def classification():
    return render_template('classification.html')

@app.route('/data_viz',methods=['GET','POST'])
def data_viz():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.form
        data = data.to_dict(flat=False)
        print(data)
        if 'max' in data:
            selection = str(data.get('Attribute')[0])
            res = 'SELECT * FROM houses WHERE '+selection+'= (Select MAX('+selection+') FROM houses)'
            results = cur.execute(res)
            for x in results:
                ret = x
            conn.close()    
            output_string = "The tuple with the highest value of selection,"+selection+": "+str(ret)
            return render_template('data_viz.html',ret = output_string,ret2='')
        elif 'min' in data:
            selection = str(data.get('Attribute')[0])
            res = 'SELECT * FROM houses WHERE '+selection+'= (Select MIN('+selection+') FROM houses)'
            results = cur.execute(res)
            for x in results:
                ret = x
            conn.close()
            
            output_string = "The tuple with the lowest value of selection,"+selection+": "+str(ret)
            return render_template('data_viz.html',ret = '',ret2 = output_string)
        elif 'submit_graphs' in data:
            data = request.form
            data = data.to_dict(flat=False)
            selection_one = str(data.get('vals')[0])
            selection_two = str(data.get('vals')[1])
            df = pd.read_csv('static/data/out.csv')
            x = df[selection_one]
            y = df[selection_two]
            plt.scatter(x,y)
            plt.xlabel(selection_one)
            plt.ylabel(selection_two)
            title = "Scatter plot between "+selection_one+" and "+selection_two
            plt.title(title)
            plt.savefig('static/created/created.png')
            return render_template('data_viz.html',fig='succ') 
    else:
        return render_template('data_viz.html') 

@app.route('/',methods=['POST'])
def predict():
    file = request.files['img']
    if file.filename == '':
        flash('No image here')
        return redirect('classification.html')
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_file_name= 'static/uploads/'+filename
        
    im = Image.open(new_file_name)
    im=im.resize((224,224))
    input_img = np.asarray(im)
    input_img = input_img[None,:]
    preds = model(input_img)
    return render_template('classification.html',prediction_text = preds)
    
@app.route('/')
def index():
    return render_template('index.html')