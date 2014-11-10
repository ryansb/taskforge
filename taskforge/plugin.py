import abc
import logging
import six


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):
    log = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        # TODO: do something with option parameters
        pass

    @abc.abstractmethod
    def process_task(self, task):
        """Receive a single task in taskw format and return the task after
        processing.

        If there are no changes, None should be returned
        """
        raise NotImplementedError


class DummyPlugin(PluginBase):
    def process_task(self, task):
        self.log.info("HEY, I'm loaded!")
