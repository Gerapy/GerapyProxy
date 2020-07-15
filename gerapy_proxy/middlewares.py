import random
import logging
import aiohttp
from gerapy_proxy.exceptions import DefinitionError
from gerapy_proxy.settings import *
import asyncio
import sys
import twisted.internet
from twisted.internet.asyncioreactor import AsyncioSelectorReactor

reactor = AsyncioSelectorReactor(asyncio.get_event_loop())

# install AsyncioSelectorReactor
twisted.internet.reactor = reactor
sys.modules['twisted.internet.reactor'] = reactor

logger = logging.getLogger(__name__)


class ProxyPoolMiddleware(object):
    """
    using proxy pool as proxy
    """
    
    def _extract_response(self, text):
        """
        extract response content
        :param text:
        :return:
        """
        settings = self.settings
        extract_func = settings.get('GERAPY_PROXY_EXTRACT_FUNC', GERAPY_PROXY_EXTRACT_FUNC)
        return extract_func(text)
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        init crawler using settings
        :param crawler:
        :return:
        """
        settings = crawler.settings
        cls.settings = settings
        # proxy pool settings
        cls.proxy_pool_url = settings.get('GERAPY_PROXY_POOL_URL', GERAPY_PROXY_POOL_URL)
        cls.proxy_pool_auth = settings.get('GERAPY_PROXY_POOL_AUTH', GERAPY_PROXY_POOL_AUTH)
        cls.proxy_pool_username = settings.get('GERAPY_PROXY_POOL_USERNAME', GERAPY_PROXY_POOL_USERNAME)
        cls.proxy_pool_password = settings.get('GERAPY_PROXY_POOL_PASSWORD', GERAPY_PROXY_POOL_PASSWORD)
        cls.proxy_pool_min_retry_times = settings.get('GERAPY_PROXY_POOL_MIN_RETRY_TIMES',
                                                      GERAPY_PROXY_POOL_MIN_RETRY_TIMES)
        cls.proxy_pool_random_enable_rate = settings.get('GERAPY_PROXY_POOL_RANDOM_ENABLE_RATE',
                                                         GERAPY_PROXY_POOL_RANDOM_ENABLE_RATE)
        cls.proxy_pool_timeout = settings.get('GERAPY_PROXY_POOL_TIMEOUT', GERAPY_PROXY_POOL_TIMEOUT)
        return cls()
    
    async def get_proxy(self):
        """
        get proxy from proxy pool
        :return:
        """
        logger.debug('start to get proxy from proxy pool')
        kwargs = {}
        if self.proxy_pool_auth:
            kwargs['auth'] = aiohttp.BasicAuth(login=self.proxy_pool_username, password=self.proxy_pool_password)
        if self.proxy_pool_timeout:
            kwargs['timeout'] = self.proxy_pool_timeout
        
        if not self.proxy_pool_url:
            raise DefinitionError('You must define `GERAPY_PROXY_POOL_URL` in settings')
        
        kwargs['url'] = self.proxy_pool_url
        logger.debug('get proxy using kwargs %s', kwargs)
        
        try:
            async with aiohttp.ClientSession() as client:
                response = await client.get(**kwargs)
                if response.status == 200:
                    proxy = self._extract_response(await response.text())
                    logger.debug('get proxy %s', proxy)
                    return proxy
        except:
            logger.error('error occurred while fetching proxy', exc_info=True)
    
    async def process_request(self, request, spider):
        """
        use proxy pool to process request
        :param request:
        :param spider:
        :return:
        """
        # judge if need proxy using retry times
        if self.proxy_pool_min_retry_times:
            retry_times = request.meta.get('retry_times')
            logger.debug('current retry times %s', retry_times)
            if not retry_times or retry_times < self.proxy_pool_min_retry_times:
                logger.debug('retry times less than proxy_pool_min_retry_times')
                request.meta['proxy'] = None
                return None
        
        # check random rate
        if self.proxy_pool_random_enable_rate < 1:
            random_number = random.random()
            logger.debug('get random number %s', random_number)
            if random_number > self.proxy_pool_random_enable_rate:
                logger.debug('random number lager than proxy_pool_random_enable_rate, skip')
                request.meta['proxy'] = None
                return None
        
        proxy = await self.get_proxy()
        
        # skip invalid
        if not proxy:
            logger.error('can not get proxy from proxy pool')
            return
        
        request.meta['proxy'] = f'http://{proxy}'


class ProxyTunnelMiddleware(object):
    """
    using proxy tunnel as proxy
    """
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        # proxy pool settings
        # proxy tunnel settings
        cls.proxy_tunnel_url = settings.get('GERAPY_PROXY_TUNNEL_URL')
        cls.proxy_tunnel_auth = settings.get('GERAPY_PROXY_TUNNEL_AUTH')
        cls.proxy_tunnel_username = settings.get('GERAPY_PROXY_TUNNEL_USERNAME')
        cls.proxy_tunnel_password = settings.get('GERAPY_PROXY_TUNNEL_PASSWORD')
        cls.proxy_tunnel_min_retry_times = settings.get('GERAPY_PROXY_TUNNEL_MIN_RETRY_TIMES')
        cls.proxy_tunnel_random_enable_rate = settings.get('GERAPY_PROXY_TUNNEL_RANDOM_ENABLE_RATE')
        
        return cls()
