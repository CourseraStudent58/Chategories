from types import ModuleType

from .api import Api
from .config import Config
from . import resources

class Client:
  """
    Configure the SDK with client_id and client_secret.

    Example::

        client = Client({
          'client_id': '<private project key>',
          'client_secret': '<private project secret>',
          'base_url': '<base url>'
        })

    Args:
      params (dict): Single parameter to hold all options
      params['client_id'] (:obj:`str`): 	Private project key.
      params['client_secret'] (:obj:`str`): Private project secret.
      params['base_url'] (:obj:`str`): JSON url of the server to be used.
  """
  def __init__(self, credentials):
    config = Config(credentials)

    self.setup(config)

  def setup(self, config):
    api = Api(config)

    for namespace, Klass in resources.mappings.items():
      setattr(self, namespace, Klass(api))
