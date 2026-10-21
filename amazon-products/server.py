
from collections import Counter
from dataclasses import dataclass
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pathlib import Path

from support.settings import load_settings
from sentence_transformers import SentenceTransformer
import torch

from support.search import (
    search_products as search_products_impl,
     SearchResult
)
from support.analysis import (
    AnalysisResult,
    ComparisonResult,
    analyze_product as analyze_product_impl,
    compare_products as compare_products_impl,
)
from support.data import (
    ProductRecord,
    ReviewRecord,
    catalog_text,
    ensure_data,
    load,
    prepare_review_texts,
)
from support.encoder import (
    combine_embeddings,
    encode_texts,
    load_model,
    summarize_reviews,
)



@dataclass
class ServerResources:
    model: SentenceTransformer
    product_embeddings: torch.Tensor
    product_ids: list[str]
    products: dict[str, ProductRecord]
    reviews: list[ReviewRecord]
    review_counts: dict[str, int]
    batch_size: int


def initialize_resources() -> ServerResources:
    base_dir = Path(__file__).resolve().parent

    settings = load_settings(base_dir / "config.json")
    dataset_dir = base_dir / "datasets"

    ensure_data(dataset_dir)
    reviews, products = load(dataset_dir)

    product_ids = list(products)
    catalog_texts = [
        catalog_text(products[product_id])
        for product_id in product_ids
    ]

    review_texts, _, review_product_ids = prepare_review_texts(reviews)

    model = load_model(settings)

    catalog_embeddings = encode_texts(
        model, catalog_texts, settings.batch_size
    )
    review_embeddings = encode_texts(
        model, review_texts, settings.batch_size
    )

    review_summaries = summarize_reviews(
        product_ids, review_product_ids, review_embeddings
    )

    product_embeddings = combine_embeddings(
        catalog_embeddings, review_summaries
    )

    counts = Counter(review["product_id"] for review in reviews)
    review_counts = dict(counts)

    return ServerResources(
        model=model,
        product_embeddings=product_embeddings,
        product_ids=product_ids,
        products=products,
        reviews=reviews,
        review_counts=review_counts,
        batch_size=settings.batch_size,
    )

mcp = MCPServer("Amazon reviews")
resources = initialize_resources()


@mcp.tool()
def search_products(query: str, top_k: int = 5) -> list[SearchResult]:
    try:
        return search_products_impl(
            query=query,
            model=resources.model,
            product_embeddings=resources.product_embeddings,
            product_ids=resources.product_ids,
            products=resources.products,
            review_counts=resources.review_counts,
            batch_size=resources.batch_size,
            top_k=top_k,
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
def analyze_product(product_id: str) -> AnalysisResult:
    try:
        return analyze_product_impl(
            product_id=product_id,
            reviews=resources.reviews,
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool()
def compare_products(product_ids: list[str]) -> ComparisonResult:
    try:
        return compare_products_impl(
            product_ids=product_ids,
            reviews=resources.reviews,
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )