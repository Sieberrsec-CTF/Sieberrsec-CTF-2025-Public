from quart import Quart, request, jsonify
import os
import io
import inspect
import asyncio
from sandbox import SkibidiSandBox
import tarfile
import base64
from concurrent.futures import ThreadPoolExecutor
import functools
import random
import time

app = Quart(__name__,static_folder=None)

executor = ThreadPoolExecutor(max_workers=4)

user_filesystem = SkibidiSandBox(base_path='users')
allowed_funcs = ['cp', 'get_id', 'list_files', 'mkdir', 'mktempdir', 'rm', 'stat', 'write_file', 'read_file']


async def async_tarfile_open(fileobj, mode):
    """Async wrapper for tarfile.open"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor, 
        functools.partial(tarfile.open, fileobj=fileobj, mode=mode)
    )


# this helps our developers test their apps in high latency environments!
# please ignore the following code 👍
@app.before_request
async def firewall():
    await asyncio.sleep(random.randint(1000,3000)/1000)

@app.route('/list_users', methods=['GET'])
async def list_users():
    try:
        users = os.listdir('users')
        log_file = ''.join([f'user: {user}, time {str(time.time())}, request: {request.url}, args: {request.args}, headers: {request.headers}\n' for user in users])
        with open('users.json', 'w') as f:
            f.write(log_file)
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sandbox', methods=['GET'])
async def sandbox():
    method = request.args.get('method')
    args = request.args.getlist('args')
    
    if method not in allowed_funcs:
        return jsonify({'error': 'Invalid method'}), 400
    
    for arg in args:
        if not isinstance(arg, str):
            return jsonify({'error': 'All arguments must be strings'}), 400
        if len(arg) > 200:
            return jsonify({'error': 'Argument too long'}), 400
    try:
        async_method = getattr(user_filesystem, method)
        import types
        if isinstance(async_method, types.MethodType):
            sig = inspect.signature(async_method)
            arg_count = len(sig.parameters)
        
        if len(args) != arg_count:  
            return jsonify({'error': f'Invalid number of arguments for {method}. Expected {arg_count}, got {len(args)}'}), 400
    except AttributeError:
        return jsonify({'error': f'Method {method} not found'}), 400
    
    try:
        async_method = getattr(user_filesystem, method)
        result = await async_method(*[str(arg) for arg in args])
        return jsonify({'result': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['GET'])
async def upload():
    tar64 = request.args.get('tar')
    
    if not tar64:
        return jsonify({'error': 'Missing tar parameter'}), 400
    
    try:
        loop = asyncio.get_event_loop()
        tar_data = await loop.run_in_executor(executor, base64.b64decode, tar64)
        tar_bytes = io.BytesIO(tar_data)
        if len(tar_bytes.getvalue()) > 1000:
            # Storage is expensive! Employees should make their projects small and efficient!
            return jsonify({'error': 'Tar file too large'}), 400
        try:
            await async_tarfile_open(fileobj=tar_bytes, mode='r')
            tar_bytes.seek(0)  
        except tarfile.TarError:
            return jsonify({'error': 'Invalid tar file'}), 400
        
        result = await user_filesystem.upload(tar_bytes)
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
async def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
async def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
async def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)