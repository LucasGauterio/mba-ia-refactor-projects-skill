from datetime import datetime
import re

def format_date(date_obj):
    if date_obj:
        return str(date_obj)
    return None

def calculate_percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)

def validate_email(email):
    if re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
        return True
    return False

def sanitize_string(s):
    if s:
        return s.strip()
    return s

def generate_id():
    import uuid
    return str(uuid.uuid4())

def log_action(action, details=None):
    timestamp = datetime.utcnow()
    print(f"[{timestamp}] ACTION: {action}")
    if details:
        print(f"  DETAILS: {details}")

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except:
        try:
            return datetime.strptime(date_string, '%d/%m/%Y')
        except:
            return None

def is_valid_color(color):
    if color and len(color) == 7 and color[0] == '#':
        return True
    return False
