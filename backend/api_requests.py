from flask import  jsonify, request
import helpers


def do_post_request_to_add(posts):
    try:
        new_post = helpers.get_post_to_add()
        new_id = helpers.generate_id(posts)
        new_post['id'] = new_id
        posts.append(new_post)

        return jsonify(new_post), 201

    except Exception as error:
        return jsonify({'Error adding new post': str(error)}), 400


def do_get_request_to_show_or_sort(posts):
    sort_criteria, direction = helpers.get_parameters_for_sorting()

    # List all posts without query parameters
    if not sort_criteria and not direction:
        return jsonify(posts), 200
    else:
        sorted_list = sorted(
            posts,
            key=lambda post: post[sort_criteria],
            reverse=(direction == 'desc')
        )

        return jsonify(sorted_list), 200


def do_delete_request(posts, post_id):
    try:
        post_to_handle = helpers.find_post_by_id(post_id, posts)
        posts.remove(post_to_handle)

        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

    except Exception as error:
        return jsonify({'Error deleting the post': str(error)}), 404


def do_update_request(posts, post_id):
    try:
        post_to_handle = helpers.find_post_by_id(post_id, posts)
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    try:
        new_post_data = request.get_json()
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    post_to_handle.update(new_post_data)
    return jsonify(post_to_handle), 200


def do_get_request_to_search(posts):
    try:
        title = request.args.get('title')
        content = request.args.get('content')
    except Exception as error:
        return jsonify({'Error': str(error)}), 404

    match_posts = []

    for post in posts:
        if title and title.lower() in post['title'].lower():
            match_posts.append(post)
            continue # to avoid a matching post is added twice

        if content and content.lower() in post['content'].lower():
            match_posts.append(post)

    return jsonify(match_posts), 200