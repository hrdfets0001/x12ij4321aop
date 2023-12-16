import requests
import ssl
from urllib3 import poolmanager

class TLSAdapter(requests.adapters.HTTPAdapter):
    """Represents a TLS adapter used to connect to a remote HTTP server.

    Args:
        requests (HTTPAdapter): The parent class representing the HTTP adapter.
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        """Initializes the pool manager.

        Args:
            connections (any): The connection pool information.
            maxsize (int): The maximal amount of bytes.
            block (bool, optional): Determines if the data should be sent in blocks. Defaults to False.
        """
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)