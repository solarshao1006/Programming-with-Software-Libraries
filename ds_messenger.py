from collections import namedtuple
import socket
import json, time

"""
A customized exception. Raised when username already taken or invalid password entered in the login page.
"""
class InvalidLoginError(Exception):
  pass

"""
A customized exception. Raised when fail to connect to the server. 
"""
class ProtocolError(Exception):
  pass

"""
A customized exception. Raised when trying to connect to an invalid ip address (after OSError is raised). 
"""
class ServerNodeNameError(Exception):
  pass

"""
A customized exception. Raised when there is no internet connection (after OSError is raised).
"""
class NoInternetError(Exception):
  pass


DSConnection = namedtuple('DSConnection', ['socket', 'send', 'recv'])
"""
A class working as a protocol. 
This class supports connecting to the server, joining into the dsuserver with a valid username and password. 
When sending, receiving messages from the server, the method included in this class must be called. 
"""
class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None
    self._newuser = None

  """
  Connect to the dsuserver and port.
  """
  def connection(self, server:str, port:str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(port)
    
    try:
      client.connect((server, PORT))
      f_send = client.makefile('w')
      f_recv = client.makefile('r')

    except OSError as e:
      code = e.errno
      if code == 8:
        raise ServerNodeNameError('Wrong SERVER or wrong PORT.')
      elif code == 51:
        raise NoInternetError('No internet connection.') 
    except:
        raise ProtocolError('Invalid socket connection')
    else:
      self.connection = DSConnection(
          socket = client,
          send = f_send,
          recv = f_recv
      )
  
  """
  Join into the server using given username and password. 
  Will raise an exception if the server catches an error when joining. 
  """
  def join(self, username, password, user_token=None):
    self.username = username
    self.password = password
    self.user_token = user_token

    cmd = {"join": {"username": self.username, "password": self.password, "token": self.user_token}}
    self._write_command(cmd)
    try:
      response = self._read_command()

    except ConnectionResetError:
      raise ServerNodeNameError('Wrong SERVER or wrong PORT.')

    except OSError as e:
      code = e.errno
      if code == 8:
        raise ServerNodeNameError('Wrong SERVER or wrong PORT.')
      elif code == 51:
        raise NoInternetError('No internet connection.')
      else:
        raise Exception('Connection Error')

    except ConnectionRefusedError:
      raise Exception('Connection Refused.')

    except TypeError:
      raise Exception("Failed to connect! Check your server location.")
    
    response_type = self.extract_type(response)
    response_msg = self.extract_response_msg(response)
  
    if response_type.upper() == 'OK':
        self.user_token = response['response']['token']
        if response_msg == 'Welcome to the ICS 32 Distributed Social!':
          self._newuser = True
        else:
          self._newuser = False
    else:
      raise InvalidLoginError('Invalid password or username already taken')

  """
  Extract type from a json format response from the server.
  """
  def extract_type(self, json_msg):
    return json_msg['response']['type']

  """
  Extract response message from a json format response from the server.
  """
  def extract_response_msg(self, json_msg, request:bool=None):
    if request:
      return json_msg['response']['messages']
    else:
      return json_msg['response']['message']

  """
  Write command to the server.
  """
  def _write_command(self, cmd):
    try:
      json.dump(cmd, self.connection.send)
      self.connection.send.flush()
    except Exception as e:
      raise Exception(e)
    
  """
  Read the response message from the server. 
  """
  def _read_command(self):
    cmd = json.loads(self.connection.recv.readline()[:-1])
    return cmd


"""
A class that works similar as ds_client module. 
This class helps send message to a specific recipient, retrieve all messages and new messages received by the user.
"""
class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    self.msg_all = []
    self.msg_new = []

    self.server_connect = DirectMessage()
    self.server_connect.connection(self.dsuserver, '2021')
    
    self.server_connect.join(self.username, self.password, self.token)
    self.token = self.server_connect.user_token
    self._is_new = self.server_connect._newuser

  """
  Sends direct messages to another user.
  Returns true if message successfully sent, false if send failed.
  """
  def send(self, message:str, recipient:str) -> bool:
    self.server_connect.recipient = recipient
    self.server_connect.message = message

    timestamp = time.time()
    cmd = {"token": self.token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}
    self.server_connect._write_command(cmd)
    res = self.server_connect._read_command()
    try:
      type = self.server_connect.extract_type(res)
      return type.upper() == 'OK'
    except:
      return False
	
  """
  Returns a list of DirectMessage objects containing all new messages.
  """
  def retrieve_new(self) -> list:
    cmd = {"token":self.token, "directmessage": "new"}
    self.server_connect._write_command(cmd)
    self.msg_new = self.server_connect.extract_response_msg(self.server_connect._read_command(), request=True)
    return self.msg_new

  """
  Returns a list of DirectMessage objects containing all messages.
  """
  def retrieve_all(self) -> list:
    cmd = {"token":self.token, "directmessage": "all"}
    self.server_connect._write_command(cmd)
    self.msg_all = self.server_connect.extract_response_msg(self.server_connect._read_command(), request=True)
    return self.msg_all