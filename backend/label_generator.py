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
    
    # Thermal printer 58mm ≈ 203 pixels at 90 DPI
    label_width = 203
    label_height = 280  # Increased for better layout
    
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load a font (fallback to default if not available)
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
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(shipping_code)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_size = 80
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Layout design for 58mm thermal printer
    y_offset = 8

    # Header: "FREE LABEL PRINTING"
    header_text = "ABERAHARJA EXPRESS"
    header_bbox = draw.textbbox((0, 0), header_text, font=font_large)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (label_width - header_width) // 2
    draw.text((header_x, y_offset), header_text, fill="black", font=font_large)
    y_offset += 18
    
    subheader_text = "Free Label Printing"
    subheader_bbox = draw.textbbox((0, 0), subheader_text, font=font_small)
    subheader_width = subheader_bbox[2] - subheader_bbox[0]
    subheader_x = (label_width - subheader_width) // 2
    draw.text((subheader_x, y_offset), subheader_text, fill="black", font=font_small)
    y_offset += 15
    
    # Separator line
    draw.line([(10, y_offset), (label_width - 10, y_offset)], fill="black", width=1)
    y_offset += 10
    
    # Sender info
    draw.text((10, y_offset), "PENGIRIM:", fill="black", font=font_small)
    y_offset += 12
    
    # Wrap sender name if too long
    max_chars_per_line = 22
    if len(sender_name) > max_chars_per_line:
        words = sender_name.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            draw.text((10, y_offset), line, fill="black", font=font_medium)
            y_offset += 13
    else:
        draw.text((10, y_offset), sender_name, fill="black", font=font_medium)
        y_offset += 15
    
    y_offset += 5
    
    # Shipping code
    draw.text((10, y_offset), "KODE PENGIRIMAN:", fill="black", font=font_small)
    y_offset += 12
    draw.text((10, y_offset), shipping_code, fill="black", font=font_large)
    y_offset += 20
    
    # QR Code - centered
    qr_x = (label_width - qr_size) // 2
    img.paste(qr_img, (qr_x, y_offset))
    y_offset += qr_size + 8
    
    # QR info
    qr_info_text = f"Scan QR: {shipping_code}"
    qr_info_bbox = draw.textbbox((0, 0), qr_info_text, font=font_small)
    qr_info_width = qr_info_bbox[2] - qr_info_bbox[0]
    qr_info_x = (label_width - qr_info_width) // 2
    draw.text((qr_info_x, y_offset), qr_info_text, fill="black", font=font_small)
    y_offset += 15
    
    # Separator line
    draw.line([(10, y_offset), (label_width - 10, y_offset)], fill="black", width=1)
    y_offset += 8
    
    # Date
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    date_text = f"Cetak: {current_date}"
    draw.text((10, y_offset), date_text, fill="black", font=font_small)
    
    # Save the image
    filename = f"label_{label_id}_{shipping_code}.png"
    filepath = os.path.join(labels_dir, filename)
    img.save(filepath, dpi=(203, 203))  # Set DPI for thermal printer
    
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