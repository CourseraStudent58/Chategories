from cpaassdk.utils import (
  compose_response,
  parse_response,
  id_from,
  is_test_response,
  response_converter,
  check_if_error_response)

class NotificationChannel:
  def __init__(self, api):
    self.api = api
    self.types = {
      'SMS': 'sms'
    }

  @property
  def base_url(self):
    return '/cpaas/notificationchannel/v1/{}'.format(self.api.user_id)

  def channels(self, params):
    """
    Retrive the list of activae notification channels.

    Args:

    Returns a json.
    """
    url = '{}/channels'.format(self.base_url)
    response = self.api.send_request(url)

  def channel(self, params):
    """
      Retrieve a list of active notification channels

      Args:
        params (dict): Single parameter to hold all options
        params['channed_id'] (:obj:`str`): The channelId provided by CPaaS after creation. 

      Return:
        Returns a json
    """
    url = '{}/channels/{}'.format(self.base_url, params.get('channel_id'))
    response = self.api.send_request(url)

  def create_channel(self, params):
    """
    Creates a new notification channel, webhook type.
    
    Args:
      params (dict): Single parameter to hold all options
      params['webhook_url'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
      
    Returns:
      Returns a json.
    """
    url = '{}/channels'.format(self.base_url)
    options = {
      'body': {
        'notificationChannel': {
          'channelData': {
            'x-webhookURL': params.get('webhook_url')
          },
          'channelType': 'webhooks',
          'clientCorrelator': self.api.config.client_correlator
        }
      }
    }

    response = self.api.send_request(url, options, 'post')

    # check if response is test response.
    if (is_test_response(response)):
      return response.json()
    # check if error_response.
    elif (check_if_error_response(response)):
      return build_error_response(response)

    # build custom_response.
    response = response.json()
    custom_response = {
      'channel_id': response['notificationChannel']['callbackURL'],
      'webhook_url': response['notificationChannel']['channelData']['x-webhookURL'],
      'channel_type': response['notificationChannel']['channelType']
    }  
    return custom_response
    

    
    




      

  

    