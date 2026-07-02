import click
from bot.logging_config import setup_logger
from bot.validators import validate_order_inputs
from bot.orders import place_order

# Initialize the dual-handler logger immediately
logger = setup_logger()

@click.command()
@click.option('--symbol', required=True, help='Trading pair, e.g., BTCUSDT')
@click.option('--side', type=click.Choice(['BUY', 'SELL'], case_sensitive=False), required=True, help='Order side: BUY or SELL')
@click.option('--type', 'order_type', type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False), required=True, help='Order type: MARKET or LIMIT')
@click.option('--quantity', type=float, required=True, help='Amount of the asset to trade')
@click.option('--price', type=float, default=None, help='Price (Required if order type is LIMIT)')
def main(symbol, side, order_type, quantity, price):
    """
    Binance Futures Testnet Trading Bot CLI.
    Places Market and Limit orders on the USDT-M testnet.
    """
    click.secho("\n=========================================", fg='cyan')
    click.secho("      BINANCE FUTURES TESTNET BOT        ", fg='cyan', bold=True)
    click.secho("=========================================", fg='cyan')
    
    try:
        # 1. Validate inputs
        sym, sde, otype, qty, prc = validate_order_inputs(symbol, side, order_type, quantity, price)
        
        # 2. Execute order
        click.echo(f"Processing {sde} order for {qty} {sym} @ {otype}...")
        result = place_order(sym, sde, otype, qty, prc)
        
        # 3. Output summary to console
        if result:
            click.secho("\n✅ ORDER SUCCESSFUL!", fg='green', bold=True)
            click.echo(f"Order ID:     {result.get('orderId')}")
            click.echo(f"Status:       {result.get('status')}")
            click.echo(f"Executed Qty: {result.get('executedQty')}")
            click.echo(f"Avg Price:    {result.get('avgPrice', '0.0')}\n")
        else:
            click.secho("\n❌ ORDER FAILED.", fg='red', bold=True)
            click.echo("Please check 'trading_bot.log' for detailed error information.\n")

    except ValueError as ve:
        logger.error(f"Validation Error in CLI: {ve}")
        click.secho(f"\n⚠️ Input Validation Error: {ve}\n", fg='yellow')
    except Exception as e:
        logger.error(f"Unexpected CLI Error: {e}")
        click.secho(f"\n❌ An unexpected error occurred. Check trading_bot.log.\n", fg='red')

if __name__ == '__main__':
    main()