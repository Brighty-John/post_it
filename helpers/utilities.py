import requests
from typing import Union

from usernames import users


def get_data_from_url(route: str) -> Union[dict, list]:
    """
    Retrieve JSON data from a specified URL route.

    :param route: The URL route from which to retrieve JSON data.
    :return: JSON data retrieved from the specified URL route.

    """
    posts_response = requests.get(route)
    return posts_response.json()


def get_comments_for_post(post_id: Union[int, str]) -> Union[dict, list]:
    """
    Retrieve comments for a specified post ID.

    :param post_id: The ID of the post for which to retrieve comments. It can be either an integer or a string.
    :return: Comments associated with the specified post ID.
    """
    data = get_data_from_url(f'https://jsonplaceholder.typicode.com/comments?postId={post_id}')

    # Add Necessary Details to be displayed in UI
    for comment in data:
        user_email = comment["email"]
        comment["commenter"] = user_email.split('@')[0].replace('_', ' ').replace('.', ' ')     # Name of the Person
        comment["user_id"] = str(users[user_email])   # User ID - Needed for fetching Avatar from picsum site
    return data


def get_email_by_id(user_id: Union[str, int]) -> Union[str, None]:
    """
    Get the email associated with the given user_id from the users dictionary.

    :param user_id : The user ID for which the email is to be retrieved.
    :return: The email associated with the user ID if found, else None.
    """
    for email, id_num in users.items():
        if id_num == int(user_id):
            return email
    return None
