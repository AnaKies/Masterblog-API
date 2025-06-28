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


def get_post_to_add():
    """
    Gets the post from the body of the client's POST request.
    Checks that the request is valid.
    """
    try:
        # Get the new post from the client
        new_post = request.get_json()
    except Exception as error:
        raise Exception(f'Invalid JSON. {error}')

    if not new_post:
        raise Exception('Empty post body.')

    if 'title' not in new_post:
        raise Exception('Missing title')

    if 'content' not in new_post:
        raise Exception('Missing content')

    return new_post


def find_post_by_id(post_id, posts):
    """
    Finds the post with the given id.
    If there is no post with this id, return None.
    """
    for post in posts:
        if post['id'] == post_id:
            return post
    raise Exception(f'No post with id {post_id} found.')