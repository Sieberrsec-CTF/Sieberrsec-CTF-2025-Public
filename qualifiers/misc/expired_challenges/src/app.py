from flask import Flask, request, jsonify
import os
import uuid
from judge import judge_submission

app = Flask(__name__)
UPLOAD_FOLDER = 'submissions/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/submit', methods=['POST'])
def submit():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    code_file = request.files['file']
    lang = request.form.get('lang', 'cpp')
    file_ext = '.cpp' if lang == 'cpp' else '.py'

    sub_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, sub_id + file_ext)
    code_file.save(file_path)

    verdict, detail = judge_submission(file_path, lang)
    response = {'verdict': verdict, 'detail': detail}

    if verdict == 'AC':
        with open('flag.txt') as f:
            response['flag'] = f.read().strip()

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
