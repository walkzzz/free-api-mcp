from mcp.server.fastmcp import FastMCP
from urllib.parse import quote
import httpx, socket
import pinyin
import requests
from urllib.parse import quote
mcp = FastMCP("free-api-server")
def resolve(host: str) -> str:
    try:
        socket.inet_aton(host)
        return host
    except OSError:
        return socket.gethostbyname(host)

ENDPOINTS = [
    "https://ip-api.com/json/{}?fields=status,message,country,regionName,city,isp&lang=zh",
    "https://freeipapi.com/api/json/{}"
]
# ----------------------------------------------------------
# 1. IP 归属地查询
# ----------------------------------------------------------
@mcp.tool()
def ip_location(ip_or_domain: str) -> str:
    target = resolve(ip_or_domain.strip())

    for tpl in ENDPOINTS:
        try:
            url = tpl.format(quote(target))
            r = httpx.get(url, timeout=3)
            r.raise_for_status()
            data = r.json()

            # ip-api.com
            if data.get("status") == "success":
                return (
                    f"{ip_or_domain}（{target}）归属地："
                    f"{data['country']} {data['regionName']} {data['city']}｜{data['isp']}"
                )

            # freeipapi.com
            if "countryName" in data:
                return (
                    f"{ip_or_domain}（{target}）归属地："
                    f"{data['countryName']} {data['regionName']} {data['cityName']}｜{data['isp']}"
                )
        except Exception:
            continue

    return "所有线路均不可用，请稍后再试"



# ----------------------------------------------------------
# 3. 今日国内新闻热点 TopN
# ----------------------------------------------------------
@mcp.tool()
def get_china_news(api_key='3a7809d74c124c4ba0433760efbcd8bc', limit=5):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'cn',  # 中国新闻
        'apiKey': api_key,
        'pageSize': limit
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            news_list = []
            for i, article in enumerate(articles, 1):
                title = article.get('title', '无标题')
                source = article.get('source', {}).get('name', '未知来源')
                news_list.append(f"{i}. {title}（{source}）")
            return '\n'.join(news_list)
        else:
            return f"获取新闻失败: {data.get('message', '未知错误')}"
    except Exception as e:
        return f"新闻获取失败：{e}"

# ----------------------------------------------------------
# 把原来的天气工具也放进来，方便一次性跑通
# ----------------------------------------------------------
@mcp.tool()
def get_weather(city: str) -> str:
    """查询城市天气"""
    key = "6ab957b52e6f9710ee017ce4115c8933"
    city = pinyin.get(city, format="strip")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={key}&lang=zh_cn"
    try:
        r = httpx.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return f"{city}：{data['weather'][0]['description']}，{data['main']['temp']-273.15:.1f}℃"
    except httpx.HTTPStatusError as e:
        return f"{city} 天气获取失败：{e} | 原始返回：{e.response.text}"
    except Exception as e:
        return f"{city} 天气获取失败：{e}"

# ----------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
