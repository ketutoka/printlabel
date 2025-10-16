import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def generate_label_with_qr(sender_name: str, shipping_code: str, label_id: int) -> str:
    """
    Generate label image with QR code for thermal printer 58mm width
    Returns the path to the generated image
    """
    
    # Create labels directory if it doesn't exist
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # Thermal printer 58mm ≈ 203 pixels at 203 DPI
    label_width = 203
    label_height = 320  # Increased for better spacing
    
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Use larger fonts for thermal printer readability
        font_large = ImageFont.truetype("arial.ttf", 16)    # Increased from 12
        font_medium = ImageFont.truetype("arial.ttf", 14)   # Increased from 10
        font_small = ImageFont.truetype("arial.ttf", 12)    # Increased from 8
        font_tiny = ImageFont.truetype("arial.ttf", 10)     # For very small text
    except:
        # Fallback fonts with better spacing
        try:
            font_large = ImageFont.truetype("calibri.ttf", 16)
            font_medium = ImageFont.truetype("calibri.ttf", 14)
            font_small = ImageFont.truetype("calibri.ttf", 12)
            font_tiny = ImageFont.truetype("calibri.ttf", 10)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
    
    # Generate QR code with better error correction for thermal
    qr = qrcode.QRCode(
        version=2,  # Slightly larger QR for better readability
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Better error correction
        box_size=3,  # Larger box size for thermal printer
        border=2,
    )
    qr.add_data(shipping_code)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_size = 85  # 3 cm ≈ 85 pixels for 58mm thermal printer
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Layout design - start directly with sender info
    y_offset = 12  # Top margin
    
    # Sender info with better spacing - centered format
    sender_label_text = "PENGIRIM:"
    sender_label_bbox = draw.textbbox((0, 0), sender_label_text, font=font_small)
    sender_label_width = sender_label_bbox[2] - sender_label_bbox[0]
    sender_label_x = (label_width - sender_label_width) // 2
    draw.text((sender_label_x, y_offset), sender_label_text, fill="black", font=font_small)
    y_offset += 18  # More spacing between label and content
    
    # Center sender name - always 2 lines format
    if len(sender_name) > 18:  # If name is too long, split intelligently
        words = sender_name.split()
        if len(words) >= 2:
            # Split into 2 lines as evenly as possible
            mid_point = len(words) // 2
            line1 = " ".join(words[:mid_point])
            line2 = " ".join(words[mid_point:])
        else:
            # Single long word, split by character
            mid_char = len(sender_name) // 2
            line1 = sender_name[:mid_char]
            line2 = sender_name[mid_char:]
    else:
        # For shorter names, put in single line centered, with empty second line
        line1 = sender_name
        line2 = ""
    
    # Draw first line centered
    line1_bbox = draw.textbbox((0, 0), line1, font=font_medium)
    line1_width = line1_bbox[2] - line1_bbox[0]
    line1_x = (label_width - line1_width) // 2
    draw.text((line1_x, y_offset), line1, fill="black", font=font_medium)
    y_offset += 18
    
    # Draw second line centered (if exists)
    if line2:
        line2_bbox = draw.textbbox((0, 0), line2, font=font_medium)
        line2_width = line2_bbox[2] - line2_bbox[0]
        line2_x = (label_width - line2_width) // 2
        draw.text((line2_x, y_offset), line2, fill="black", font=font_medium)
        y_offset += 18
    else:
        y_offset += 18  # Keep spacing consistent even if no second line
    
    y_offset += 8  # Extra space after sender
    
    # Shipping code with better spacing - centered format
    shipping_label_text = "RESI PENGIRIMAN:"
    shipping_label_bbox = draw.textbbox((0, 0), shipping_label_text, font=font_small)
    shipping_label_width = shipping_label_bbox[2] - shipping_label_bbox[0]
    shipping_label_x = (label_width - shipping_label_width) // 2
    draw.text((shipping_label_x, y_offset), shipping_label_text, fill="black", font=font_small)
    y_offset += 18  # More spacing
    
    # Make shipping code centered and handle long codes
    if len(shipping_code) > 15:  # For long codes (like 20 characters)
        # Split into 2 lines for better readability
        mid_point = len(shipping_code) // 2
        # Find a good break point (space or hyphen) near the middle
        break_point = mid_point
        for i in range(max(0, mid_point-3), min(len(shipping_code), mid_point+4)):
            if shipping_code[i] in ['-', '_', ' ']:
                break_point = i
                break
        
        line1 = shipping_code[:break_point]
        line2 = shipping_code[break_point:].lstrip('-_')  # Remove leading separators
        
        # Draw first line centered
        line1_bbox = draw.textbbox((0, 0), line1, font=font_medium)
        line1_width = line1_bbox[2] - line1_bbox[0]
        line1_x = (label_width - line1_width) // 2
        draw.text((line1_x, y_offset), line1, fill="black", font=font_medium)
        y_offset += 16
        
        # Draw second line centered
        line2_bbox = draw.textbbox((0, 0), line2, font=font_medium)
        line2_width = line2_bbox[2] - line2_bbox[0]
        line2_x = (label_width - line2_width) // 2
        draw.text((line2_x, y_offset), line2, fill="black", font=font_medium)
        y_offset += 20
    else:
        # For shorter codes, add spacing between characters and center
        shipping_code_spaced = " ".join(shipping_code)
        shipping_code_bbox = draw.textbbox((0, 0), shipping_code_spaced, font=font_medium)
        shipping_code_width = shipping_code_bbox[2] - shipping_code_bbox[0]
        shipping_code_x = (label_width - shipping_code_width) // 2
        draw.text((shipping_code_x, y_offset), shipping_code_spaced, fill="black", font=font_medium)
        y_offset += 25  # More spacing
    
    # QR Code - centered with more space
    qr_x = (label_width - qr_size) // 2
    img.paste(qr_img, (qr_x, y_offset))
    y_offset += qr_size + 12  # More space after QR
    
    # QR info with better centering
    qr_info_text = f"Scan: {shipping_code}"
    qr_info_bbox = draw.textbbox((0, 0), qr_info_text, font=font_tiny)
    qr_info_width = qr_info_bbox[2] - qr_info_bbox[0]
    qr_info_x = (label_width - qr_info_width) // 2
    draw.text((qr_info_x, y_offset), qr_info_text, fill="black", font=font_tiny)
    y_offset += 18
    
    # Thicker separator line
    draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=2)
    y_offset += 12
    
    # Save the image with higher DPI for thermal printer
    filename = f"label_{label_id}_{shipping_code}.png"
    filepath = os.path.join(labels_dir, filename)
    img.save(filepath, dpi=(300, 300))  # Higher DPI for sharper text
    
    return filepath

def generate_thermal_optimized_label(sender_name: str, shipping_code: str, label_id: int) -> str:
    """
    Generate thermal printer optimized label (monochrome, high contrast)
    """
    
    # Create labels directory if it doesn't exist
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # Thermal printer 58mm ≈ 203 pixels at 203 DPI
    label_width = 203
    label_height = 280
    
    # Create monochrome image (1-bit)
    img = Image.new('1', (label_width, label_height), 1)  # 1 = white, 0 = black
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load a font
        font_large = ImageFont.truetype("arial.ttf", 12)
        font_medium = ImageFont.truetype("arial.ttf", 10)
        font_small = ImageFont.truetype("arial.ttf", 8)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=2,
        border=1,
    )
    qr.add_data(shipping_code)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color=0, back_color=1)  # Black on white for thermal
    qr_size = 80
    qr_img = qr_img.resize((qr_size, qr_size))
            
    # Continue with rest of layout...
    # (Similar to above but with thermal optimizations)
    
    # Save as monochrome PNG
    filename = f"thermal_label_{label_id}_{shipping_code}.png"
    filepath = os.path.join(labels_dir, filename)
    img.save(filepath)
    
    return filepath

def get_label_image(label_id: int, shipping_code: str) -> str:
    """Get the path to an existing label image"""
    filename = f"label_{label_id}_{shipping_code}.png"
    return os.path.join("labels", filename)

def generate_shipping_label(sender_name: str, sender_phone: str, recipient_name: str, 
                          recipient_address: str, recipient_phone: str, shipping_code: str, label_id: int) -> str:
    """
    Generate shipping label with sender and recipient information for thermal printer 58mm width
    Returns the path to the generated image
    """
    
    # Create labels directory if it doesn't exist
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # Thermal printer 58mm ≈ 203 pixels at 203 DPI
    label_width = 203
    label_height = 400  # Increased for more content
    
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Use larger fonts for thermal printer readability
        font_large = ImageFont.truetype("arial.ttf", 16)
        font_medium = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_tiny = ImageFont.truetype("arial.ttf", 10)
    except:
        # Fallback fonts
        try:
            font_large = ImageFont.truetype("calibri.ttf", 16)
            font_medium = ImageFont.truetype("calibri.ttf", 14)
            font_small = ImageFont.truetype("calibri.ttf", 12)
            font_tiny = ImageFont.truetype("calibri.ttf", 10)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
    
    # Layout design with better spacing
    y_offset = 12  # Top margin
        
    # TO Section (Recipient)
    to_label_text = "TO:"
    to_label_bbox = draw.textbbox((0, 0), to_label_text, font=font_small)
    to_label_width = to_label_bbox[2] - to_label_bbox[0]
    to_label_x = (label_width - to_label_width) // 2
    draw.text((to_label_x, y_offset), to_label_text, fill="black", font=font_small)
    y_offset += 16
    
    # Recipient name centered
    recipient_bbox = draw.textbbox((0, 0), recipient_name, font=font_medium)
    recipient_width = recipient_bbox[2] - recipient_bbox[0]
    recipient_x = (label_width - recipient_width) // 2
    draw.text((recipient_x, y_offset), recipient_name, fill="black", font=font_medium)
    y_offset += 18
    
    # Address label centered
    address_label_text = "ADDRESS:"
    address_label_bbox = draw.textbbox((0, 0), address_label_text, font=font_tiny)
    address_label_width = address_label_bbox[2] - address_label_bbox[0]
    address_label_x = (label_width - address_label_width) // 2
    draw.text((address_label_x, y_offset), address_label_text, fill="black", font=font_tiny)
    y_offset += 14
    
    # Address - wrap to multiple lines and center each line
    max_chars_per_line = 25
    address_words = recipient_address.split()
    address_lines = []
    current_line = ""
    
    for word in address_words:
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) <= max_chars_per_line:
            current_line = test_line
        else:
            if current_line:
                address_lines.append(current_line)
            current_line = word
    if current_line:
        address_lines.append(current_line)
    
    for line in address_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_tiny)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (label_width - line_width) // 2
        draw.text((line_x, y_offset), line, fill="black", font=font_tiny)
        y_offset += 12
    
    # Recipient phone centered
    phone_label_text = f"NO HP: {recipient_phone}"
    phone_label_bbox = draw.textbbox((0, 0), phone_label_text, font=font_tiny)
    phone_label_width = phone_label_bbox[2] - phone_label_bbox[0]
    phone_label_x = (label_width - phone_label_width) // 2
    draw.text((phone_label_x, y_offset), phone_label_text, fill="black", font=font_tiny)
    y_offset += 20
    
    # Separator line
    draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=1)
    y_offset += 15
    
    # FROM Section (Sender)
    from_label_text = "FROM:"
    from_label_bbox = draw.textbbox((0, 0), from_label_text, font=font_small)
    from_label_width = from_label_bbox[2] - from_label_bbox[0]
    from_label_x = (label_width - from_label_width) // 2
    draw.text((from_label_x, y_offset), from_label_text, fill="black", font=font_small)
    y_offset += 16
    
    # Sender name centered
    sender_bbox = draw.textbbox((0, 0), sender_name, font=font_medium)
    sender_width = sender_bbox[2] - sender_bbox[0]
    sender_x = (label_width - sender_width) // 2
    draw.text((sender_x, y_offset), sender_name, fill="black", font=font_medium)
    y_offset += 18
    
    # Sender phone centered
    sender_phone_text = f"NO HP: {sender_phone}"
    sender_phone_bbox = draw.textbbox((0, 0), sender_phone_text, font=font_tiny)
    sender_phone_width = sender_phone_bbox[2] - sender_phone_bbox[0]
    sender_phone_x = (label_width - sender_phone_width) // 2
    draw.text((sender_phone_x, y_offset), sender_phone_text, fill="black", font=font_tiny)
    y_offset += 20
    
    # Separator line
    draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=2)
    y_offset += 15
    
    # Shipping code section - only if not empty
    if shipping_code and shipping_code.strip():
        shipping_label_text = "RESI PENGIRIMAN:"
        shipping_label_bbox = draw.textbbox((0, 0), shipping_label_text, font=font_small)
        shipping_label_width = shipping_label_bbox[2] - shipping_label_bbox[0]
        shipping_label_x = (label_width - shipping_label_width) // 2
        draw.text((shipping_label_x, y_offset), shipping_label_text, fill="black", font=font_small)
        y_offset += 18
        
        # Shipping code centered
        if len(shipping_code) > 15:
            # Split long codes
            mid_point = len(shipping_code) // 2
            break_point = mid_point
            for i in range(max(0, mid_point-3), min(len(shipping_code), mid_point+4)):
                if shipping_code[i] in ['-', '_', ' ']:
                    break_point = i
                    break
            
            line1 = shipping_code[:break_point]
            line2 = shipping_code[break_point:].lstrip('-_')
            
            line1_bbox = draw.textbbox((0, 0), line1, font=font_medium)
            line1_width = line1_bbox[2] - line1_bbox[0]
            line1_x = (label_width - line1_width) // 2
            draw.text((line1_x, y_offset), line1, fill="black", font=font_medium)
            y_offset += 16
            
            line2_bbox = draw.textbbox((0, 0), line2, font=font_medium)
            line2_width = line2_bbox[2] - line2_bbox[0]
            line2_x = (label_width - line2_width) // 2
            draw.text((line2_x, y_offset), line2, fill="black", font=font_medium)
            y_offset += 20
        else:
            shipping_code_spaced = " ".join(shipping_code)
            shipping_code_bbox = draw.textbbox((0, 0), shipping_code_spaced, font=font_medium)
            shipping_code_width = shipping_code_bbox[2] - shipping_code_bbox[0]
            shipping_code_x = (label_width - shipping_code_width) // 2
            draw.text((shipping_code_x, y_offset), shipping_code_spaced, fill="black", font=font_medium)
            y_offset += 25
        
        # Add separator after shipping code
        draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=1)
        y_offset += 15
        
        # Final separator line after shipping code
        draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=2)
        y_offset += 12
    
    # Save the image
    filename = f"shipping_label_{label_id}_{shipping_code or 'no_code'}.png"
    filepath = os.path.join(labels_dir, filename)
    img.save(filepath, dpi=(300, 300))
    
    return filepath