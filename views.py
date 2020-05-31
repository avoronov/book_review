from collections.abc import Iterable

from faker import Faker
from marshmallow import ValidationError, EXCLUDE
import random

from sanic.log import logger
from sanic.response import json, redirect, empty
from sanic.views import HTTPMethodView

from asyncpg.exceptions import ForeignKeyViolationError

from models import db, Author, Book, Publisher
from schemas import BookSchema, AuthorSchema, PublisherSchema


# TODO
# - add auth
# - swap get_or_404 with custom code to unify responses
# - add pagination


def make_response(result=None, errors=None, status=200):
    resp = {}

    if result is not None:
        resp["result"] = result

    if errors is not None:
        if not isinstance(errors, Iterable):
            errors = [errors]
        resp["errors"] = errors

    logger.info(resp)

    if resp:
        return json(resp, status=status)
    else:
        return empty(status=status)


class BooksView(HTTPMethodView):
    schema = BookSchema()

    async def get(self, request):  # noqa
        books = await Book.load(author=Author, publisher=Publisher).gino.all()

        # TODO

        resp = self.schema.dump(books, many=True)
        return make_response(result=resp)

    async def post(self, request):  # noqa
        book_data = request.json or {}

        try:
            validated_data = self.schema.load(book_data, unknown=EXCLUDE)
            book = await Book.create(**validated_data)
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)
        except ForeignKeyViolationError as err:
            # this checks look so weird
            msg = "Unknown error on book creation"
            if 'author_id' in err.detail:
                msg = {"author_id": f"Author #{book_data.get('author_id')} not found"}
            elif 'publisher_id' in err.detail:
                msg = {"publisher_id": f"Publisher #{book_data.get('publisher_id')} not found"}
            return make_response(errors=msg, status=400)

        resp = self.schema.dump(book)
        return make_response(result=resp, status=201)


class BookView(HTTPMethodView):
    schema = BookSchema()

    async def get(self, request, book_id):  # noqa
        book = await Book.load(
            author=Author,
            publisher=Publisher
        ).where(Book.id == book_id).gino.first()

        if book is None:
            return make_response(errors=f"Book #{book_id} not found", status=404)

        resp = self.schema.dump(book)
        return make_response(result=resp)

    async def put(self, request, book_id):  # noqa
        book = await Book.get_or_404(book_id)

        book_data = request.json or {}

        try:
            validated_data = self.schema.load(book_data, unknown=EXCLUDE)
            await book.update(**validated_data).apply()
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)
        except ForeignKeyViolationError as err:
            # this checks look so weird
            msg = "Unknown error on book creation"
            if 'author_id' in err.detail:
                msg = {"author_id": f"Author #{book_data.get('author_id')} not found"}
            elif 'publisher_id' in err.detail:
                msg = {"publisher_id": f"Publisher #{book_data.get('publisher_id')} not found"}
            return make_response(errors=msg, status=400)

        book = await Book.load(
            author=Author,
            publisher=Publisher
        ).where(Book.id == book_id).gino.first()

        resp = self.schema.dump(book)
        return make_response(result=resp, status=200)

    async def delete(self, request, book_id):  # noqa
        book = await Book.get_or_404(book_id)
        await book.delete()
        make_response(result=f"Book #{book_id} is deleted", status=200)


class AuthorsView(HTTPMethodView):
    schema = AuthorSchema()

    async def get(self, request):  # noqa
        authors = await Author.gino.all()
        resp = self.schema.dump(authors, many=True)
        return make_response(result=resp)

    async def post(self, request):  # noqa
        author_data = request.json or {}

        try:
            validated_data = self.schema.load(author_data)
            author = await Author.create(**validated_data)
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)

        resp = self.schema.dump(author)
        return make_response(result=resp, status=201)


class AuthorView(HTTPMethodView):
    schema = AuthorSchema()

    async def get(self, request, author_id):  # noqa
        author = await Author.get_or_404(author_id)
        resp = self.schema.dump(author)
        return make_response(result=resp)

    async def put(self, request, author_id):
        author = await Author.get_or_404(author_id)

        author_data = request.json or {}

        try:
            validated_data = self.schema.load(author_data)
            await author.update(**validated_data).apply()
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)

        resp = self.schema.dump(author)
        return make_response(result=resp, status=200)

    async def delete(self, request, author_id):  # noqa
        author = await Author.get_or_404(author_id)

        try:
            await author.delete()
        except ForeignKeyViolationError:
            # this checks look so weird
            msg = {"author_id": f"There are several books, referencing author #{author_id}"}
            return make_response(errors=msg, status=400)

        make_response(result=f"Author #{author_id} is deleted", status=200)


class PublishersView(HTTPMethodView):
    schema = PublisherSchema()

    async def get(self, request):  # noqa
        publishers = await Publisher.gino.all()
        resp = self.schema.dump(publishers, many=True)
        return make_response(result=resp)

    async def post(self, request, *args, **kwargs):  # noqa
        publisher_data = request.json or {}

        try:
            validated_data = self.schema.load(publisher_data)
            publisher = await Publisher.create(**validated_data)
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)

        resp = self.schema.dump(publisher)
        return make_response(result=resp, status=201)


class PublisherView(HTTPMethodView):
    schema = PublisherSchema()

    async def get(self, request, publisher_id):  # noqa
        publisher = await Publisher.get_or_404(publisher_id)
        resp = self.schema.dump(publisher)
        return make_response(result=resp)

    async def put(self, request, publisher_id):
        publisher = await Publisher.get_or_404(publisher_id)

        publisher_data = request.json or {}

        try:
            validated_data = self.schema.load(publisher_data)
            await publisher.update(**validated_data).apply()
        except ValidationError as err:
            return make_response(errors=err.messages, status=400)

        resp = self.schema.dump(publisher)
        return make_response(result=resp, status=200)

    async def delete(self, request, publisher_id):  # noqa
        publisher = await Publisher.get_or_404(publisher_id)

        try:
            await publisher.delete()
        except ForeignKeyViolationError:
            # this checks look so weird
            msg = {"publisher_id": f"There are several books, referencing publisher #{publisher_id}"}
            return make_response(errors=msg, status=400)

        make_response(result=f"Publisher #{publisher_id} is deleted", status=200)


class MaintainanceView(HTTPMethodView):

    async def get(self, request):  # noqa

        count = 10
        faker = Faker(locale='en_US')

        authors = []
        publishers = []

        for _ in range(count):
            author = await Author.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
            authors.append(author)

            publisher = await Publisher.create(
                name=faker.company(),
            )
            publishers.append(publisher)

        authors_cnt = len(authors) - 1
        publishers_cnt = len(publishers) - 1

        for _ in range(count * count):
            await Book.create(
                title=faker.sentence(),
                brief=faker.paragraph(nb_sentences=5),
                rate=random.randint(0, 5),
                author_id=authors[random.randint(0, authors_cnt)].id,
                publisher_id=publishers[random.randint(0, publishers_cnt)].id,
            )

        return redirect('/books/')
