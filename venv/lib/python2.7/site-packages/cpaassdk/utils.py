import humps
import json
import re

def remove_empty_from_dict(d):
  if type(d) is dict:
    return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
  elif type(d) is list:
    return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
  else:
    return d

def compose_response(actual_response, formatted_response):
  return {
    'actual_response': actual_response,
    'formatted_response': formatted_response
  }

def response_converter(res):
  """
  convert response object from camelCase to snake_case
  """
  return humps.decamelize(res)

def check_if_error_response(res):
  """
  check for error status code
  """
  return True if (res.status_code >= 400) else False


def build_error_response(res):
  """
  Function to build error response.
  """
  if (res.status_code >= 400):

    res = response_converter(res.json())
    """
    sample error response
    {
      "requestError": {
        "serviceException": {
          "messageId": "SVC0005",
          "text": "Attribute %1 specified in message part %2 is a duplicate",
          "variables": [
            "john",
            "userName"
          ]
        }
      }
    }
    """
    if res:
      error_obj = find_messageid_containing_obj(res, 'message_id')
      if error_obj:
        return {
          'name' : error_obj['name'],
          'exception_id': error_obj['message_id'],
          'message': re.sub(r"%[0-9]", '{}', error_obj['text']).format(*error_obj['variables'])
        }
      else:
        return {
          'name': 'RequestError',
          'exception_id': '',
          'message': res['message']
        }

def find_messageid_containing_obj(obj, key, parent_key=''):
  if key in obj:
    obj['name'] = parent_key
    return obj
  for k, v in obj.items():
      if isinstance(v,dict):
        item = find_messageid_containing_obj(v, key, k)
        if item is not None:
          return item
    
def parse_response(res):
  """
  Function to remove the top most key from response.
  """
  response = res.json()
  return list(response.values())[0]

def id_from(url):
  chunks = url.split('/')

  return chunks[len(chunks) - 1]

def is_test_response(res):
  """
  check if the response is test_response or not
  """
  try:
    res = res.json()
    return True if '__for_test__' in res else False
  except Exception as error:
    return False
