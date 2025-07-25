from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import uuid
import json
import re
import requests
import os
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
PERMISSION_MANAGER_URL = os.environ.get('PERMISSION_MANAGER_URL', 'http://permission-manager:5000')
FLAG_SERVER_URL = os.environ.get('FLAG_SERVER_URL', 'http://golang-flag-server:5000')


def remove_json_comments(json_str):
    # Remove /* */ style comments
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    # Remove // style comments
    json_str = re.sub(r'//.*', '', json_str)
    json_str = re.sub(r'\s+', '', json_str)
    return json_str
def has_duplicate_keys(json_str):
    try:
        def detect_duplicates(pairs):
            keys = [k for k, _ in pairs]
            if len(keys) != len(set(keys)):
                raise ValueError("Duplicate key detected")
            return dict(pairs)
        json.loads(remove_json_comments(json_str), object_pairs_hook=detect_duplicates)
        return False  # No duplicate keys
    except Exception as e:
        print(e)
        if "Duplicate key detected" in str(e):
            return True # Duplicate keys found
        return True  # Other JSON errors


@app.route('/')
def index():
    # Assign session if not yet assigned
    if 'id' not in session:
        session['id'] = str(uuid.uuid4())
    
    # Check if account exists
    has_account = session.get('account_created', False)
    if has_account:
        return render_template('dashboard.html', session_id=session['id'])
    else:
        return render_template('index.html', session_id=session['id'])
    

@app.route('/create', methods=['POST'])
def create_account():
    # Get JSON data from request
    json_str = request.get_data(as_text=True)  # Get raw body as string
    key_to_insert = '"authorised_to_modify_perms":0'
    if json_str.startswith("{"):
        json_str = "{" + key_to_insert + "," + json_str[1:]
    else:
        return jsonify({'error': 'Not a valid Json Object'}), 400
    if has_duplicate_keys(json_str):
        return jsonify({'error': 'Duplicate keys found in JSON or Invalid JSON'}), 400
    
    # Post to permission manager
    response = requests.post(
        f'{PERMISSION_MANAGER_URL}/create',
        data=json_str,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        session['account_created'] = True
        root_perm_json_str = """
        {
            "root": 1
        }
        """
        requests.post(f"{FLAG_SERVER_URL}/create", data={'uuid': session['id'], 'root_perm': root_perm_json_str})
        return jsonify({'success': True, 'message': 'Account created successfully'})
    else:
        return jsonify({'error': 'Failed to create account with permission manager'}), 500


@app.route('/update_perms', methods=['POST'])
def update_perms():
    # First, check if user is authorized to modify permissions
    fetch_response = requests.get(
        f'{PERMISSION_MANAGER_URL}/fetch_perms',
        params={'uuid': session.get('id')},
            timeout=10
        )
    resp_json = fetch_response.json()
    if fetch_response.status_code != 200:
        return jsonify({'error': 'Unknown error'}), fetch_response.status_code
    if resp_json.get('authorised_to_modify_perms', 0) != 1:
        return jsonify({'error': 'User not authorized to modify permissions'}), 403
    
    # If user has authorized to modify, check if he is modifying his own perms or trying to give root perms
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    uuid = json_data.get('uuid')
    root_perm = json_data.get('root')
    if uuid != session.get('id'):
        return jsonify({'error': 'You can only update your own permissions'}), 403
    if root_perm == 0:
        return jsonify({'error': 'Not everyone can go around giving root perms'}), 400
    
    # If pass check, proceed with update
    root_perm_json_str = '{"root":' + str(root_perm) + '}'
    resp = requests.post(f"{FLAG_SERVER_URL}/create", data={'uuid': uuid, 'root_perm': root_perm_json_str})
    if resp.status_code == 200:
        return jsonify({'success': True, 'message': 'Permissions updated successfully'})
    else:
        return jsonify({'error': 'Failed to update permissions'}), 500


@app.route('/get_flag')
def get_flag():
    uuid = session.get('id')
    if not uuid:
        return jsonify({'error': 'You do not have an Admin Portal account'}), 400
    resp = requests.get(f"{FLAG_SERVER_URL}/flag", params={'uuid': uuid}, timeout=10)
    if resp.status_code == 200:
        flag = resp.json()
        return render_template('flag.html', flag=flag['flag'])
    else:
        return render_template('flag.html', flag="flag server 500 error")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)