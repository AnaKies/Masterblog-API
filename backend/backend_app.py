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
            new_post = helpers.get_post()
        except Exception as error:
            return jsonify({'Error': str(error)}), 404

        new_id = helpers.generate_id(POSTS)
        new_post['id'] = new_id
        POSTS.append(new_post)

        return jsonify(new_post), 201
    else:
        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post_to_delete = helpers.find_post_by_id(post_id, POSTS)
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    POSTS.remove(post_to_delete)

    return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
