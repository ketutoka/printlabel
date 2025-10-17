import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def generate_label_with_qr(sender_name: str, shipping_code: str, label_id: int, sender_phone: str = "0818986657") -> str:
    """
    Generate simple label image with QR code for thermal printer 58mm width
    Large fonts and QR code for better readability
    Returns the path to the generated image
    """
    
    # Create labels directory if it doesn't exist
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # Thermal printer 58mm ≈ 203 pixels at 203 DPI
    label_width = 203
    label_height = 270  # Increased for large QR and fonts
    
    # Create white background
    img = Image.new('1', (label_width, label_height), 1)  # 1 = putih
    draw = ImageDraw.Draw(img)    

    try:
        # Smaller fonts for better spacing
        font_header = ImageFont.truetype("arial.ttf", 12)    # Reduced from 16 to 12
        font_name = ImageFont.truetype("arial.ttf", 12)      # Reduced from 16 to 11
        font_phone = ImageFont.truetype("arial.ttf", 12)     # Reduced from 16 to 10
        font_resi_label = ImageFont.truetype("arial.ttf", 12) # Reduced from 14 to 10
        font_resi_code = ImageFont.truetype("arial.ttf", 12)  # Reduced from 18 to 12
    except:
        # Final fallback
        font_header = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_phone = ImageFont.load_default()
        font_resi_label = ImageFont.load_default()
        font_resi_code = ImageFont.load_default()
    
    # Generate larger QR code like the example
    qr = qrcode.QRCode(
        version=3,  # Larger QR version
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Lower error correction for larger data capacity
        box_size=4,  # Much larger box size
        border=1,    # Minimal border
    )
    qr.add_data(shipping_code)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_size = 110  # Reduced QR code size for better fit
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Layout design matching the example
    y_offset = 3  # Reduced top margin

    # "PENGIRIM:" header - centered
    pengirim_text = "PENGIRIM:"
    pengirim_bbox = draw.textbbox((0, 0), pengirim_text, font=font_header)
    pengirim_width = pengirim_bbox[2] - pengirim_bbox[0]
    pengirim_x = (label_width - pengirim_width) // 2
    draw.text((pengirim_x, y_offset), pengirim_text, fill=0, font=font_header)
    y_offset += 16  # Reduced spacing after header
    
    # Sender name - large and centered like "SehatJos" in example
    # Split name if too long to fit
    if len(sender_name) > 12:  # Adjust threshold for large font
        words = sender_name.split()
        if len(words) >= 2:
            mid_point = len(words) // 2
            line1 = " ".join(words[:mid_point])
            line2 = " ".join(words[mid_point:])
        else:
            # Single long word, split by character
            mid_char = len(sender_name) // 2
            line1 = sender_name[:mid_char]
            line2 = sender_name[mid_char:]
    else:
        line1 = sender_name
        line2 = ""
    
    # Draw first line of name
    line1_bbox = draw.textbbox((0, 0), line1, font=font_name)
    line1_width = line1_bbox[2] - line1_bbox[0]
    line1_x = (label_width - line1_width) // 2
    draw.text((line1_x, y_offset), line1, fill=0, font=font_name)
    y_offset += 16  # Reduced spacing
    
    # Draw second line of name if exists
    if line2:
        line2_bbox = draw.textbbox((0, 0), line2, font=font_name)
        line2_width = line2_bbox[2] - line2_bbox[0]
        line2_x = (label_width - line2_width) // 2
        draw.text((line2_x, y_offset), line2, fill=0, font=font_name)
        y_offset += 16  # Reduced spacing
    else:
        y_offset += 3  # Smaller space if no second line
    
    # Phone number
    phone_text = sender_phone or "0818986657"  # Use provided phone or default
    phone_bbox = draw.textbbox((0, 0), phone_text, font=font_phone)
    phone_width = phone_bbox[2] - phone_bbox[0]
    phone_x = (label_width - phone_width) // 2
    draw.text((phone_x, y_offset), phone_text, fill=0, font=font_phone)
    y_offset += 16  # Reduced spacing
    
    # "Resi Pengiriman:" label
    resi_label_text = "Resi Pengiriman:"
    resi_label_bbox = draw.textbbox((0, 0), resi_label_text, font=font_resi_label)
    resi_label_width = resi_label_bbox[2] - resi_label_bbox[0]
    resi_label_x = (label_width - resi_label_width) // 2
    draw.text((resi_label_x, y_offset), resi_label_text, fill=0, font=font_resi_label)
    y_offset += 16  # Reduced spacing
    
    # QR Code - centered
    qr_x = (label_width - qr_size) // 2
    img.paste(qr_img, (qr_x, y_offset))
    y_offset += qr_size + 2  # Minimal space after QR
    
    # Shipping code below QR - very large like "SPXID050699308944A" in example

    max_chars = 28
    words = shipping_code.split()
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if len(test) <= max_chars:
            line = test
        else:
            line_bbox = draw.textbbox((0, 0), line, font=font_resi_code)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (label_width - line_width) // 2
            draw.text((line_x, y_offset), line, fill=0, font=font_resi_code)
            y_offset += 16  # Reduced spacing
            line = w
            
    if line:
        line_bbox = draw.textbbox((0, 0), line, font=font_resi_code)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (label_width - line_width) // 2
        draw.text((line_x, y_offset), line, fill=0, font=font_resi_code)
        y_offset += 16  # Reduced spacing


    """ if len(shipping_code) > 12:  # Split long codes
        # For very long codes, split into multiple lines
        chars_per_line = 12
        lines = []
        for i in range(0, len(shipping_code), chars_per_line):
            lines.append(shipping_code[i:i+chars_per_line])
        
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font_resi_code)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (label_width - line_width) // 2
            draw.text((line_x, y_offset), line, fill=0, font=font_resi_code)
            y_offset += 16  # Reduced spacing
    else:
        # For shorter codes, show in one line
        code_bbox = draw.textbbox((0, 0), shipping_code, font=font_resi_code)
        code_width = code_bbox[2] - code_bbox[0]
        code_x = (label_width - code_width) // 2
        draw.text((code_x, y_offset), shipping_code, fill=0, font=font_resi_code)
        y_offset += 16  # Reduced spacing
    """

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

def generate_shipping_label_old(sender_name: str, sender_phone: str, recipient_name: str, 
                          recipient_address: str, recipient_phone: str, shipping_code: str, label_id: int) -> str:
    """
    Generate shipping label with sender and recipient information for thermal printer 58mm width
    Optimized for thermal printer sharpness and clarity
    Returns the path to the generated image
    """
    
    # Create labels directory if it doesn't exist
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # Thermal printer 58mm ≈ 304 pixels at 304 DPI (optimized resolution)
    label_width = 304  # 1.5x for clean rendering without artifacts
    label_height = 450  # Proportionally increased
    
    # Create RGB image for cleaner text rendering, convert later
    img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Smaller fonts for better spacing on thermal printing
        font_large = ImageFont.truetype("arial.ttf", 22)      # Reduced from 28 to 22
        font_medium = ImageFont.truetype("arial.ttf", 18)     # Reduced from 24 to 18
        font_small = ImageFont.truetype("arial.ttf", 16)      # Reduced from 20 to 16
        font_tiny = ImageFont.truetype("arial.ttf", 14)       # Reduced from 16 to 14
    except:
        # Fallback fonts with regular weight
        try:
            font_large = ImageFont.truetype("calibri.ttf", 22)    # Reduced sizes
            font_medium = ImageFont.truetype("calibri.ttf", 18)
            font_small = ImageFont.truetype("calibri.ttf", 16)
            font_tiny = ImageFont.truetype("calibri.ttf", 14)
        except:
            # Final fallback - load default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
    
    # Layout design with compact spacing
    y_offset = 10  # Reduced top margin
        
    # TO Section (Recipient)
    to_label_text = "KEPADA:"
    to_label_bbox = draw.textbbox((0, 0), to_label_text, font=font_small)
    to_label_width = to_label_bbox[2] - to_label_bbox[0]
    to_label_x = (label_width - to_label_width) // 2
    draw.text((to_label_x, y_offset), to_label_text, fill=0, font=font_small)
    y_offset += 18  # Reduced spacing
    
    # Recipient name centered (handle long names better)
    if len(recipient_name) > 20:  # Split long names for better readability
        words = recipient_name.split()
        if len(words) >= 2:
            mid_point = len(words) // 2
            name_line1 = " ".join(words[:mid_point])
            name_line2 = " ".join(words[mid_point:])
        else:
            mid_char = len(recipient_name) // 2
            name_line1 = recipient_name[:mid_char]
            name_line2 = recipient_name[mid_char:]
        
        # Draw first line
        line1_bbox = draw.textbbox((0, 0), name_line1, font=font_medium)
        line1_width = line1_bbox[2] - line1_bbox[0]
        line1_x = (label_width - line1_width) // 2
        draw.text((line1_x, y_offset), name_line1, fill=0, font=font_medium)
        y_offset += 20  # Reduced spacing
        
        # Draw second line
        line2_bbox = draw.textbbox((0, 0), name_line2, font=font_medium)
        line2_width = line2_bbox[2] - line2_bbox[0]
        line2_x = (label_width - line2_width) // 2
        draw.text((line2_x, y_offset), name_line2, fill=0, font=font_medium)
        y_offset += 20  # Reduced spacing
    else:
        recipient_bbox = draw.textbbox((0, 0), recipient_name, font=font_medium)
        recipient_width = recipient_bbox[2] - recipient_bbox[0]
        recipient_x = (label_width - recipient_width) // 2
        draw.text((recipient_x, y_offset), recipient_name, fill=0, font=font_medium)
        y_offset += 20  # Reduced spacing
        
    # Address - wrap to multiple lines and center each line
    max_chars_per_line = 28
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
        draw.text((line_x, y_offset), line, fill=0, font=font_tiny)
        y_offset += 15  # Reduced line spacing
    
    # Recipient phone centered
    phone_label_text = f"HP: {recipient_phone}"
    phone_label_bbox = draw.textbbox((0, 0), phone_label_text, font=font_tiny)
    phone_label_width = phone_label_bbox[2] - phone_label_bbox[0]
    phone_label_x = (label_width - phone_label_width) // 2
    draw.text((phone_label_x, y_offset), phone_label_text, fill=0, font=font_tiny)
    y_offset += 18  # Reduced spacing, removed separator line
        
    # FROM Section (Sender)
    from_label_text = "PENGIRIM:"
    from_label_bbox = draw.textbbox((0, 0), from_label_text, font=font_small)
    from_label_width = from_label_bbox[2] - from_label_bbox[0]
    from_label_x = (label_width - from_label_width) // 2
    draw.text((from_label_x, y_offset), from_label_text, fill=0, font=font_small)
    y_offset += 18  # Reduced spacing
    
    # Sender name centered
    sender_bbox = draw.textbbox((0, 0), sender_name, font=font_medium)
    sender_width = sender_bbox[2] - sender_bbox[0]
    sender_x = (label_width - sender_width) // 2
    draw.text((sender_x, y_offset), sender_name, fill=0, font=font_medium)
    y_offset += 20  # Reduced spacing
    
    # Sender phone centered
    sender_phone_text = f"HP: {sender_phone}"
    sender_phone_bbox = draw.textbbox((0, 0), sender_phone_text, font=font_tiny)
    sender_phone_width = sender_phone_bbox[2] - sender_phone_bbox[0]
    sender_phone_x = (label_width - sender_phone_width) // 2
    draw.text((sender_phone_x, y_offset), sender_phone_text, fill=0, font=font_tiny)
    y_offset += 18  # Reduced spacing, removed separator line
        
    # Shipping code section - only if not empty
    if shipping_code and shipping_code.strip():
        shipping_label_text = "RESI PENGIRIMAN:"
        shipping_label_bbox = draw.textbbox((0, 0), shipping_label_text, font=font_small)
        shipping_label_width = shipping_label_bbox[2] - shipping_label_bbox[0]
        shipping_label_x = (label_width - shipping_label_width) // 2
        draw.text((shipping_label_x, y_offset), shipping_label_text, fill=0, font=font_small)
        y_offset += 18  # Reduced spacing
        
        # Shipping code centered with better formatting
        if len(shipping_code) > 15:
            # Split long codes intelligently
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
            draw.text((line1_x, y_offset), line1, fill=0, font=font_medium)
            y_offset += 18  # Reduced spacing
            
            line2_bbox = draw.textbbox((0, 0), line2, font=font_medium)
            line2_width = line2_bbox[2] - line2_bbox[0]
            line2_x = (label_width - line2_width) // 2
            draw.text((line2_x, y_offset), line2, fill=0, font=font_medium)
            y_offset += 20  # Reduced spacing
        else:
            # For shorter codes, add spacing for readability
            shipping_code_spaced = " ".join(shipping_code) if len(shipping_code) <= 10 else shipping_code
            shipping_code_bbox = draw.textbbox((0, 0), shipping_code_spaced, font=font_medium)
            shipping_code_width = shipping_code_bbox[2] - shipping_code_bbox[0]
            shipping_code_x = (label_width - shipping_code_width) // 2
            draw.text((shipping_code_x, y_offset), shipping_code_spaced, fill=0, font=font_medium)
            y_offset += 20  # Reduced spacing
    
    # Convert RGB to grayscale first
    img_gray = img.convert('L')
    
    # Apply threshold to ensure pure black and white
    threshold = 128
    img_bw = img_gray.point(lambda x: 0 if x < threshold else 255, mode='1')
    
    # Resize back to original thermal printer resolution (203px width)
    img_final = img_bw.resize((203, int(300 * img_bw.height / img_bw.width)), Image.Resampling.LANCZOS)
    
    # Save with optimal settings for thermal printer
    filename = f"shipping_label_{label_id}_{shipping_code or 'no_code'}.png"
    filepath = os.path.join(labels_dir, filename)
    
    # Save as 1-bit PNG for maximum sharpness on thermal printer
    img_final.save(filepath, "PNG", optimize=True, bits=1)
    
    return filepath

def generate_shipping_label(sender_name: str, sender_phone: str, recipient_name: str, 
                            recipient_address: str, recipient_phone: str, 
                            shipping_code: str, label_id: int) -> str:
    """
    Generate ultra-sharp 1-bit thermal printer label (no dithering, no blur)
    Compatible with 58mm printers (203 DPI)
    """
    labels_dir = "labels"
    os.makedirs(labels_dir, exist_ok=True)

    # Thermal 58mm = 203px width
    label_width = 203
    label_height = 300  # cukup panjang untuk alamat panjang

    # Gunakan mode '1' langsung untuk hasil hitam/putih tajam
    img = Image.new('1', (label_width, label_height), 1)  # 1 = putih
    draw = ImageDraw.Draw(img)

    # Gunakan font tebal agar solid di thermal printer
    try:
        font_bold_large = ImageFont.truetype("arial.ttf", 13)
        font_bold_medium = ImageFont.truetype("arial.ttf", 11)
        font_bold_small = ImageFont.truetype("arial.ttf", 10)
    except:
        font_bold_large = ImageFont.load_default()
        font_bold_medium = ImageFont.load_default()
        font_bold_small = ImageFont.load_default()

    y = 10
    x = 20

    # ======= Bagian Penerima =======
    draw.text((x, y), "KEPADA:", font=font_bold_small, fill=0)
    y += 16

    # Nama penerima
    draw.text((x, y), recipient_name, font=font_bold_medium, fill=0)
    y += 18

    # Alamat (wrap text otomatis)
    max_chars = 28
    words = recipient_address.split()
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if len(test) <= max_chars:
            line = test
        else:
            draw.text((x, y), line, font=font_bold_small, fill=0)
            y += 16
            line = w
    if line:
        draw.text((x, y), line, font=font_bold_small, fill=0)
        y += 18

    draw.text((x, y), f"HP: {recipient_phone}", font=font_bold_small, fill=0)
    y += 26

    # ======= Bagian Pengirim =======
    draw.text((x, y), "PENGIRIM:", font=font_bold_small, fill=0)
    y += 16
    draw.text((x, y), sender_name, font=font_bold_medium, fill=0)
    y += 16
    draw.text((x, y), f"HP: {sender_phone}", font=font_bold_small, fill=0)
    y += 10

    # ======= Finishing =======
    # Crop area kosong agar tidak terlalu panjang
    img_cropped = img.crop((0, 0, label_width, min(y + 10, label_height)))

    filename = f"thermal_label_{label_id}_{shipping_code or 'nocode'}.bmp"
    filepath = os.path.join(labels_dir, filename)
    img_cropped.save(filepath, format="BMP")

    return filepath
