from mcp.server.fastmcp import FastMCP
from urllib.parse import quote
import httpx
import pinyin
mcp = FastMCP("free-api-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """查询城市天气"""
    # key = os.getenv("OWM_KEY", "demo")
    key = "6ab957b52e6f9710ee017ce4115c8933"
    # 根据中文城市名称转为：城市的拼音
    city = pinyin.get(city, format="strip")

    # 使用 OpenWeatherMap 查询天气
    url = f"https://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={key}&lang=zh_cn"
    try:
        r = httpx.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return f"{city}：{data['weather'][0]['description']}，{data['main']['temp']-273.15:.1f}℃"
    except httpx.HTTPStatusError as e:          # 有 response 的异常
        return f"{city} 天气获取失败：{e} | 原始返回：{e.response.text}"
    except Exception as e:                      # 其他网络/解析异常
        return f"{city} 天气获取失败：{e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
