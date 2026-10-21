import torch

from support.data import ProductRecord
from typing import TypedDict
from sentence_transformers import SentenceTransformer
from support.encoder import encode_query


class SearchResult(TypedDict):
    product_id: str
    title: str
    similarity: float
    review_count: int


def validate_search(query: str, top_k: int) -> None:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    if type(top_k) is not int or not 1 <= top_k <= 20:
        raise ValueError("top_k must be an integer between 1 and 20")


def search_top_k(
    product_embeddings: torch.Tensor,
    query_embedding: torch.Tensor,
    top_k: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    similarities = product_embeddings @ query_embedding

    k = min(top_k, product_embeddings.shape[0])

    top_values, top_indices = torch.topk(
        similarities,
        k=k,
        largest=True,
        sorted=True,
    )

    return top_values, top_indices


def build_search_results(
    top_values: torch.Tensor,
    top_indices: torch.Tensor,
    product_ids: list[str],
    products: dict[str, ProductRecord],
    review_counts: dict[str, int],
) -> list[SearchResult]:
    results: list[SearchResult] = []

    for value, index in zip(top_values.tolist(), top_indices.tolist()):
        product_id = product_ids[index]
        product = products[product_id]

        results.append({
            "product_id": product_id,
            "title": product["title"],
            "similarity": float(value),
            "review_count": review_counts[product_id],
        })

    return results

def search_products(
    query: str,
    model: SentenceTransformer,
    product_embeddings: torch.Tensor,
    product_ids: list[str],
    products: dict[str, ProductRecord],
    review_counts: dict[str, int],
    batch_size: int,
    top_k: int = 5,
) -> list[SearchResult]:
    validate_search(query, top_k)

    query_embedding = encode_query(model, query, batch_size)

    top_values, top_indices = search_top_k(
        product_embeddings,
        query_embedding,
        top_k,
    )

    results = build_search_results(
        top_values,
        top_indices,
        product_ids,
        products,
        review_counts,
    )

    return results