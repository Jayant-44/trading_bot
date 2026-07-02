import logging
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_binance_client

# Grab the central logger
logger = logging.getLogger("trading_bot")

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    logger.info(f"--- PREPARING ORDER REQUEST ---")
    logger.info(f"Details: {side} {quantity} {symbol} @ {order_type} (Price: {price if price else 'Market'})")
    
    try:
        client = get_binance_client()
        
        # Build the exact payload required by Binance Futures
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        if order_type == 'LIMIT':
            # Binance requires 'timeInForce' for Limit orders (GTC = Good Till Canceled)
            params['timeInForce'] = 'GTC' 
            params['price'] = price
        
        logger.info(f"Sending payload to Binance: {params}")
        
        # Execute the futures order
        response = client.futures_create_order(**params)
        
        # Parse output requirements: orderId, status, executedQty, avgPrice
        order_id = response.get('orderId')
        status = response.get('status')
        executed_qty = response.get('executedQty')
        avg_price = response.get('avgPrice', '0.0')
        
        logger.info(f"--- ORDER SUCCESS ---")
        logger.info(f"Order ID: {order_id}")
        logger.info(f"Status: {status}")
        logger.info(f"Executed Qty: {executed_qty}")
        logger.info(f"Avg Price: {avg_price}")
        
        return response

    except BinanceAPIException as e:
        # Catches exact errors from Binance (e.g., "Margin is insufficient")
        logger.error(f"--- BINANCE API ERROR ---")
        logger.error(f"Status Code: {e.status_code}")
        logger.error(f"Message: {e.message}")
    except BinanceRequestException as e:
        # Catches network drops or connection timeouts
        logger.error(f"--- NETWORK ERROR ---")
        logger.error(str(e))
    except Exception as e:
        # Catches anything else unexpectedly broken in Python
        logger.error(f"--- UNEXPECTED SYSTEM ERROR ---")
        logger.error(str(e))
    
    return None