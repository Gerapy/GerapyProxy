# Gerapy Proxy

This is a package for supporting proxy with async mechanism in Scrapy, also this
package is a module in [Gerapy](https://github.com/Gerapy/Gerapy).

## Installation

```shell script
pip3 install gerapy-proxy
```

## Usage

If you have a proxy pool which can provide a random proxy for every request, you can use this package
to integrate proxy into your Scrapy/Gerapy Project.

For example, there is a [ProxyPool API](https://proxypool.scrape.center/random) which can return a random proxy 
per time, we can configure `GERAPY_PROXY_POOL_URL` setting provided by this package to enable proxy for every Scrapy Request.

To use this package, firstly install it by this command:

```shell script
pip3 install gerapy-proxy
```

Then enable it in DownloadMiddleware:

```python
DOWNLOADER_MIDDLEWARES = {
    'gerapy_proxy.middlewares.ProxyPoolMiddleware': 543,
}
```

and add proxy url in settings:

```shell script
GERAPY_PROXY_POOL_URL = 'https://proxypool.scrape.center/random'
```

This ProxyPool is configured based on this [ProxyPool](https://github.com/Python3WebSpider/ProxyPool) repo, you can
also build your own ProxyPool service.

Now, you've finished it.

The `ProxyPoolMiddleware` will firstly fetch a proxy from `GERAPY_PROXY_POOL_URL` and set `meta.proxy` attribute
to Scrapy Reqeust.

## Configuration

### Basic Auth

If your ProxyPool has Basic Auth, you can enable it by configuring these settings:

```shell script
GERAPY_PROXY_POOL_AUTH = True
GERAPY_PROXY_POOL_USERNAME = <username>
GERAPY_PROXY_POOL_PASSWORD = <password>
```

### Min Retry Times

If you want to enable Proxy depends on the retry times, you can configure this settings:

```shell script
GERAPY_PROXY_POOL_MIN_RETRY_TIMES = 2
```

Then proxy will only work if the retry times of Request greater or equal than 2.

### Random Enabled

If you want to enable the proxy randomly, you can configure the probability of enabling it:

```shell script
GERAPY_PROXY_POOL_RANDOM_ENABLE_RATE = 0.8
```

Then probability of enabling the proxy is 80%, if you configure it to 1, proxy will always be enabled.

### Fetch Timeout

You can also configure the max time of fetching proxy from ProxyPool:

```shell script
GERAPY_PROXY_POOL_TIMEOUT = 5
```

After configuring this, if Proxy Pool does not return result in 5s, proxy will not be used.

### ProxyPool Response Parser

Your ProxyPool may not return the same format as [this](https://github.com/Python3WebSpider/ProxyPool) in plain text,
you can also define a parser to extract proxy from your ProxyPool.

For example, if your ProxyPool return this for every request:

```json
{
  "host": "111.222.223.224",
  "port": 3128
}
```

You can define a method like:

```python
import json
def parse_result(text):
    data = json.loads(text)
    return f'{data.get("host")}:{data.get("port")}'
  
GERAPY_PROXY_EXTRACT_FUNC = parse_result 
```

Then you will get the proxy with correct format.

## Example

For more detail, please see [example](./example).

Also you can directly run with Docker:

```
docker run germey/gerapy-proxy-example
```

Outputs:

```shell script
2020-07-15 19:17:34 [scrapy.utils.log] INFO: Scrapy 2.2.0 started (bot: example)
2020-07-15 19:17:34 [scrapy.utils.log] INFO: Versions: lxml 4.3.3.0, libxml2 2.9.9, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 20.3.0, Python 3.7.7 (default, May  6 2020, 04:59:01) - [Clang 4.0.1 (tags/RELEASE_401/final)], pyOpenSSL 19.1.0 (OpenSSL 1.1.1d  10 Sep 2019), cryptography 2.8, Platform Darwin-19.4.0-x86_64-i386-64bit
2020-07-15 19:17:34 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.selectreactor.SelectReactor
2020-07-15 19:17:34 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'example',
 'CONCURRENT_REQUESTS': 3,
 'DOWNLOAD_TIMEOUT': 10,
 'NEWSPIDER_MODULE': 'example.spiders',
 'RETRY_TIMES': 10,
 'SPIDER_MODULES': ['example.spiders']}
2020-07-15 19:17:34 [scrapy.extensions.telnet] INFO: Telnet Password: 33299ca0ce64f215
2020-07-15 19:17:34 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage',
 'scrapy.extensions.logstats.LogStats']
2020-07-15 19:17:34 [asyncio] DEBUG: Using selector: KqueueSelector
2020-07-15 19:17:34 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'gerapy_proxy.middlewares.ProxyPoolMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2020-07-15 19:17:34 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2020-07-15 19:17:34 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2020-07-15 19:17:34 [scrapy.core.engine] INFO: Spider opened
2020-07-15 19:17:34 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2020-07-15 19:17:34 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2020-07-15 19:17:34 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:34 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: get proxy 113.124.94.189:9999
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: get proxy 84.53.238.49:23500
2020-07-15 19:17:35 [gerapy_proxy.middlewares] DEBUG: get proxy 217.150.77.31:53281
2020-07-15 19:17:40 [scrapy.core.engine] DEBUG: Crawled (200) <POST https://httpbin.org/delay/3> (referer: None)
2020-07-15 19:17:40 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:40 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:40 [example.spiders.httpbin] INFO: got request from 113.124.94.189 successfully, current page 1
2020-07-15 19:17:40 [gerapy_proxy.middlewares] DEBUG: get proxy 144.52.244.3:9999
2020-07-15 19:17:45 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <POST https://httpbin.org/delay/3> (failed 1 times): User timeout caused connection failure: Getting https://httpbin.org/delay/3 took longer than 10.0 seconds..
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:45 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <POST https://httpbin.org/delay/3> (failed 1 times): User timeout caused connection failure: Getting https://httpbin.org/delay/3 took longer than 10.0 seconds..
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: start to get proxy from proxy pool
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: get proxy using kwargs {'timeout': 5, 'url': 'https://proxypool.scrape.center/random'}
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: get proxy 1.20.101.149:44778
2020-07-15 19:17:45 [gerapy_proxy.middlewares] DEBUG: get proxy 105.27.116.46:56792
```