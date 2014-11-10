import abc
import logging
import pkg_resources
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
    def __init__(self, *args, **kwargs):
        super(DummyPlugin, self).__init__(*args, **kwargs)
        self.opts = kwargs

    def pre_run(self):
        self.log.debug("prerun for DummyPlugin")

    def post_run(self):
        self.log.debug("postrun for DummyPlugin")

    def process_task(self, task):
        self.log.info("Hey, dummy plugin loaded with options: "
                      "{}".format(self.opts))


def load_plugin(plugin_conf):
    """Takes a full plugin configuration dict

    Returns an instance of the plugin loaded and initialized with the plugin
    options
    """
    ep = pkg_resources.EntryPoint.parse(
        "{name} = {entrypoint}".format(**plugin_conf),
        pkg_resources.get_distribution(plugin_conf.get('module', 'taskforge'))
    )

    return ep.load()(**plugin_conf.get('options', {}))
