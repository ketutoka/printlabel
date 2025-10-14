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
    label_height = 250  # Adjustable based on content
    
    # Create white background
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load a font (fallback to default if not available)
        font_large = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 8)
    except:
        font_large = ImageFont.load_default()
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
    y_offset = 10

    # Header: "FREE LABEL PRINTING"
    header_text = "Aberaharja Free Label Printing"
    header_bbox = draw.textbbox((0, 0), header_text, font=font_large)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (label_width - header_width) // 2
    draw.text((header_x, y_offset), header_text, fill="black", font=font_large)
    y_offset += 25
    
    # Separator line
    draw.line([(10, y_offset), (label_width - 10, y_offset)], fill="black", width=1)
    y_offset += 10
    
    # Sender info
    draw.text((10, y_offset), "Pengirim:", fill="black", font=font_small)
    y_offset += 15
    draw.text((10, y_offset), sender_name, fill="black", font=font_large)
    y_offset += 20
    
    # Shipping code
    draw.text((10, y_offset), "Kode Pengiriman:", fill="black", font=font_small)
    y_offset += 15
    draw.text((10, y_offset), shipping_code, fill="black", font=font_large)
    y_offset += 25
    
    # QR Code - centered
    qr_x = (label_width - qr_size) // 2
    img.paste(qr_img, (qr_x, y_offset))
    y_offset += qr_size + 10
    
    # Date
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    date_text = f"Tanggal: {current_date}"
    draw.text((10, y_offset), date_text, fill="black", font=font_small)
    
    # Save the image
    filename = f"label_{label_id}_{shipping_code}.png"
    filepath = os.path.join(labels_dir, filename)
    img.save(filepath)
    
    return filepath

def get_label_image(label_id: int, shipping_code: str) -> str:
    """Get the path to an existing label image"""
    filename = f"label_{label_id}_{shipping_code}.png"
    return os.path.join("labels", filename)