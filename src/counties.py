import re

KENYA_COUNTIES = [
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa",
    "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu",
    "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga",
    "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans Nzoia",
    "Uasin Gishu", "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia",
    "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga",
    "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii",
    "Nyamira", "Nairobi",
]

COUNTY_ALIASES = {
    "Muranga": "Murang'a",
    "Murang’a": "Murang'a",
    "Nairobi City": "Nairobi",
    "Elgeyo Marakwet": "Elgeyo-Marakwet",
    "Taita Taveta": "Taita-Taveta",
    "Tharaka Nithi": "Tharaka-Nithi",
    "Homabay": "Homa Bay",
}


def normalize_county(name):
    if name is None:
        return None
    cleaned = str(name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    cleaned = COUNTY_ALIASES.get(cleaned, cleaned)
    return cleaned
