import paypalrestsdk
import logging

logging.basicConfig(level=logging.INFO)

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox o live
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})