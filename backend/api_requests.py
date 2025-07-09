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
    """
    The output of this endpoint should be a list of posts sorted based on the provided parameters.
    If the parameters are not provided, the list should retain the original order of posts.
    """
    try:
        sort_criteria, direction = helpers.get_parameters_for_sorting()

        # List all posts without query parameters
        if not sort_criteria and not direction:
            return jsonify(posts), 200

    except Exception as error:
        return jsonify({'Error sort criteria': str(error)}), 400

    try:
        sorted_list = sorted(
            posts,
            key=lambda post: post[sort_criteria],
            reverse=(direction == 'desc')
        )

        return jsonify(sorted_list), 200
    except Exception as error:
        # 500 -> internal server error
        return jsonify({'Error sorting posts': str(error)}), 500


def do_delete_request(posts, post_id):
    try:
        post_to_handle = helpers.find_post_by_id(post_id, posts)

        if not post_to_handle:
            return jsonify(f'No post with id {post_id} found.'), 404

    except Exception as error:
        # 500 -> internal server error
        return jsonify({'Error finding post': str(error)}), 500

    try:
        posts.remove(post_to_handle)

        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

    except Exception as error:
        # 500 -> internal server error
        return jsonify({'Error deleting the post': str(error)}), 500


def do_update_request(posts, post_id):
    try:
        post_to_handle = helpers.find_post_by_id(post_id, posts)

        if not post_to_handle:
            return jsonify(f'No post with id {post_id} found.'), 404

    except Exception as error:
        # 500 -> internal server error
        return jsonify({'Error finding post': str(error)}), 500

    try:
        new_post_data = request.get_json()
        post_to_handle.update(new_post_data) # updates the dictionary (post)

        return jsonify(post_to_handle), 200

    except Exception as error:
        # 500 -> internal server error
        return jsonify({'Error updating post': str(error)}), 500


def do_get_request_to_search(posts):
    try:
        title = request.args.get('title')
        content = request.args.get('content')
    except Exception as error:
        # 400 -> Bad request
        return jsonify({'Error getting search parameters': str(error)}), 400

    match_posts = []

    try:
        for post in posts:
            if title and title.lower() in post['title'].lower():
                match_posts.append(post)
                continue # to avoid a matching post is added twice when title and content match

            if content and content.lower() in post['content'].lower():
                match_posts.append(post)

        return jsonify(match_posts), 200

    except Exception as error:
        return jsonify({'Error searching post': str(error)}), 404