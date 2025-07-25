from flask import Flask, request, render_template, redirect, flash
import os
from werkzeug.utils import secure_filename

import PickleRick

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = "./uploads"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'recipe' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['recipe']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename[::-1].startswith('.pkl'[::-1]):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                with open(filepath, 'rb') as f:
                    obj = PickleRick.loads(f.read())
                
                result = str(obj)

            except Exception as e:
                result = f"Error: {e}"
        else:
            flash('Only .pkl files allowed!')
    
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run()