import re
import json

with open("raw.txt", "r") as file:
    text = file.read()

#Extract all prices
prices = re.findall(r"\d+\.\d{2}", text)
prices = [float(p) for p in prices]

#Extract product names
products = re.findall(r"([A-Za-z ]+)\s+\d+\.\d{2}", text)

# Remove "Total" from products if captured
products = [p.strip() for p in products if p.strip().lower() != "total"]

#Calculate total
calculated_total = sum(prices[:-1])

#Extract date
date = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", text)
date = date.group(1) if date else None

#Extract time
time = re.search(r"Time:\s*(\d{2}:\d{2})", text)
time = time.group(1) if time else None

#Extract payment method
payment = re.search(r"Payment Method:\s*(.+)", text)
payment = payment.group(1) if payment else None

#Create structured output
receipt_data = {
    "date": date,
    "time": time,
    "products": products,
    "prices": prices[:-1],
    "calculated_total": round(calculated_total, 2),
    "receipt_total": prices[-1] if prices else None,
    "payment_method": payment
}

print(json.dumps(receipt_data, indent=4))