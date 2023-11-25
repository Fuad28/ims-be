

def generate_serial_number(serial_number):
    """Generate serial numbers"""

    total_length = 7
    prefix= "#"
    
    padded_serial_number = str(serial_number).zfill(total_length - len(prefix))
    generated_serial_number = f"{prefix}{padded_serial_number}"
    
    return generated_serial_number