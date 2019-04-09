import socket

if (socket.getfqdn() == 'mealscount.com') or (socket.getfqdn() == "ca.mealscount.com"):
    from .prod import *
else:
    from .dev import *

# gets the fully qualified domain name
# like ca.mealscount.com and associates that with rule for California
# modules can exist for each state.
try:
    if socket.getfqdn().split('.')[-3] == 'ca':
        from . import ca
    elif socket.getfqdn().split('.')[-3] == 'tx':
        from . import tx
    elif socket.getfqdn().split('.')[-3] == 'ny':
        from . import ny
except:
    pass
__all__ = ['django_config', 'funding_rules', 'us_regions', 'model_version_info']
