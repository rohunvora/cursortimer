import csv
import random
import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "data")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "catalogue.csv")

# Helper --------------------------------------------------------------------

def slugify(name: str) -> str:
    """Turn an arbitrary string into a slug suitable for IDs."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return slug

# Manual seed items ----------------------------------------------------------

manual_items = {
    "Fashion": [
        ("Hermès Birkin Bag", 12000, 12000, None),
        ("Rolex Submariner Watch", 8000, 8000, None),
        ("Rolex Daytona Watch", 12000, 12000, None),
        ("Tiffany Diamond Necklace", 5000, 5000, None),
        ("Cartier Love Bracelet", 7000, 7000, None),
        ("Louis Vuitton Sneakers", 1000, None, None),
        ("Gucci Floral Dress", 3500, None, None),
        ("Prada Sunglasses", 300, None, None),
        ("Saint Laurent Leather Jacket", 4500, None, None),
        ("Celine Leather Belt", 450, None, None),
    ],
    "Transportation": [
        ("Tesla Model S", 90000, 90000, None),
        ("Mercedes-Benz G-Wagon", 140000, 140000, None),
        ("Porsche 911 Carrera", 130000, 130000, None),
        ("BMW X7", 78000, 78000, None),
        ("Audi R8", 160000, 160000, None),
        ("Lamborghini Huracán", 240000, 240000, None),
        ("Ferrari F8 Tributo", 280000, 280000, None),
        ("Private Jet Hour Charter", 6000, None, None),
        ("Luxury Yacht Charter Day", 12000, None, None),
        ("Range Rover Sport", 83000, 83000, None),
    ],
    "Housing": [
        ("Beverly Hills Mansion Down Payment", 500000, 500000, None),
        ("Miami Beach Condo Deposit", 300000, 300000, None),
        ("Complete Kitchen Renovation", 75000, 75000, None),
        ("Restoration Hardware Sofa", 8000, None, None),
        ("Viking Professional Range", 12000, None, None),
        ("Wolf Sub-Zero Refrigerator", 11000, None, None),
        ("Dyson V15 Detect Vacuum", 800, None, None),
        ("Casper King Mattress", 1800, None, None),
        ("Ride-On Lawn Mower", 3500, None, None),
        ("Nest Learning Thermostat", 250, None, None),
    ],
    "Tech": [
        ("Apple iPhone 15 Pro", 999, None, None),
        ("Apple MacBook Pro 16\"", 3499, None, None),
        ("Apple iPad Pro 13\"", 1299, None, None),
        ("Tesla Powerwall", 7500, 7500, None),
        ("Apple Watch Ultra", 799, 799, None),
        ("Meta Quest 3 VR Headset", 499, None, None),
        ("Sony PlayStation 5", 499, None, None),
        ("NVIDIA GeForce RTX 4090 GPU", 1599, None, None),
        ("Samsung 8K QLED TV 75\"", 4500, None, None),
        ("Sonos Arc Soundbar", 899, None, None),
    ],
    "Services": [
        ("Private School Tuition (Annual)", 35000, None, 35000),
        ("Live-in Nanny Annual Salary", 30000, None, 30000),
        ("Personal Trainer Annual", 12000, 12000, None),
        ("Private Chef Annual", 100000, 100000, None),
        ("Housekeeping Service (Weekly)", 5000, None, None),
        ("Luxury Vacation – Bali Week", 8000, None, None),
        ("First-Class Flight NY → Tokyo", 11000, 11000, None),
        ("VIP Concert Tickets", 1200, None, None),
        ("Golf Club Membership (Annual)", 15000, 15000, None),
        ("Engagement Ring", 15000, None, None),  # forced-add
        ("Wedding Event Spend", 25000, None, None),  # forced-add
    ],
}

# How many total rows per category
TARGET_PER_CATEGORY = 60

# Price ranges for auto-generated filler items (min, max)
price_ranges = {
    "Fashion": (50, 1500),
    "Transportation": (5000, 75000),
    "Housing": (500, 15000),
    "Tech": (50, 3000),
    "Services": (500, 20000),
}

random.seed(42)

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def build_rows():
    rows = []
    for category, items in manual_items.items():
        existing_count = len(items)
        filler_needed = TARGET_PER_CATEGORY - existing_count
        lo, hi = price_ranges[category]

        # Start with manual items
        for name, price, spouse_price, kid_price in items:
            slug = slugify(name)
            img_url = f"https://source.unsplash.com/featured/?{category.lower()}"  # placeholder
            rows.append({
                "id": slug,
                "name": name,
                "category": category,
                "price": price,
                "img_url": img_url,
                "spouse_variant_price": spouse_price if spouse_price is not None else "",
                "kid_variant_price": kid_price if kid_price is not None else "",
            })

        # Auto-generate filler
        for i in range(1, filler_needed + 1):
            name = f"{category} Item {i}"
            price = random.randint(lo, hi)
            slug = slugify(name)
            img_url = f"https://source.unsplash.com/featured/?{category.lower()}"
            rows.append({
                "id": slug,
                "name": name,
                "category": category,
                "price": price,
                "img_url": img_url,
                "spouse_variant_price": "",
                "kid_variant_price": "",
            })
    return rows


def write_csv(rows):
    ensure_dir(OUTPUT_DIR)
    headers = ["id", "name", "category", "price", "img_url", "spouse_variant_price", "kid_variant_price"]
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"✔ Catalogue written to {OUTPUT_PATH} ({len(rows)} rows)")


if __name__ == "__main__":
    write_csv(build_rows())