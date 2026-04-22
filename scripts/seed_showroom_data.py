from __future__ import annotations

import shutil
import sqlite3
import ssl
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"
MEDIA_DIR = BASE_DIR / "media"
STATIC_IMAGE_DIR = BASE_DIR / "static" / "images"

TARGET_DIRS = ["logos", "products", "interior", "exterior", "carimag"]
STATIC_POOL = [
    STATIC_IMAGE_DIR / "l1.jpg",
    STATIC_IMAGE_DIR / "l2.jpg",
    STATIC_IMAGE_DIR / "l3.jpg",
]


COMPANIES = [
    {
        "name": "Ferrari",
        "ceo": "Benedetto Vigna",
        "est_year": 1939,
        "origin": "Italy",
        "logo_domain": "ferrari.com",
        "products": [
            {"name": "SF90 Stradale", "color": "Rosso Corsa", "seats": "2 Seater", "fuel": "Hybrid", "cc": 3990, "mileage": 18, "price": 75000000, "query": "ferrari,sf90,stradale"},
            {"name": "Purosangue", "color": "Blu Corsa", "seats": "4 Seater", "fuel": "Petrol", "cc": 6496, "mileage": 10, "price": 105000000, "query": "ferrari,purosangue"},
            {"name": "12Cilindri", "color": "Nero Daytona", "seats": "2 Seater", "fuel": "Petrol", "cc": 6496, "mileage": 9, "price": 88000000, "query": "ferrari,12cilindri"},
        ],
    },
    {
        "name": "Lamborghini",
        "ceo": "Stephan Winkelmann",
        "est_year": 1963,
        "origin": "Italy",
        "logo_domain": "lamborghini.com",
        "products": [
            {"name": "Revuelto", "color": "Verde Mantis", "seats": "2 Seater", "fuel": "Hybrid", "cc": 6498, "mileage": 11, "price": 89000000, "query": "lamborghini,revuelto"},
            {"name": "Urus SE", "color": "Giallo Auge", "seats": "5 Seater", "fuel": "Hybrid", "cc": 3996, "mileage": 12, "price": 52000000, "query": "lamborghini,urus"},
            {"name": "Temerario", "color": "Arancio Xanto", "seats": "2 Seater", "fuel": "Hybrid", "cc": 3995, "mileage": 13, "price": 76000000, "query": "lamborghini,temerario"},
        ],
    },
    {
        "name": "Bentley",
        "ceo": "Frank-Steffen Walliser",
        "est_year": 1919,
        "origin": "United Kingdom",
        "logo_domain": "bentleymotors.com",
        "products": [
            {"name": "Continental GT", "color": "British Racing Green", "seats": "4 Seater", "fuel": "Hybrid", "cc": 3996, "mileage": 12, "price": 59000000, "query": "bentley,continental,gt"},
            {"name": "Flying Spur", "color": "Onyx", "seats": "5 Seater", "fuel": "Hybrid", "cc": 3996, "mileage": 11, "price": 61000000, "query": "bentley,flying,spur"},
            {"name": "Bentayga EWB", "color": "Moonbeam", "seats": "5 Seater", "fuel": "Petrol", "cc": 3996, "mileage": 10, "price": 68000000, "query": "bentley,bentayga"},
        ],
    },
    {
        "name": "Rolls-Royce",
        "ceo": "Chris Brownridge",
        "est_year": 1906,
        "origin": "United Kingdom",
        "logo_domain": "rolls-roycemotorcars.com",
        "products": [
            {"name": "Phantom", "color": "Arctic White", "seats": "5 Seater", "fuel": "Petrol", "cc": 6749, "mileage": 9, "price": 110000000, "query": "rolls,royce,phantom"},
            {"name": "Spectre", "color": "Tempest Grey", "seats": "4 Seater", "fuel": "EV", "cc": 0, "mileage": 530, "price": 98000000, "query": "rolls,royce,spectre"},
            {"name": "Cullinan", "color": "Midnight Sapphire", "seats": "5 Seater", "fuel": "Petrol", "cc": 6749, "mileage": 8, "price": 92000000, "query": "rolls,royce,cullinan"},
        ],
    },
    {
        "name": "McLaren",
        "ceo": "Nick Collins",
        "est_year": 1963,
        "origin": "United Kingdom",
        "logo_domain": "cars.mclaren.com",
        "products": [
            {"name": "750S", "color": "McLaren Orange", "seats": "2 Seater", "fuel": "Petrol", "cc": 3994, "mileage": 12, "price": 62000000, "query": "mclaren,750s"},
            {"name": "Artura", "color": "Flux Green", "seats": "2 Seater", "fuel": "Hybrid", "cc": 2993, "mileage": 17, "price": 51000000, "query": "mclaren,artura"},
            {"name": "GTS", "color": "Storm Grey", "seats": "2 Seater", "fuel": "Petrol", "cc": 3994, "mileage": 13, "price": 47000000, "query": "mclaren,gts"},
        ],
    },
]


RENTAL_CARS = [
    {"car_name": "Hyundai Creta", "company": "Hyundai", "color": "Titan Grey", "fuel_type": "petrol", "seat_capacity": "5 seater", "transmission_type": "automated", "total_km_driven": 12450, "amminities": "Sunroof, wireless charging, camera", "bootspace": 433, "rating": 5, "milage": 17, "query": "hyundai,creta,suv"},
    {"car_name": "Honda Elevate", "company": "Honda", "color": "Platinum White", "fuel_type": "petrol", "seat_capacity": "5 seater", "transmission_type": "manual", "total_km_driven": 14320, "amminities": "Cruise control, camera, airbags", "bootspace": 458, "rating": 4, "milage": 16, "query": "honda,elevate,suv"},
    {"car_name": "Kia Seltos", "company": "Kia", "color": "Intense Red", "fuel_type": "petrol", "seat_capacity": "5 seater", "transmission_type": "automated", "total_km_driven": 10230, "amminities": "Ventilated seats, display, camera", "bootspace": 433, "rating": 5, "milage": 17, "query": "kia,seltos,suv"},
    {"car_name": "Toyota Hyryder", "company": "Toyota", "color": "Cafe White", "fuel_type": "petrol", "seat_capacity": "5 seater", "transmission_type": "manual", "total_km_driven": 11870, "amminities": "Heads-up display, camera, auto AC", "bootspace": 373, "rating": 4, "milage": 20, "query": "toyota,hyryder,suv"},
    {"car_name": "MG Hector", "company": "MG", "color": "Starry Black", "fuel_type": "diesel", "seat_capacity": "5 seater", "transmission_type": "manual", "total_km_driven": 16540, "amminities": "Panoramic roof, ADAS, display", "bootspace": 587, "rating": 4, "milage": 15, "query": "mg,hector,suv"},
    {"car_name": "Toyota Innova Hycross", "company": "Toyota", "color": "Silver Metallic", "fuel_type": "petrol", "seat_capacity": "7 seater", "transmission_type": "automated", "total_km_driven": 21430, "amminities": "Ottoman seats, ADAS, camera", "bootspace": 300, "rating": 5, "milage": 19, "query": "toyota,innova,hycross"},
    {"car_name": "Mahindra Scorpio-N", "company": "Mahindra", "color": "Deep Forest", "fuel_type": "diesel", "seat_capacity": "7 seater", "transmission_type": "manual", "total_km_driven": 18660, "amminities": "4X4, sunroof, dual-zone AC", "bootspace": 460, "rating": 4, "milage": 15, "query": "mahindra,scorpio,suv"},
    {"car_name": "Tata Safari", "company": "Tata", "color": "Cosmic Gold", "fuel_type": "diesel", "seat_capacity": "7 seater", "transmission_type": "automated", "total_km_driven": 17220, "amminities": "Panoramic roof, ADAS, JBL audio", "bootspace": 420, "rating": 5, "milage": 14, "query": "tata,safari,suv"},
    {"car_name": "Kia Carens", "company": "Kia", "color": "Aurora Black", "fuel_type": "petrol", "seat_capacity": "7 seater", "transmission_type": "manual", "total_km_driven": 13470, "amminities": "Rear AC vents, display, camera", "bootspace": 216, "rating": 4, "milage": 16, "query": "kia,carens,mpv"},
    {"car_name": "Toyota Fortuner", "company": "Toyota", "color": "Pearl White", "fuel_type": "diesel", "seat_capacity": "7 seater", "transmission_type": "automated", "total_km_driven": 19890, "amminities": "Leather seats, camera, hill assist", "bootspace": 296, "rating": 5, "milage": 14, "query": "toyota,fortuner,suv"},
]


def reset_media_dirs() -> None:
    for folder in TARGET_DIRS:
        target = MEDIA_DIR / folder
        target.mkdir(parents=True, exist_ok=True)
        for child in target.iterdir():
            if child.is_file():
                child.unlink()


def safe_name(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def write_logo_svg(destination: Path, brand_name: str) -> str:
    initials = "".join(part[0] for part in brand_name.split()[:2]).upper()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
<rect width="800" height="500" rx="36" fill="#08111f"/>
<rect x="24" y="24" width="752" height="452" rx="28" fill="#0f1c31" stroke="#ff9f1c" stroke-width="4"/>
<text x="400" y="210" text-anchor="middle" fill="#ffbf69" font-size="120" font-family="Arial, sans-serif" font-weight="700">{initials}</text>
<text x="400" y="305" text-anchor="middle" fill="#f4f7fb" font-size="44" font-family="Arial, sans-serif" font-weight="700">{brand_name}</text>
<text x="400" y="360" text-anchor="middle" fill="#7bdff6" font-size="22" font-family="Arial, sans-serif" letter-spacing="6">LUXURY PERFORMANCE</text>
</svg>"""
    destination.write_text(svg, encoding="utf-8")
    return destination.as_posix()


def download_file(url: str, destination: Path) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    context = ssl._create_unverified_context()
    with urlopen(request, timeout=45, context=context) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return destination.as_posix()


def lorem_url(query: str, lock_number: int) -> str:
    return f"https://loremflickr.com/1200/800/{quote(query)}?lock={lock_number}"


def clearbit_url(domain: str) -> str:
    return f"https://logo.clearbit.com/{domain}"


def copy_static_variant(destination: Path, index: int) -> str:
    source = STATIC_POOL[index % len(STATIC_POOL)]
    shutil.copyfile(source, destination)
    return destination.as_posix()


def seed_database() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("DELETE FROM carsapp_productexteriorimgs")
    cur.execute("DELETE FROM carsapp_productinteriorimgs")
    cur.execute("DELETE FROM carsapp_products")
    cur.execute("DELETE FROM carsapp_company")
    cur.execute("DELETE FROM rentalapp_cars")

    image_counter = 10

    for company in COMPANIES:
        logo_filename = f"logos/{safe_name(company['name'])}.svg"
        logo_path = MEDIA_DIR / logo_filename
        try:
            download_file(clearbit_url(company["logo_domain"]), logo_path)
        except Exception:
            write_logo_svg(logo_path, company["name"])

        cur.execute(
            """
            INSERT INTO carsapp_company (name, ceo, est_year, origin, logo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company["name"], company["ceo"], company["est_year"], company["origin"], logo_filename),
        )
        company_id = cur.lastrowid

        for product in company["products"]:
            product_slug = safe_name(product["name"])
            product_image = f"products/{product_slug}.jpg"
            interior_image = f"interior/{product_slug}_interior.jpg"
            exterior_image = f"exterior/{product_slug}_exterior.jpg"

            try:
                download_file(lorem_url(product["query"] + ",car", image_counter), MEDIA_DIR / product_image)
                download_file(lorem_url(product["query"] + ",interior", image_counter + 200), MEDIA_DIR / interior_image)
                download_file(lorem_url(product["query"] + ",exterior", image_counter + 400), MEDIA_DIR / exterior_image)
            except Exception:
                copy_static_variant(MEDIA_DIR / product_image, image_counter)
                copy_static_variant(MEDIA_DIR / interior_image, image_counter + 1)
                copy_static_variant(MEDIA_DIR / exterior_image, image_counter + 2)

            cur.execute(
                """
                INSERT INTO carsapp_products
                (product_name, color, seat_Capacity, fuel_type, cc, mileage, product_img, price, company_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    product["name"],
                    product["color"],
                    product["seats"],
                    product["fuel"],
                    product["cc"],
                    product["mileage"],
                    product_image,
                    product["price"],
                    company_id,
                ),
            )
            product_id = cur.lastrowid
            cur.execute(
                "INSERT INTO carsapp_productinteriorimgs (interior, product_id) VALUES (?, ?)",
                (interior_image, product_id),
            )
            cur.execute(
                "INSERT INTO carsapp_productexteriorimgs (exterior, product_id) VALUES (?, ?)",
                (exterior_image, product_id),
            )
            image_counter += 1

    rental_lock = 1000
    for car in RENTAL_CARS:
        image_path = f"carimag/{safe_name(car['car_name'])}.jpg"
        try:
            download_file(lorem_url(car["query"], rental_lock), MEDIA_DIR / image_path)
        except Exception:
            copy_static_variant(MEDIA_DIR / image_path, rental_lock)

        cur.execute(
            """
            INSERT INTO rentalapp_cars
            (car_name, Company, color, fuel_type, seat_capacity, transmission_type, total_km_driven,
             amminities, bootspace, rating, car_img, milage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                car["car_name"],
                car["company"],
                car["color"],
                car["fuel_type"],
                car["seat_capacity"],
                car["transmission_type"],
                car["total_km_driven"],
                car["amminities"],
                car["bootspace"],
                car["rating"],
                image_path,
                car["milage"],
            ),
        )
        rental_lock += 1

    conn.commit()
    conn.close()


def main() -> None:
    reset_media_dirs()
    seed_database()
    print("Seeded 5 luxury brands, 15 products, and 10 rental cars.")


if __name__ == "__main__":
    main()
