BASE_URL = 'https://oauth-cpaas.att.com'

class Config:
  def __init__(self, config = {}):
    self.client_id = config.get('client_id')
    self.client_secret = config.get('client_secret')
    self.base_url = config.get('base_url') or BASE_URL
    self.client_correlator = '{}-python'.format(config.get('client_id'))

    if self.client_id is None or self.client_secret is None:
      raise Exception('client id and client secret are manditory')