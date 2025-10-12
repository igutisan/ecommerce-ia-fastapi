import asyncio
import json
from typing_extensions import List
import uuid
from sqlalchemy.orm import Session
from app.dtos.create_product_dto import CreateProductDTO
from app.models.products import ProductModel
from app.services.genia_service import (
    generate_product_description,
    generate_image,
)
import re


async def create_product(
    product_dto: CreateProductDTO, seller_id: str, db: Session
) -> ProductModel:
    # Ejecutar las llamadas a la IA de forma concurrente
    try:
        description_task = asyncio.to_thread(
            generate_product_description, product_dto.name, product_dto.description
        )
        image_task = asyncio.to_thread(
            generate_image, product_dto.name, product_dto.description
        )

        results = await asyncio.gather(description_task, image_task)

        generated_description_str = results[0]
        image_url = results[1]

        # Parsear la descripción generada
        try:
            generated_data = json.loads(
                clean_llm_json_response(generated_description_str)
            )
            enhanced_description = generated_data.get("productDescription", "")
        except (json.JSONDecodeError, AttributeError):
            enhanced_description = "Could not generate enhanced description."

    except Exception as e:
        # Si la IA falla, continuamos con los datos originales pero registramos el error
        print(f"Error calling AI services: {e}")
        enhanced_description = "(AI enhancement failed)"
        image_url = None

    new_product = ProductModel(
        id=str(uuid.uuid4()),
        name=product_dto.name,
        description=enhanced_description,
        price=product_dto.price,
        image_url=image_url,
        seller_id=seller_id,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_products_by_seller(db: Session, seller_id: str) -> List[ProductModel]:
    return db.query(ProductModel).filter(ProductModel.seller_id == seller_id).all()


def clean_llm_json_response(raw_response: str) -> str:
    """
    Limpia una respuesta de un LLM que devuelve un JSON
    dentro de un bloque de código markdown (```json ... ```).
    """
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
    if match:
        return match.group(1)

    return raw_response.strip()
