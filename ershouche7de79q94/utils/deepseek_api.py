# coding:utf-8
import os
import json
import requests

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


def build_analyze_prompt(car_info: dict, prediction: dict, market_stats: dict) -> str:
    return (
        "你是一位资深的二手车估价分析师。请根据以下信息，对这辆二手车的预测价格进行专业分析。\n"
        "要求：使用中文，条理清晰，分点说明，语气专业但易懂。不要使用 # 号标题，用**加粗**代替标题。\n\n"
        f"【车辆信息】\n"
        f"- 品牌：{car_info.get('brand', '未知')}\n"
        f"- 型号：{car_info.get('model1', '未知')}\n"
        f"- 年份：{car_info.get('vehicleage', '未知')}\n"
        f"- 行驶里程：{car_info.get('kilometer', '未知')} 万公里\n"
        f"- 所在城市：{car_info.get('city', '未知')}\n\n"
        f"【预测结果】\n"
        f"- 预测低价：{prediction.get('low', '—')} 万元\n"
        f"- 预测中价：{prediction.get('mid', '—')} 万元\n"
        f"- 预测高价：{prediction.get('high', '—')} 万元\n\n"
        f"【市场参考数据】\n"
        f"- 同品牌车辆数量：{market_stats.get('brand_count', '—')} 辆\n"
        f"- 同品牌均价：{market_stats.get('brand_avg_price', '—')} 万元\n"
        f"- 同城市车辆数量：{market_stats.get('city_count', '—')} 辆\n"
        f"- 同城市均价：{market_stats.get('city_avg_price', '—')} 万元\n"
        f"- 全平台均价：{market_stats.get('total_avg_price', '—')} 万元\n\n"
        "请从以下几个方面进行分析：\n"
        "1. **价格定位**：该预测价格在同类车中处于什么水平（偏高/合理/偏低）\n"
        "2. **价格区间解读**：预测区间的宽窄说明了什么（市场稳定性）\n"
        "3. **关键影响因素**：车龄、里程、品牌、城市分别对价格有什么影响\n"
        "4. **买卖建议**：给出买家和卖家各自的建议\n"
    )


def stream_analyze(car_info: dict, prediction: dict, market_stats: dict):
    prompt = build_analyze_prompt(car_info, prediction, market_stats)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    resp = requests.post(
        DEEPSEEK_API_URL, headers=headers, json=payload, stream=True, timeout=60
    )
    resp.raise_for_status()

    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        data_str = line[6:]
        if data_str.strip() == "[DONE]":
            break
        try:
            chunk = json.loads(data_str)
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content", "")
            if content:
                yield content
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
