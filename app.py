from flask import Flask, render_template


from helpers.utilities import get_data_from_url, get_comments_for_post, get_email_by_id
from usernames import users

app = Flask(__name__)


@app.route('/user/<user_id>')
def filter_posts_by_user(user_id: str):
    """
        Filter posts by a specific user ID and retrieve associated comments.

        :param user_id: The ID of the user whose posts are to be filtered.
        :type user_id: str
        :return: Rendered template displaying filtered posts and associated comments.
        """
    # Retrieve all posts
    posts = get_data_from_url('https://jsonplaceholder.typicode.com/posts')

    # Filter the posts for the specified user_id
    filtered_posts = [post for post in posts if post['userId'] == int(user_id)]
    author_mail = get_email_by_id(user_id)
    author = author_mail.split('@')[0].replace('_', ' ').replace('.', ' ')
    # Retrieve comment for each filtered post
    for post in filtered_posts:
        post["author"] = author
        post['comments'] = get_comments_for_post(post["id"])
    return render_template('homepage.html', posts=filtered_posts, user_mapping=users)


@app.route('/')
@app.route('/<post_id>')
def post_details(post_id=None):
    """
    Retrieve details of a specific post or all posts if no post_id is provided.
    Fetch comments for each post and add them to the post object.

    :param post_id: Optional. The ID of the post to retrieve details for.
    :type post_id: str or None
    :return: Rendered template displaying post details and associated comments.
    """
    # Fetch all posts or specific post
    resource_url = f'https://jsonplaceholder.typicode.com/posts/{post_id}' if post_id else \
        'https://jsonplaceholder.typicode.com/posts'
    posts = get_data_from_url(resource_url)

    # When a specific post is required, the return data will be a dictionary - convert it into a list of dictionary
    if post_id:
        posts = [posts]

    # Fetch comments for each post and add them to the post object
    for post in posts:
        post['author'] = get_email_by_id(post["userId"]).split('@')[0].replace('_', ' ').replace('.', ' ')
        post['comments'] = get_comments_for_post(post["id"])

    return render_template('homepage.html', posts=posts, user_mapping=users)


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
