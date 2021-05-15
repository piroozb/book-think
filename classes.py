from __future__ import annotations

from typing import Set, List, Optional
from datetime import date
import uuid


class User:
    """A user class.

    === Public Attributes ===
    user_name:
        - the username that we allow (further update => restrict username?)
    # TODO
    password:
        - the password of the user
    favourites:
        - all of the user's favourite publications
    bio:
        - biography of the user

    === Private Attributes ===
    _join_date:
        - Autogenerated joined date
    """
    # find how to use bcrypt and google cloud secret manager to store all this
    user_name: str
    following: Set[str]
    _join_date: date
    favourites: List[Publication]
    bio: str
    _id: str
    # list? Dict?

    def __init__(self, user_name: str) -> None:
        self.user_name = user_name
        self.following = set()
        self._join_date = date.today()
        self.favourites = []
        self.bio = ''
        self._id = str(uuid.uuid4())

    def add_favourite(self, publication: Publication) -> None:
        self.favourites.append(publication)

    def add_bio(self, bio: str) -> None:
        self.bio = bio


class Post:
    """A post class.

    === Public Attributes ===
    content:
        - the content of this comment
    like:
        - how other reacts to it?? (less priority)
    created_by:
        - the user that made this rating
    created_on:
        - when the user made this post
    === Private Attributes ===


    === Representation Invariants ===
    """
    content: str
    like: Set[str]
    created_by: str
    created_on: date

    def __init__(self, content: str, user_name: str):
        self.content = content
        self.like = set()
        self.created_by = user_name
        self.created_on = date.today()

    def like(self, user: User) -> None:
        """Add or removes a user from the likes"""
        #  TODO think about how to unlike
        if user.user_name not in self.like:
            self.like.add(user.user_name)
        else:
            self.like.remove(user.user_name)

    def edit_content(self, content: str) -> None:
        """Edit the contents of this post to <content>"""
        self.content = content


class Rating(Post):
    """A rating class to rate a publication

    === Public Attributes ===
    rating:
        - how this user rates the publication.
    === Representation Invariants ===
    - 0.0 <= rating <= 5.0
    """
    # TODO how to deal with people making two reviews?
    rating: float

    def __init__(self, content: str, user_name: str, rating: float) -> None:
        super().__init__(content, user_name)
        self.rating = rating

    def edit_rating(self, rating: float) -> None:
        """Edit the rating of this Rating to <rating>"""
        self.rating = rating


class Comment(Post):
    """A Comment class to comment on a publication

    === Public Attributes ===
    replies:
        - A list of all replies to this comment
    """
    replies: List[Comment]

    def __init__(self, content: str, user_name: str) -> None:
        super().__init__(content, user_name)
        self.replies = []

    def create_replies(self, new_comment: Comment) -> None:
        """create a reply for the current comment  """
        self.replies.append(new_comment)


class Publication:
    """A publication class.

    === Public Attributes ===
    title:
        - publication name
    author:
        - name of the author of this publication
    genre:
        - publication genre
    ratings:
        - ratings posted by users
    thread:
        - a list of posts made by users
    """
    title: str
    author: str
    genre: str
    ratings: List[Rating]
    thread: List[Comment]

    def __init__(self, title: str, author: str, genre: str) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.ratings = []
        self.thread = []

    def add_rating(self, new_rating: Rating) -> None:
        """Add a rating to this publication"""
        # *currently I'm just appending it to a list,
        # maybe make it into a dict?? idk*
        self.ratings.append(new_rating)
        # Addressing the concern about multiple reviews from earlier, we can
        # change this method to return true/false depending on if adding was
        # successful, and make one of the failing conditions happen when a user
        # adds multiple reviews. We can check if they are about to add another
        # review by doing something like:
        # new_rating.created_by in
        # (rating.created_by for rating in self.ratings)

    def add_comment(self, new_comment: Comment) -> None:
        """Add a comment to this publication"""
        self.thread.append(new_comment)

    def calculate_rating(self) -> float:
        """Return the rating out of 5 stars"""
        # # uhhh i dont remember the optimal way of doing this
        # i = 0
        # count = 0
        # for item in self.rate:
        #     i += 1
        #     count += item.rating
        #
        # return count/i if i != 0 else 0

        total_rating = sum(rating.rating for rating in self.ratings)
        num_ratings = len(self.ratings)
        return total_rating / num_ratings if num_ratings > 0 else 0

    # Probably better to have separate methods for this
    # def delete_post(self, post: Post) -> bool:
    #     """Delete <post> from <self.thread> or <self.ratings>. Return true if
    #     this was successful and false otherwise.
    #     """
    #     try:
    #         if isinstance(post, Comment):
    #             self.thread.remove(post)
    #         elif isinstance(post, Rating):
    #             self.ratings.remove(post)
    #     except ValueError:
    #         return False
    #     return True

    def delete_rating(self, rating: Rating) -> bool:
        """Delete <rating> from <self.ratings>. Return true if this was
        successful and false otherwise.
        """
        try:
            self.ratings.remove(rating)
        except ValueError:
            return False
        return True

    def delete_comment(self, comment: Comment) -> bool:
        """Delete <rating> from <self.ratings>. Return true if this was
        successful and false otherwise.
        """
        try:
            self.thread.remove(comment)
        except ValueError:
            return False
        return True


class Book(Publication):
    """A book class.

    === Public Attributes ===
    pages:
        - number of pages this book has
    chapters:
        - number of chapters this book has. Equal to None if this book
          has no chapters.
    === Representation Invariants ===
    - <chapters> is None if and only if this book has no chapters
    """
    pages: int
    chapters: int

    def __init__(self, title: str, author: str, genre: str, pages: int,
                 chapters: Optional[int]) -> None:
        # Same as Publication.__init__(...)
        super().__init__(title, author, genre)
        self.pages = pages
        self.chapters = chapters


class Series(Publication):
    """A series class.

    === Public Attributes ===
    volumes:
        - a list containing the publications included in this series
    """
    volumes: List[Publication]

    def __init__(self, title: str, author: str, genre: str,
                 volumes: List[Publication]) -> None:
        super().__init__(title, author, genre)
        self.volumes = volumes[:]
