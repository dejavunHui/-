from flask import Flask, render_template
from pathlib2 import Path
import shutil, os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from . import config
from . import app
from . import cnv
from . import eval
from . import array2dcm
from . import upload
ALLOWED_EXTIENSIONS = {'png', 'jpg', 'jpeg', 'nii', 'nii.gz', 'dcm', 'npy'}
app.config['UPLOAD_FOLDER'] = config.UPLOADDIR

d = array2dcm.DCMUtils(config.DCMDIR)
print(d.colortype)
d.gray()

def process():
    cnv.is_add()
    cnv(config.UPLOADDIR)
    #文件转移
    d = Path(config.UPLOADDIR)
    files = list(d.glob('*'))
    for idx, file_ in enumerate(files):
        try:
            shutil.move(str(file_), config.UPLOADBAKDIR)
        except:
            os.remove(str(file_))



def predict():
    e = eval.Eval(1, 512, config.NPYDIR, config.CHECKPOINTDIR)
    for data in e():
        d(data)
   

def upserver():
    upload(config.DCMDIR, config.DCMBAKDIR)

def allowed_file(filename):
    return '.' in filename #and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTIENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process()
            predict()
            upserver()
            return redirect(url_for('home'))
    return render_template('upload.html')


