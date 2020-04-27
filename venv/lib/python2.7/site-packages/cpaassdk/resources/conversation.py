from cpaassdk.utils import (
  compose_response,
  parse_response,
  build_error_response,
  id_from,
  is_test_response,
  response_converter,
  check_if_error_response)
from cpaassdk.resources.notification_channel import NotificationChannel

class Conversation:
  """
  CPaaS conversation.
  """
  def __init__(self, api):
    self.api = api
    self.types = {
      'SMS': 'sms'
    }

  @property
  def base_url(self):
    return '/cpaas/smsmessaging/v1/{}'.format(self.api.user_id)

  def create_message(self, params):
    """
      Send a new outbound message

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options.
        params['sender_address'] (:obj:`str`): Sender address information, basically the from address. E164 formatted DID number passed as a value, which is owned by the user. If the user wants to let CPaaS uses the default assigned DID number, this field can either has "default" value or the same value as the user_id.
        params['destination_address'] (:obj:`array[str]`):
        params['message'] (:obj:`str`): SMS text message
    """
    message_type = params.get('type')
    destination_address = params.get('destination_address')
    address =  destination_address if type(destination_address) is list else [ destination_address ]
    if (message_type == self.types['SMS']):
      options = {
        'body': {
          'outboundSMSMessageRequest': {
            'address': address,
            'clientCorrelator': self.api.config.client_correlator,
            'outboundSMSTextMessage': {
              'message': params.get('message')
            }
          }
        }
      }
      url = '{}/outbound/{}/requests'.format(self.base_url, params.get('sender_address'))

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
        'message': response['outboundSMSMessageRequest']['outboundSMSTextMessage']['message'],
        'sender_address': response['outboundSMSMessageRequest']['senderAddress'],
        'delivery_info': response['outboundSMSMessageRequest']['deliveryInfoList']['deliveryInfo']
      }
      return custom_response

  def get_messages(self, params):
    """
      Gets all messages.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['query'] (:obj:`dict`, optional): To hold all query related parameters.
        params['query']['name'] (:obj:`int`, optional): Performs search operation on first_name and last_name fields.
        params['query']['first_name'] (:obj:`int`, optional): Performs search for the first_name field of the directory items.
        params['query']['last_name'] (:obj:`int`, optional): Performs search for the last_name field of the directory items.
        params['query']['user_name'] (:obj:`int`, optional): Performs search for the user_name field of the directory items.
        params['query']['phone_number'] (:obj:`int`, optional): Performs search for the fields containing a phone number, like businessPhoneNumber, homePhoneNumber, mobile, pager, fax.
        params['query']['order'] (:obj:`int`, optional): Ordering the contact results based on the requested sortBy value, order query parameter should be accompanied by sortBy query parameter.
        params['query']['sort_by'] (:obj:`int`, optional): SortBy value is used to detect sorting the contact results based on which attribute. If order is not provided with that, ascending order is used.
        params['query']['max'] (:obj:`int`, optional): Maximum number of contact results that has been requested from CPaaS for this query.
        params['query']['next'] (:obj:`string`, optional): Pointer for the next chunk of contacts, should be gathered from the previous query results.

    """
    message_type = params.get('type')
    options = {}
    url = ''
    remote_address = params.get('remote_address')
    local_address = params.get('local_address')

    if (message_type == self.types['SMS']):
      options = {
        'query': params.get('query')
      }
      url = '{}/remoteAddresses'
      if (remote_address):
        url = '{}/{}'.format(url, remote_address)
      if (local_address):
        url = '{}/localAddresses/{}'.format(url, local_address)
      
      response = self.api.send_request(url, options)
      
      # check if response is test response.
      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)      
      
      # if not custom response remove the top level key and return
      return parse_response(response)

  def get_status(self, params):
    """
      Read a conversation message status

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj: `str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['message_id'] (:obj:`str`): Identification of the SMS message.
    """
    url = ''
    message_type = params.get('type')
    if (message_type == self.types['SMS']):
      url = '{}/remoteAddresses/{}/localAddresses/{}/messages/{}/status'.format(self.base_url, params.get('remote_address'), params.get('local_address'), params.get('message_id'))
      response = self.api.send_request(url, {})

      # check if response is test response.
      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)      
      
      # if not custom response remove the top level key and return
      return parse_response(response)

  def get_messages_in_thread(self, params):
    """
      Read all messages in a thread

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['query'] (:obj:`dict`, optional): To hold all query related parameters.
        params['query']['max'] (:obj:`int`, optional): Number of messages that is requested from CPaaS.
        params['query']['next'] (:obj:`string`, optional): Pointer for the next page to retrieve for the messages, provided by CPaaS in previous GET response.
        params['query']['new'] (:obj:`string`, optional): Filters the messages or threads having messages that are not received by the user yet
        params['query']['last_message_time'] (:obj:`int`, optional): Filters the messages or threads having messages that are sent/received after provided Epoch time
    """
    message_type = params.get('type')
    options = {}
    url = ''
    if (message_type == self.types['SMS']):
      options = {
        'query': params.get('query')
      }
      url = '{}/remoteAddresses/{}/localAddresses/{}/messages'.format(self.base_url, params.get('remote_address'), params.get('local_address'))
      
      response = self.api.send_request(url, options)

      # check if response is test response.
      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)      
      
      # if not custom response remove the top level key and return
      return parse_response(response)

  def delete_message(self, params):
    """
      Delete conversation message

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['remote_address'] (:obj:`str`): Remote address information while retrieving the SMS history, basically the destination telephone number that user exchanged SMS before. E164 formatted DID number passed as a value.
        params['local_address'] (:obj:`str`): Local address information while retrieving the SMS history, basically the source telephone number that user exchanged SMS before.
        params['message_id'] (:obj:`str`, optional): Identification of the SMS message. If messageId is not passed then the SMS thread is deleted with all messages.

    """
    message_type = params.get('type')
    url = ''
    if (message_type == self.types['SMS']):
      url = '{}/remoteAddresses/{}/localAddresses/{}'.format(self.base_url, params.get('remote_address'), params.get('local_address'))
      if params.get('message_id'):
        url = '{}/messages/{}'.format(url, params.get('message_id'))

      response = self.api.send_request(url, {}, 'delete')

      # check if response is test response.
      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response) 

      # if not custom response remove the top level key and return
      return parse_response(response)

  def get_subscriptions(self, params):
    """
      Read all active subscriptions.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options

    """
    url = ''
    message_type = params.get('type')

    if (message_type == this.types['SMS']):
      url = '{}/inbound/subscriptions'.format(self.base_url)

      response = self.api.send_request(url, {})

      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)

      # build custom_response.
      response = response.json()
      custom_response = []
      if (("subscriptionList" in response) and ("subscription" in response["subscriptionList"])):
        for subscription in response["subsctiptionList"]["subscription"]:
          custom_response.append({
            'notify_url': subscription['callbackReference']['notifyURL'],
            'destination_address': subscription['destinationAddress'],
            'subscription_id': id_from(subscription['resourceURL']) 
          })
        return custom_response

  def get_subscription(self, params):
    """
      Read active subscription

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['subscription_id'] (:obj:`str`): Resource ID of the subscription
  
    """
    url = ''
    message_type = params.get('type')

    if (message_type == self.types['SMS']):
      url = '{}/inbound/subscriptions/{}'.format(self.base_url, params.get('subscription_id'))
      
      response = self.api.send_request(url, {})

      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)

      # build custom_response.
      response = response.json()
      if ("subscription" in response):
        custom_response =  {
          'notify_url': response['subscription']['callbackReference']['notifyURL'],
          'destination_address': response['subcription']['destinationAddress'],
          'subscription_id': id_from(response['subscription']['resourceURL'])
        }
        return custom_response

  def subscribe(self, params):
    """
      Create a new subscription.

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['webhook_url'] (:obj:`str`): The webhook that has been acquired during SMS API subscription, which the incoming notifications supposed to be sent to.
        params['destination_address'] (:obj:`str`, optional): The address that incoming messages are received for this subscription. If does not exist, CPaaS uses the default assigned DID number to subscribe against. It is suggested to provide the intended E164 formatted DID number within this parameter.
   
    """
    message_type = params.get('type')

    if (message_type == self.types['SMS']):
      # create a notifyURL with webhookURL
      channel = NotificationChannel(self.api).create_channel(params)
      options = {
        'body': {
          'subscription': {
            'callbackReference': {
              'notifyURL': channel['channel_id']
            },
            'clientCorrelator': self.api.config.client_correlator,
            'destinationAddress': params.get('destination_address')
          }
        }
      }
      url = '{}/inbound/subscriptions'.format(self.base_url)

      response = self.api.send_request(url, options, 'post')

      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)

      # build custom_response.
      response = response.json()
      custom_response =  {
        'webhook_url': params.get('webhook_url'),
        'destination_address': response['subscription']['destinationAddress'],
        'subscription_id': id_from(response['subscription']['resourceURL'])
      }
      return custom_response

  def unsubscribe(self, params):
    """
      Unsubscription from conversation notification

      Args:
        params (dict): Single parameter to hold all options
        params['type'] (:obj:`str`): Type of conversation. Possible values - SMS. Check conversation.types for more options
        params['subscription_id'] (:obj:`str`): Resource ID of the subscription

    """
    message_type = params.get('type')
    if (message_type == self.types['SMS']):
      url = '{}/inbound/subscriptions/{}'.format(self.base_url, params.get('subscription_id'))

      response = self.api.send_request(url, {}, 'delete')

      if (is_test_response(response)):
        return response.json()
      # check if error_response.
      elif (check_if_error_response(response)):
        return build_error_response(response)

      # build custom_response.
      response = response.json()
      custom_response = {
        'subscription_id': params.get('subscription_id'),
        'success': True,
        'message': 'Unsubscribed from {} conversation notification'.format(params['type'])
      }
      return custom_response