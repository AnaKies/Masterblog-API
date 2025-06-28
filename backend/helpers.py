from flask import request, jsonify


def generate_id(posts):
    """
    Searches for a maximal ID in the list of posts and
    generates a new one by incrementing the maximal ID.
    """
    max_id = 0

    for post in posts:
        if post['id'] > max_id:
            max_id = post['id']

    generated_id = max_id + 1

    return generated_id


def get_post():
    try:
        # Get the new post from the client
        new_post = request.get_json()
    except Exception as error:
        return jsonify({'Error': str(error)}), 400

    if not new_post:
        return jsonify({'Error': 'Empty post body.'}), 400

    if 'title' not in new_post:
        return jsonify({'Error': 'Missing title'}), 400

    if 'content' not in new_post:
        return jsonify({'Error': 'Missing content'}), 400

    return new_post