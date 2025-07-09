from flask import Flask, request
from flask_cors import CORS
import api_requests

app = Flask(__name__)
# the CORS allows the browser the cross-domain communication (front-end and back-end)
CORS(app)

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
def get_sort_add_posts():
    if request.method == 'POST':
        response = api_requests.do_post_request_to_add(POSTS)
    else:
        # GET request
        response = api_requests.do_get_request_to_show_or_sort(POSTS)

    return response


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def delete_update_posts(post_id):
    if request.method == 'DELETE':
        response = api_requests.do_delete_request(POSTS, post_id)
    else:
        # Update post (PUT)
        response = api_requests.do_update_request(POSTS, post_id)

    return response


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    response = api_requests.do_get_request_to_search(POSTS)

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
