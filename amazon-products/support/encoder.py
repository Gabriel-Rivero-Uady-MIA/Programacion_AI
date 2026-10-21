import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

from support.settings import Settings


def load_model(settings: Settings) -> SentenceTransformer:
    model = SentenceTransformer(
        settings.model_name,
        device=settings.device,
    )
    return model


def encode_texts(
    model: SentenceTransformer,
    texts: list[str],
    batch_size: int,
) -> torch.Tensor:
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    return embeddings


def summarize_reviews(
    product_ids: list[str],
    review_product_ids: list[str],
    review_embeddings: torch.Tensor,
) -> torch.Tensor:
    summaries: list[torch.Tensor] = []

    for product_id in product_ids:
        positions = [
            i
            for i, review_product_id in enumerate(review_product_ids)
            if review_product_id == product_id
        ]

        if not positions:
            raise ValueError(f"No review embeddings for product {product_id}")

        product_vectors = review_embeddings[positions]
        average = product_vectors.mean(dim=0)
        normalized_average = F.normalize(average, dim=0)

        summaries.append(normalized_average)

    return torch.stack(summaries)


def combine_embeddings(
    catalog_embeddings: torch.Tensor,
    review_summaries: torch.Tensor,
) -> torch.Tensor:
    combined = 0.5 * catalog_embeddings + 0.5 * review_summaries
    return F.normalize(combined, dim=1)


def encode_query(
    model: SentenceTransformer,
    query: str,
    batch_size: int,
) -> torch.Tensor:
    query_vectors = encode_texts(model, [query], batch_size)
    return query_vectors[0]
