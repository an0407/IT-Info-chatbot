import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r"^[6-9]\d{9}$", phone))


def is_valid_date(date_str: str) -> bool:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date >= datetime.now().date()  
    except:
        return False
    
def is_valid_company(company : str) -> bool:
    if company.lower() in ['tcs', 'cognizant', 'zoho', 'amazon', 'hcl', 'ibm', 'dxc', 'mahindra', 'tech mahindra', 'techmahindra', 'capgemini',
                           'hexaware', 'oracle', 'virtusa', 'atos', 'dell', 'mphasis', 'freshworks', 'hps', 'kissflow', 'infosys', 'wipro',
                           'lnt', 'l&t', 'ltts', 'lt', 'thoughtworks', 'altimetrik', 'photon', 'intellectdesign', 'ltimidntree', 'walmart',
                           'trimble', '3iinfotech', '3i-infotech', 'ideas2it', 'incedoinc', 'chargebee', 'xoriant', 'logitech', 'aziro', 'borngroup'
                           'hindujatech', 'inspirisys', 'birlasoft', 'spiderindia', 'way2smile', 'teamtweaks', 'pyramidionsolutions', 'happyfox',
                           'fourkites', 'contus', 'ramco', 'softsuave']:
        return True
    else:
        return False

def is_valid_time(time: str) -> bool:
    try:
        datetime.strptime(time, "%H:%M")
        return True
    except:
        return False


valid_car_models = [
    "bmw m4",
    "bmw x1",
    "bmw x3",
    "bmw x5",
    "bmw i7",
    "bmw m8",
    "bmw 5 series",
    "bmw 7 series",
    "bmw z4"
]

def is_valid_car_model(model: str) -> bool:
    return model.lower() in [m.lower() for m in valid_car_models]