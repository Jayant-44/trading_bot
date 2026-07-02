import os
from dotenv import load_dotenv
from binance.client import Client
import logging

# Load environment variables
load_dotenv()

# Grab the central logger
logger = logging.getLogger("trading_bot")

def get_binance_client() -> Client:
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        error_msg = "API keys are missing! Check your .env file."
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        # Initialize client specifically for Testnet
        client = Client(api_key, api_secret, testnet=True)
        
        # Binance Futures endpoints require explicit routing
        client.API_URL = 'https://testnet.binancefuture.com/fapi'
        
        logger.info("Binance client initialized successfully for Testnet.")
        return client
        
    except Exception as e:
        logger.error(f"Failed to initialize Binance client: {e}")
        raise