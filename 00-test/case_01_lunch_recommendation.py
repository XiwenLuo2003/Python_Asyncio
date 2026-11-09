# -*- coding: utf-8 -*-
"""午餐推荐：查门店信息，过滤，再按评分和距离选出前三家。

运行：python case_01_lunch_recommendation.py
只使用本地模拟接口，不需要联网，也不需要安装第三方库。
"""

import asyncio
import time
from typing import Dict, List


# 门店接口中的价格是字符串，单位为元；距离单位为公里。
SHOP_DATA = {
    101: {
        "name": "巷口盖饭", "rating": 4.6, "distance_km": 0.5,
        "price": "28.0", "is_open": True,
    },
    102: {
        "name": "园区面馆", "rating": 4.4, "distance_km": 0.3,
        "price": "25.0", "is_open": True,
    },
    103: {
        "name": "轻食小馆", "rating": 4.8, "distance_km": 4.0,
        "price": "38.0", "is_open": True,
    },
    104: {
        "name": "铁板牛排", "rating": 5.0, "distance_km": 0.2,
        "price": "68.0", "is_open": True,
    },
    105: {
        "name": "老街砂锅", "rating": 4.9, "distance_km": 0.4,
        "price": "32.0", "is_open": False,
    },
    106: {
        "name": "家常小炒", "rating": 4.5, "distance_km": 1.0,
        "price": "35.0", "is_open": True,
    },
}
REQUEST_DELAY = 2.00
BUDGET = 40.0
TOP_K = 3


async def fetch_shop(shop_id: int) -> Dict:
    """模拟查询一家门店。

    每次查询耗时 REQUEST_DELAY 秒，返回一份独立的门店字典。
    批量查询允许同时发起，不存在限流或前后依赖。
    """
    # time.sleep(REQUEST_DELAY)
    await asyncio.sleep(REQUEST_DELAY)
    shop = SHOP_DATA[shop_id].copy()
    shop["shop_id"] = shop_id
    return shop


async def fetch_shops(shop_ids: List[int]) -> List[Dict]:
    """取回所有门店，返回顺序与 shop_ids 一致。

    六家门店应同时查询，不能把总耗时累加成六次接口耗时。
    """
    started = time.perf_counter()
    tasks = []
    for shop_id in shop_ids:
        tasks.append(asyncio.create_task(fetch_shop(shop_id)))

    # shops = []
    # for task in tasks:
    #     shop = task.result()
    #     # shop = asyncio.create_task(task)
    #     shops.append(shop)
    shops = list(await asyncio.gather(*tasks))

    elapsed = time.perf_counter() - started
    print(f"门店查询：{len(shops)} 家，耗时 {elapsed:.2f}s")
    return shops


def filter_shops(shops: List[Dict], budget: float) -> List[Dict]:
    """保留营业中且人均价格不超过预算的门店。

    接口字段不变；返回记录的 price 转为浮点数供后续展示使用。
    不修改传入的门店记录。
    """
    candidates = []
    for shop in shops:
        # price = shop["price"]
        price = float(shop["price"])
        over_budget = price > budget
        closed = not shop["is_open"]
        # if closed and over_budget:
        if closed or over_budget:
            continue

        candidate = shop.copy()
        candidate["price"] = price
        candidates.append(candidate)

    return candidates


def score_shops(shops: List[Dict]) -> List[Dict]:
    """计算推荐得分，不改变候选门店的输入顺序。

    满分为 1。评分越高越好，距离越近越好：
        score = 0.7 * (rating / 5) + 0.3 * (1 - distance_km / 5)
    本题所有门店距离都在 0 到 5 公里之间。
    """
    scored = []
    # row = {}
    for shop in shops:
        rating_score = shop["rating"] / 5.0
        distance_score = shop["distance_km"] / 5.0
        # score = 0.7 * rating_score + 0.3 * distance_score
        score = 0.7 * rating_score + 0.3 * (1-distance_score)

        # row.update(shop)
        row = shop.copy()
        row["score"] = score
        scored.append(row)

    return scored


def select_top(shops: List[Dict], k: int) -> List[Dict]:
    """按得分降序返回前 k 家，不足 k 家时全部返回。

    同分时保留输入顺序。排序和截取不应修改传入的列表。
    """
    # ranked = shops.copy()
    # ranked = ranked.sort(key=lambda shop: shop["score"], reverse=True)
    ranked = sorted(shops, key=lambda shop: shop["score"], reverse=True)
    return ranked[:k]


def print_report(shops: List[Dict], candidates: List[Dict],
                 recommendations: List[Dict]) -> None:
    """输出筛选过程、最终推荐和推荐门店的平均人均价格。"""
    print(f"\n预算：{BUDGET:.0f} 元；需要推荐：{TOP_K} 家")
    print(f"查询 {len(shops)} 家，筛选后 {len(candidates)} 家")
    print("筛选后的门店：")
    for shop in candidates:
        status = "营业" if shop["is_open"] else "停业"
        print(
            f"  {shop['shop_id']} {shop['name']} | {status} | "
            f"{shop['price']:.0f} 元 | {shop['distance_km']:.1f} km"
        )

    print("\n推荐结果：")
    for rank, shop in enumerate(recommendations, start=1):
        print(
            f"  {rank}. {shop['shop_id']} {shop['name']} | "
            f"评分 {shop['rating']:.1f} | 距离 {shop['distance_km']:.1f} km | "
            f"推荐分 {shop['score']:.3f}"
        )

    # average_price = (sum(recommendations) / len(recommendations)
    #                  if recommendations else 0.0)
    average_price = (sum(shop["price"] for shop in recommendations)
                     / len(recommendations)
                     if recommendations else 0.0)
    print(f"\n推荐门店平均人均价格：{average_price:.2f} 元")


async def main() -> None:
    """运行一次午餐推荐。

    输入来自同一片商圈，用户预算为 40 元，需要三条推荐。
    依次执行查询、筛选、打分、排序，输出每个阶段的结果。
    """
    shop_ids = list(SHOP_DATA)
    shops = await fetch_shops(shop_ids)
    candidates = filter_shops(shops, budget=BUDGET)
    scored = score_shops(candidates)
    recommendations = select_top(scored, k=TOP_K)

    print_report(shops, candidates, recommendations)


if __name__ == "__main__":
    asyncio.run(main())
