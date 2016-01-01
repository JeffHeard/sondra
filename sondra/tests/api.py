from sondra import document, suite, collection, application
from sondra.auth.request_processor import AuthRequestProcessor
from sondra.auth.decorators import authentication_required, authorization_required, authenticated_method, authorized_method
from sondra.expose import expose_method
from sondra.schema import S
from sondra.lazy import fk, ref


class ConcreteSuite(suite.Suite):
    "A simple API for testing"
    definitions = {
        "concreteSuiteDefn": {"type": "string", "pattern": "[0-9]+"}
    }
    api_request_processors = (
        AuthRequestProcessor(),
    )

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


class SimpleDocument(document.Document):
    "A simple document type"

    schema = S.object(
        {
            "name": S.string(title="Name", description="The name of the document"),
            "slug": S.string(),
            "date": S.date(title="Date", description="The date of the document"),
            "value": S.integer(default=0),
            "defaultValue": S.string(
                title="Default Value",
                default="Default Value 1",
                description="A property with a default value"),
            "timestamp": S.datetime(),
        },
        required=["name",],
        propertyOrder=['name','date','timestamp']
    )
    processors = (
        document.SlugPropertyProcessor('name'),
    )
    specials = {
        "date": document.DateTime(),
        "timestamp": document.Now()
    }

    @expose_method
    def arg_test(self, dict_arg: dict={}, int_arg: int=0, str_arg: str="", list_arg: list=[]) -> list:
        return [{"one": 1}, 0, 2]


    @expose_method
    def simple_none_return(self) -> None:
        return None

    @expose_method
    def simple_int_return(self) -> int:
        return 1

    @expose_method
    def simple_number_return(self) -> float:
        return 1.0

    @expose_method
    def simple_str_return(self) -> str:
        return "String"

    @expose_method
    def list_return(self) -> [str]:
        return ["0", "1", "2", "3"]

    @expose_method
    def dict_return(self) -> dict:
        return {
            'a': 0,
            'b': 1,
            'c': 2
        }

    @expose_method
    def operates_on_self(self) -> str:
        return self.schema['type']

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


class ForeignKeyDoc(document.Document):
    "A document with a foreign key."
    schema = S.object(
        {
            "name": S.string(),
            "slug": S.string(),
            "simple_document": fk(SimpleDocument),
            "rest": S.array(items=fk(SimpleDocument))
        },
        required=["name"]
    )
    processors = (
        document.SlugPropertyProcessor('name'),
    )


class SimplePoint(document.Document):
    "A simple geographic point"
    schema = S.object(
        {
            "name": S.string(),
            "slug": S.string(),
            "date": S.date(),
            "timestamp": S.date(),
            "geometry": S.object(),
        },
        required=["name","geometry"]
    )
    processors = (
        document.SlugPropertyProcessor('name'),
    )
    specials = {
        "geometry": document.Geometry('point'),
        "date": document.DateTime(),
        "timestamp": document.Now()
    }



class SimpleDocuments(collection.Collection):
    "A collection of simple documents"
    document_class = SimpleDocument
    primary_key = "slug"
    indexes = ("timestamp", "name")

    @expose_method
    def arg_test(self, dict_arg: dict={}, int_arg: int=0, str_arg: str="", list_arg: list=[]) -> list:
        return [{"one": 1}, 0, 2]

    @expose_method
    def simple_none_return(self) -> None:
        return None

    @expose_method
    def simple_int_return(self) -> int:
        return 1

    @expose_method
    def simple_number_return(self) -> float:
        return 1.0

    @expose_method
    def simple_str_return(self) -> str:
        return "String"

    @expose_method
    def list_return(self) -> [str]:
        return ["0", "1", "2", "3"]

    @expose_method
    def dict_return(self) -> dict:
        return {
            'a': 0,
            'b': 1,
            'c': 2
        }

    @expose_method
    def operates_on_self(self) -> str:
        return self.title

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


class SimplePoints(collection.Collection):
    "A collection of simple points."

    document_class = SimplePoint
    primary_key = "slug"
    indexes = ("timestamp", "name", "geometry")


class ForeignKeyDocs(collection.Collection):
    "A collection of documents with foreign keys."

    document_class = ForeignKeyDoc
    primary_key = "slug"


class SimpleApp(application.Application):
    "A simple application containing all the collections defined and some methods."
    collections = (
        SimpleDocuments,
        SimplePoints,
        ForeignKeyDocs
    )

    definitions = {
        "appDef": S.color(pattern="#FF.*")
    }

    @expose_method
    def arg_test(self, dict_arg: dict={}, int_arg: int=0, str_arg: str="", list_arg: list=[]) -> list:
        return [{"one": 1}, 0, 2]

    @expose_method
    def simple_none_return(self) -> None:
        return None

    @expose_method
    def simple_int_return(self) -> int:
        return 1

    @expose_method
    def simple_number_return(self) -> float:
        return 1.0

    @expose_method
    def simple_str_return(self) -> str:
        return "String"

    @expose_method
    def list_return(self) -> [str]:
        return ["0", "1", "2", "3"]

    @expose_method
    def dict_return(self) -> dict:
        return {
            'a': 0,
            'b': 1,
            'c': 2
        }

    @expose_method
    def operates_on_self(self) -> str:
        return self.title

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


class DerivedCollection(SimpleDocuments):
    "A collection derived from SimpleDocuments"

    @expose_method
    def derived_method(self) -> None:
        pass


class DerivedApp(SimpleApp):
    "An application derived from SimpleApp that adds a definition and a collection."

    definitions = {
        "derivedDef": S.email(pattern=".*@gmail.com")
    }
    collections = (DerivedCollection,)

    @expose_method
    def derived_method(self) -> None:
        pass


class EmptyApp(application.Application):
    "An empty application"

#####
# APIs for testing authentication and authorization
#####


@authentication_required('write')
class AuthenticatedSuite(suite.Suite):
    "A simple API for testing"
    definitions = {
        "concreteSuiteDefn": {"type": "string", "pattern": "[0-9]+"}
    }

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


@authorization_required('write')
class AuthorizedSuite(suite.Suite):
    "A simple API for testing"
    definitions = {
        "concreteSuiteDefn": {"type": "string", "pattern": "[0-9]+"}
    }

    @authenticated_method
    @expose_method
    def authenticated_method(self) -> str:
        return "Successfully authenticated method"

    @authorized_method
    @expose_method
    def authorized_method(self) -> str:
        return "Accessed authorized method"


@authentication_required('read', 'write')
class AuthenticatedDocument(document.Document):
    "A simple document type"

    schema = S.object(
        {
            "name": S.string(title="Name", description="The name of the document"),
            "slug": S.string(),
        },
        required=["name",],
        propertyOrder=['name']
    )
    processors = (
        document.SlugPropertyProcessor('name'),
    )

    @expose_method
    def simple_none_return(self) -> None:
        return None


@authentication_required('read', 'write')
class AuthenticatedDocuments(collection.Collection):
    """A collection of simple documents"""

    document_class = SimpleDocument
    primary_key = "slug"
    indexes = ("timestamp", "name")

    @expose_method
    def simple_none_return(self) -> None:
        return None


@authentication_required('write')
class AuthenticatedApp(application.Application):
    """A simple application containing all the collections defined and some methods."""

    collections = (
        AuthenticatedDocuments,
        SimpleDocuments,  # this should still require authentication to write, because the app is authenticated
    )

    definitions = {
        "appDef": S.color(pattern="#FF.*")
    }

    @expose_method
    def simple_none_return(self) -> None:
        return None


@authorization_required('read','write')
class AuthorizedDocument(document.Document):
    """A simple document type"""

    schema = S.object(
        {
            "name": S.string(title="Name", description="The name of the document"),
            "slug": S.string(),
        },
        required=["name",],
        propertyOrder=['name']
    )
    processors = (
        document.SlugPropertyProcessor('name'),
    )

    @expose_method
    def simple_none_return(self) -> None:  # should be protected by authorization
        return None


@authorization_required('read','write')
class AuthorizedDocuments(collection.Collection):
    """A collection of simple documents."""

    document_class = SimpleDocument
    primary_key = "slug"
    indexes = ("timestamp", "name")

    @expose_method
    def simple_none_return(self) -> None:  # should be protected by authorization
        return None


@authorization_required('write')
class AuthorizedApp(application.Application):
    """A simple application containing all the collections defined and some methods."""

    collections = (
        AuthorizedDocuments,  # protects read, write, and delete
        SimpleDocuments  # Should be able to read the documents, but not write or delete them anonymously
    )

    definitions = {
        "appDef": S.color(pattern="#FF.*")
    }

    @expose_method
    def simple_none_return(self) -> None:
        return None
