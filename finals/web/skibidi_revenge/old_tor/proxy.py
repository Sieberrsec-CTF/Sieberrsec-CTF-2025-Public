from quart import Quart, request, jsonify
app = Quart(__name__)


@app.route('/')
def hello():
    with open('/home/skibidi/hidden_service/hostname', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)