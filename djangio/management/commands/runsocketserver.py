import eventlet
import re
import socketio
from django.apps.config import AppConfig
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from djangio import listener

naiveip_re = re.compile(r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""", re.X)


class Command(BaseCommand):
    help = 'Runs a SocketIO server'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.default_port = 9000

    def add_arguments(self, parser):
        parser.add_argument('addrport', nargs='?',
                            help='Optional port number, or ipaddr:port')

    def handle(self, *args, **options):
        if not options.get('addrport'):
            self.addr = ''
            self.port = self.default_port
        else:
            m = re.match(naiveip_re, options['addrport'])
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % options['addrport'])
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)

        self._load_all_socket_listeners()
        app = socketio.Middleware(listener)
        eventlet.wsgi.server(eventlet.listen((self.addr, self.port)), app)

    def _load_all_socket_listeners(self):
        for app in settings.INSTALLED_APPS:
            app_config = AppConfig.create(app)
            try:
                from app_config.module import sockets
            except ImportError:
                pass
