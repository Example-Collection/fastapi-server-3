import logging
import time

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.otel import tracer


def handle_request_from_server_2(item_price: float):
    with tracer.start_as_current_span("server-3-handle-request-from-server-2"):
        logging.warning(f"[SERVER-3] Checking if item_price is greater than or equal to 0.0.")
        time.sleep(0.6)
        if item_price < 0.0:
            logging.warning(f"[SERVER-3] Item price was lower than 0.0. (item_price: {item_price})")
            raise HTTPException(status_code=400, detail="Item price should be greater than or equal to 0.0.")
        else:
            logging.warning(f"[SERVER-3] Item price was greater than or equal to 0.0. (item_price: {item_price})")
            return JSONResponse(content=jsonable_encoder({"message": "Item price is valid."}), status_code=200)
