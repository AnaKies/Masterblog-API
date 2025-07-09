from flask import request, jsonify


def generate_id(posts):
    """
    Searches for a maximal ID in the list of posts and
    generates a new one by incrementing the maximal ID.
    If the post list is empty, the ID is 1.
    """
    max_id = 0

    try:
        for post in posts:
            if post['id'] > max_id:
                max_id = post['id']

        generated_id = max_id + 1

        return generated_id

    except Exception as error:
        raise Exception(f'Error generating ID: {error}')


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
    try:
        for post in posts:
            if post['id'] == post_id:
                return post
        raise Exception(f'No post with id {post_id} found.')
    except Exception as error:
        raise Exception(f'Error finding post with id {post_id}: {error}')


def get_parameters_for_sorting():
    try:
        # check if user keys exist and one of them is wrong
        for key in request.args:
            if key not in ['sort', 'direction']:
                raise Exception(f'Wrong key argument: {key}')

        sort_criteria = request.args.get('sort')
        direction = request.args.get('direction')

    except Exception as error:
        raise Exception(f'Error getting query parameters: {error}')

    if sort_criteria and sort_criteria not in ['title', 'content']:
        raise Exception('The value of the key "sort" should be "title" or "content"')

    if direction and direction not in ['asc', 'desc']:
        raise Exception('The value of the key "direction" should be "asc" or "desc"')

    return sort_criteria, direction