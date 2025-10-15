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
    qr_size = 90  # Increased from 80
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Layout design with better spacing
    y_offset = 12  # More top margin

    # Header with better spacing
    header_text = "ABERAHARJA EXPRESS"
    header_bbox = draw.textbbox((0, 0), header_text, font=font_medium)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (label_width - header_width) // 2
    draw.text((header_x, y_offset), header_text, fill="black", font=font_medium)
    y_offset += 22  # More spacing
    
    subheader_text = "Free Label Printing"
    subheader_bbox = draw.textbbox((0, 0), subheader_text, font=font_tiny)
    subheader_width = subheader_bbox[2] - subheader_bbox[0]
    subheader_x = (label_width - subheader_width) // 2
    draw.text((subheader_x, y_offset), subheader_text, fill="black", font=font_tiny)
    y_offset += 18  # More spacing
    
    # Thicker separator line
    draw.line([(8, y_offset), (label_width - 8, y_offset)], fill="black", width=2)
    y_offset += 15  # More spacing after line
    
    # Sender info with better spacing
    draw.text((12, y_offset), "PENGIRIM:", fill="black", font=font_small)
    y_offset += 18  # More spacing between label and content
    
    # Wrap sender name with better line spacing
    max_chars_per_line = 18  # Reduced for larger font
    if len(sender_name) > max_chars_per_line:
        words = sender_name.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= max_chars_per_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            draw.text((12, y_offset), line, fill="black", font=font_medium)
            y_offset += 18  # Better line spacing
    else:
        draw.text((12, y_offset), sender_name, fill="black", font=font_medium)
        y_offset += 20
    
    y_offset += 8  # Extra space after sender
    
    # Shipping code with better spacing
    draw.text((12, y_offset), "KODE PENGIRIMAN:", fill="black", font=font_small)
    y_offset += 18  # More spacing
    
    # Make shipping code more prominent and spaced out
    shipping_code_spaced = " ".join(shipping_code)  # Add space between characters
    draw.text((12, y_offset), shipping_code_spaced, fill="black", font=font_large)
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
    
    # Date with better formatting
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    date_text = f"Cetak: {current_date}"
    draw.text((12, y_offset), date_text, fill="black", font=font_tiny)
    
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
    
    # Rest of the layout (similar but optimized for thermal)
    y_offset = 8
    
    # Header
    header_text = "ABERAHARJA EXPRESS"
    header_bbox = draw.textbbox((0, 0), header_text, font=font_large)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (label_width - header_width) // 2
    draw.text((header_x, y_offset), header_text, fill=0, font=font_large)
    y_offset += 18
    
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