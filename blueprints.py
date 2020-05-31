from sanic import Blueprint

from views import BooksView, BookView, AuthorsView, AuthorView, PublishersView, PublisherView, MaintainanceView


def get_blueprints():
    books_blue_print = Blueprint('books', url_prefix='/books')
    books_blue_print.add_route(BooksView.as_view(), '/')
    books_blue_print.add_route(BookView.as_view(), '/<book_id:int>')

    authors_blue_print = Blueprint('authors', url_prefix='/authors')
    authors_blue_print.add_route(AuthorsView.as_view(), '/')
    authors_blue_print.add_route(AuthorView.as_view(), '/<author_id:int>')

    publishers_blue_print = Blueprint('publishers', url_prefix='/publishers')
    publishers_blue_print.add_route(PublishersView.as_view(), '/')
    publishers_blue_print.add_route(PublisherView.as_view(), '/<publisher_id:int>')

    maintainance_blue_print = Blueprint('maintainance', url_prefix='/filldb')
    maintainance_blue_print.add_route(MaintainanceView.as_view(), '/')

    return books_blue_print, authors_blue_print, publishers_blue_print, maintainance_blue_print
