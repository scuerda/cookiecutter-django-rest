# pylint: disable=no-member, no-self-use
from typing import Set
import abc
from {{cookeicutter.app_name}}.domain import model
from djangoproject.{{cookiecutter.app_shortname}} import models as django_models


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[model.Batch]

    def add(self, batch: model.Batch):
        self.seen.add(batch)

    def get(self, reference) -> model.Batch:
        p = self._get(reference)
        if p:
            self.seen.add(p)
        return p

    @abc.abstractmethod
    def _get(self, reference):
        raise NotImplementedError



class DjangoBaseRepository(AbstractRepository):

    def add(self, batch):
        raise NotImplementedError

    def update(self, batch):
        raise NotImplementedError

    def _get(self, reference):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError
