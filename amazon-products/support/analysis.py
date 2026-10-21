
import numpy as np
from typing import TypedDict

from support.data import ReviewRecord


class AnalysisResult(TypedDict):
    product_id: str
    review_count: int
    rating_counts: dict[int, int]
    rating_proportions: dict[int, float]
    mean: float | None
    median: float | None

class ComparisonResult(TypedDict):
    products: list[AnalysisResult]
    mean_differences: list[float | None]

def analyze_product(
    product_id: str,
    reviews: list[ReviewRecord],
) -> AnalysisResult:
    if not product_id.strip():
        raise ValueError("Product ID cannot be empty")

    ratings = [
        review["rating"]
        for review in reviews
        if review["product_id"] == product_id
    ]

    review_count = len(ratings)

    rating_counts = {
        star: ratings.count(star)
        for star in range(1, 6)
    }

    rating_proportions = {
        star: count / review_count if review_count else 0.0
        for star, count in rating_counts.items()
    }

    if review_count:
        mean = float(np.mean(ratings))
        median = float(np.median(ratings))
    else:
        mean = None
        median = None

    return {
        "product_id": product_id,
        "review_count": review_count,
        "rating_counts": rating_counts,
        "rating_proportions": rating_proportions,
        "mean": mean,
        "median": median,
    }

def compare_products(
    product_ids: list[str],
    reviews: list[ReviewRecord],
) -> ComparisonResult:
    if len(product_ids) < 2:
        raise ValueError("At least two products are required")

    if any(not product_id.strip() for product_id in product_ids):
        raise ValueError("Product IDs cannot be empty")

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Product IDs must be distinct")

    results = [
        analyze_product(product_id, reviews)
        for product_id in product_ids
    ]

    reference_mean = results[0]["mean"]

    mean_differences: list[float | None] = []

    for product in results:
        current_mean = product["mean"]

        if reference_mean is None or current_mean is None:
            mean_differences.append(None)
        else:
            mean_differences.append(current_mean - reference_mean)

    return {
        "products": results,
        "mean_differences": mean_differences,
    }