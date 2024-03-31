from flask import Flask
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pydicom import dcmread

 
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

            print(f"save to {os.path.join(app.config['UPLOAD_FOLDER'],filename)}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                   filename))
            
            # 要檢查 沒有檔案才放進來，已經有了要render錯誤
            
            # return redirect(url_for('uploaded_file',
                                    # filename=filename))
            print("allow file", file.filename)
        else:
            # print("not allow")  # render not allow
            return "Error: the file should be dcm format"
    
    # 主畫面
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# list all available dcm files

# create an API to receive the DCM and show the information



if __name__ == '__main__':  
   app.run()