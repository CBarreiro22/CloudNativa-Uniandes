from abc import abstractmethod, ABC


class BaseCommand(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Please implement in subclass")

    @abstractmethod
    def post(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Please implement in subclass")
