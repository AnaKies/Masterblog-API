from flask import Flask, jsonify, request
from flask_cors import CORS
import helpers

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = helpers.get_post()
        new_id = helpers.generate_id(POSTS)
        new_post['id'] = new_id
        POSTS.append(new_post)

        return jsonify(new_post), 201
    else:
        return jsonify(POSTS)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
