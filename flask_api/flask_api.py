from flask import Flask, jsonify, request
from flask import render_template, abort
from werkzeug.utils import secure_filename
import os
from pydicom import dcmread
from glob import glob

 
# instance of flask application
app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
 

# create an API to store the DCM
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'dcm'

@app.route('/upload_dcm', methods=['GET','POST'])
def upload_dcm():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Check the file is exist already
            if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                abort(500, "File already exists.")

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                   filename))
            
        else:
            abort(500, "the file should be dcm format")
    
    # 主畫面
    return render_template('home.html')

# list all available dcm files
@app.route('/list_dcm', methods=['GET'])
def list_dcm():
    if request.method == 'GET':
        if not os.path.isdir(UPLOAD_FOLDER):
            abort(500, "DCM path not found in server")
        
        files = glob(UPLOAD_FOLDER + '/*.dcm')
        return jsonify([os.path.basename(file) for file in files])
    
# create an API to receive the DCM and show the information
@app.route('/dcm_information/<dcm_file_name>', methods=['GET'])
def retrieve_dcm_information(dcm_file_name):
    dcm_file = dcm_file_name + '.dcm'
    try:
        ds = dcmread("/".join([UPLOAD_FOLDER, dcm_file]))
    except FileNotFoundError:
        return "File not Found"
    
    attributes = ['PatientID', 'AccessionNumber', 'StudyInstanceUID', 
              'SOPInstanceUID', 'ReferencedSOPInstanceUID', 
              'SeriesInstanceUID', 'SeriesDate', 'SeriesNumber']
    # handle keyerror
    result = {}
    for attr in attributes:
        if hasattr(ds, attr):
            result[attr] = getattr(ds, attr)
    
    print(result)
    return jsonify(result)

if __name__ == '__main__':  
   app.run()