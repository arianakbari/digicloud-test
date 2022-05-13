import punq

from domain.boundaries.input.feed_service_abstract import FeedServiceAbstract
from domain.boundaries.input.feed_item_service_abstract import FeedItemServiceAbstract
from domain.boundaries.output.feed_parser_abstract import FeedParserAbstract
from domain.boundaries.output.feed_repository_abstract import FeedRepositoryAbstract
from domain.boundaries.output.feed_item_repository_abstract import (
    FeedItemRepositoryAbstract,
)


from domain.services.feed_service import FeedService
from domain.services.feed_item_service import FeedItemService
from adapters.feed_parser import FeedParser
from webapp.feed.services.feed_repository import FeedRepository
from webapp.feed.services.feed_item_repository import FeedItemRepository


container = punq.Container()

container.register(FeedServiceAbstract, FeedService)
container.register(FeedItemServiceAbstract, FeedItemService)
container.register(FeedParserAbstract, FeedParser)
container.register(FeedRepositoryAbstract, FeedRepository)
container.register(FeedItemRepositoryAbstract, FeedItemRepository)

# based on https://github.com/django/django/blob/main/django/views/generic/base.py
def get_ioc_view(cls, **initkwargs):
    def view(request, *args, **kwargs):
        self = container.instantiate(cls, **initkwargs)
        self.setup(request, *args, **kwargs)
        return self.dispatch(request, *args, **kwargs)

    view.view_class = cls
    view.view_initkwargs = initkwargs
    view.__doc__ = cls.__doc__
    view.__module__ = cls.__module__
    view.__annotations__ = cls.dispatch.__annotations__
    view.__dict__.update(cls.dispatch.__dict__)

    return view
