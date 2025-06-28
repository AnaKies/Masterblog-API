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
        try:
            new_post = helpers.get_post_to_add()
        except Exception as error:
            return jsonify({'Error': str(error)}), 404

        new_id = helpers.generate_id(POSTS)
        new_post['id'] = new_id
        POSTS.append(new_post)

        return jsonify(new_post), 201
    else:
        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def handle_post(post_id):
    try:
        post_to_handle = helpers.find_post_by_id(post_id, POSTS)
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    if request.method == 'DELETE':
        POSTS.remove(post_to_handle)

        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'})
    else:
        # Update post (PUT)
        try:
            new_post_data = request.get_json()
        except Exception as error:
            return jsonify({'Error': str(error)}), 404
        post_to_handle.update(new_post_data)
        return jsonify(post_to_handle), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
