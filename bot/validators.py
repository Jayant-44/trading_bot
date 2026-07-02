def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    # Normalize inputs to uppercase strings to avoid case-sensitivity errors
    symbol = str(symbol).upper()
    side = str(side).upper()
    order_type = str(order_type).upper()

    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be strictly 'BUY' or 'SELL'.")
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError("Order type must be strictly 'MARKET' or 'LIMIT'.")
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number.")
    except ValueError:
        raise ValueError(f"Invalid quantity provided: {quantity}")

    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("A price must be provided for LIMIT orders.")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be a positive number.")
        except ValueError:
            raise ValueError(f"Invalid price provided: {price}")
    else:
        # Ignore price for MARKET orders
        price = None 

    return symbol, side, order_type, quantity, price