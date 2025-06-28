from flask import Flask, jsonify, request
from flask_cors import CORS
import helpers

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Zebra post", "content": "This is a wild animal."},
    {"id": 2, "title": "Apple pie", "content": "This is about baking."},
    {"id": 3, "title": "Coding life", "content": "This is a post about Python."},
    {"id": 4, "title": "Mountain echo", "content": "This is a nature post."},
    {"id": 5, "title": "Yellow sun", "content": "This is a sunny post."},
    {"id": 6, "title": "Banana world", "content": "This is a fruit post."},
    {"id": 7, "title": "Digital storm", "content": "This is about technology."},
    {"id": 8, "title": "Happy hour", "content": "This is a fun time post."},
    {"id": 9, "title": "Zen garden", "content": "This is a relaxing post."},
    {"id": 10, "title": "Early bird", "content": "This is a morning post."},
    {"id": 11, "title": "Lazy dog", "content": "This is a chill post."},
    {"id": 12, "title": "Violet flame", "content": "This is a mystical post."},
    {"id": 13, "title": "Jungle book", "content": "This is a classic tale."},
    {"id": 14, "title": "Quiet forest", "content": "This is about trees."},
    {"id": 15, "title": "Rocket launch", "content": "This is space-related."},
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
        # GET request
        sort_criteria, direction = helpers.get_parameters_for_sorting()

        if not sort_criteria and not direction:
            return jsonify(POSTS), 200
        else:
            sorted_list = sorted(
                POSTS,
                key=lambda post: post[sort_criteria],
                reverse=(direction == 'desc')
            )

            return jsonify(sorted_list), 200


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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    try:
        title = request.args.get('title')
        content = request.args.get('content')
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    match_posts = []

    for post in POSTS:
        if title and title.lower() in post['title'].lower():
            match_posts.append(post)
            continue # to avoid a matching post is added twice

        if content and content.lower() in post['content'].lower():
            match_posts.append(post)

    return jsonify(match_posts), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
