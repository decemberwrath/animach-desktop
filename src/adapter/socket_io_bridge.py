# -*- coding: utf-8 -*-
import requests
from socket import error as SocketError
from websocket import SSLError, WebSocketTimeoutException
from socketIO_client import SocketIO, WebsocketTransport, TimeoutError, ConnectionError
from socketIO_client.parsers import parse_packet_text
from src.adapter.event_reactor import getEventReactor
import config


def patch_recv_packet(self):
    try:
        packet_text = self._connection.recv()
    except WebSocketTimeoutException as e:
        raise TimeoutError('recv timed out (%s)' % e)
    except SSLError as e:
        raise ConnectionError('recv disconnected by SSL (%s)' % e)
    except WebSocketConnectionClosedException as e:
        raise ConnectionError('recv disconnected (%s)' % e)
    except SocketError as e:
        raise ConnectionError('recv disconnected (%s)' % e)
    if not isinstance(packet_text, six.binary_type):
        packet_text = six.u(packet_text)
    engineIO_packet_type, engineIO_packet_data = parse_packet_text(
        packet_text)
    yield engineIO_packet_type, engineIO_packet_data

WebsocketTransport.recv_packet = patch_recv_packet


class SocketIOConnection:
    def __init__(self):
        self.host = config.DOMAIN
        self.channel = config.CHANNEL
        self.channelpw = config.CHANNELPASS
        self.name = config.LOGIN
        self.password = config.PASSWORD
        self.socket_port = self.__get_socket_port()

    def __get_socket_port(self):
        # response format:
        # {
        #    'servers': [
        #        {'url': 'https://blabla.com:5555', 'secure': True},
        #        {'url': 'http://blabla.com:6666', 'secure': False}
        #    ]
        # }
        url = 'http://%s/socketconfig/%s.json' % (self.host, self.channel)
        servers = requests.get(url).json()['servers']
        for server in servers:
            if server['secure'] is not False:
                continue
            server_url = server['url']
            port = server_url.split(':')[-1]
            return int(port)

    def __init_channel_callbacks(self):
        self.socket_io.emit('initChannelCallbacks')

    def __login(self):
        self.socket_io.emit('login', {
            'name': self.name,
            'pw': self.password
        })

    def __join_channel(self):
        self.socket_io.emit('joinChannel', {
            'name': self.channel,
            'pw': self.channelpw
        })

    def send_message(self, message):
        msg = { 'msg': message, 'meta': {} }
        self.socket_io.emit('chatMsg', msg)

    def connect(self, app):
        event_reactor_cls = getEventReactor(app)
        self.socket_io = SocketIO(self.host, self.socket_port, event_reactor_cls)
        self.__init_channel_callbacks()
        self.__join_channel()
        self.__login()
        self.socket_io .wait()

socket_io_connection = SocketIOConnection()
