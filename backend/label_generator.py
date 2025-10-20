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
    
    # "Resi Pengiriman:" label - rata kiri
    resi_label_text = "Resi Pengiriman:"
    draw.text((20, y_offset), resi_label_text, fill=0, font=font_resi_label)  # Rata kiri
    y_offset += 16  # Reduced spacing
    
    # QR Code - rata kiri untuk konsistensi
    qr_x = 20  # Sama dengan margin kiri text (x position)
    img.paste(qr_img, (qr_x, y_offset))
    y_offset += qr_size + 2  # Minimal space after QR
    
    # Shipping code below QR - rata kiri
    max_chars = 28
    words = shipping_code.split()
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if len(test) <= max_chars:
            line = test
        else:
            draw.text((20, y_offset), line, fill=0, font=font_resi_code)  # Rata kiri
            y_offset += 16  # Reduced spacing
            line = w

    if line:
        draw.text((20, y_offset), line, fill=0, font=font_resi_code)  # Rata kiri
        y_offset += 10  # Reduced spacing


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
    #filename = f"label_{label_id}_{shipping_code}.png"
    #filepath = os.path.join(labels_dir, filename)
    #img.save(filepath, dpi=(300, 300))  # Higher DPI for sharper text

    # Crop area kosong agar tidak terlalu panjang
    img_cropped = img.crop((0, 0, label_width, min(y_offset + 5, label_height)))

    filename = f"label_{label_id}_{shipping_code or 'nocode'}.bmp"
    filepath = os.path.join(labels_dir, filename)
    img_cropped.save(filepath, format="BMP")

    return filepath


def get_label_image(label_id: int, shipping_code: str) -> str:
    """Get the path to an existing label image"""
    filename = f"label_{label_id}_{shipping_code}.png"
    return os.path.join("labels", filename)

def generate_shipping_label(sender_name: str, sender_phone: str, recipient_name: str = "", 
                            recipient_address: str = "", recipient_phone: str = "", 
                            shipping_code: str = "", label_id: int = 0, label_size: str = "58mm") -> str:
    """
    Generate ultra-sharp 1-bit thermal printer label (no dithering, no blur)
    Compatible with 58mm and 80mm printers (203 DPI)
    Recipient and shipping code are optional - will be skipped if empty
    """
    labels_dir = "labels"
    os.makedirs(labels_dir, exist_ok=True)

    # Determine label width based on size
    if label_size == "80mm":
        label_width = 284  # 80mm ≈ 284px at 203 DPI
        font_large = 15
        font_medium = 13
        font_small = 11
        qr_size = 100
        max_chars = 38  # More characters for wider label
    else:  # Default 58mm
        label_width = 203  # 58mm ≈ 203px at 203 DPI
        font_large = 13
        font_medium = 11
        font_small = 10
        qr_size = 80
        max_chars = 28

    label_height = 350  # Dynamic height based on content

    # Gunakan mode '1' langsung untuk hasil hitam/putih tajam
    img = Image.new('1', (label_width, label_height), 1)  # 1 = putih
    draw = ImageDraw.Draw(img)

    # Gunakan font dengan ukuran sesuai label
    try:
        font_bold_large = ImageFont.truetype("arial.ttf", font_large)
        font_bold_medium = ImageFont.truetype("arial.ttf", font_medium)
        font_bold_small = ImageFont.truetype("arial.ttf", font_small)
    except:
        font_bold_large = ImageFont.load_default()
        font_bold_medium = ImageFont.load_default()
        font_bold_small = ImageFont.load_default()

    y = 15  # Start position
    x = 20

    # ======= Bagian Penerima (Optional) =======
    if recipient_name and recipient_name.strip():
        draw.text((x, y), "KEPADA:", font=font_bold_small, fill=0)
        y += 15  # Kurangi spacing dari 18 ke 15

        # Nama penerima
        draw.text((x, y), recipient_name, font=font_bold_medium, fill=0)
        y += 15  # Kurangi spacing dari 20 ke 15

        # Alamat (wrap text otomatis) - hanya jika ada
        if recipient_address and recipient_address.strip():
            words = recipient_address.split()
            line = ""
            for w in words:
                test = line + " " + w if line else w
                if len(test) <= max_chars:
                    line = test
                else:
                    draw.text((x, y), line, font=font_bold_small, fill=0)
                    y += 14  # Kurangi spacing dari 16 ke 14
                    line = w
            if line:
                draw.text((x, y), line, font=font_bold_small, fill=0)
                y += 15  # Kurangi spacing dari 18 ke 15

        # HP penerima - hanya jika ada
        if recipient_phone and recipient_phone.strip():
            draw.text((x, y), f"HP: {recipient_phone}", font=font_bold_small, fill=0)
            y += 15  # Kurangi spacing dari 18 ke 15
        
        y += 15  # Kurangi spacing dari 20 ke 15

    # ======= Bagian Pengirim =======
    draw.text((x, y), "PENGIRIM:", font=font_bold_small, fill=0)
    y += 15  # Kurangi spacing dari 18 ke 15
    draw.text((x, y), sender_name, font=font_bold_medium, fill=0)
    y += 15  # Kurangi spacing dari 18 ke 15
    draw.text((x, y), f"HP: {sender_phone}", font=font_bold_small, fill=0)
    y += 15  # Kurangi spacing dari 20 ke 15

    # ======= Bagian Resi/QR Code (Optional) =======
    if shipping_code and shipping_code.strip():
        y += 10  # Kurangi spacing dari 15 ke 10

        # Generate QR Code untuk resi
        qr = qrcode.QRCode(
            version=2 if label_size == "58mm" else 3,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3 if label_size == "58mm" else 4,
            border=1,
        )
        qr.add_data(shipping_code)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        
        # Posisi QR rata kiri (konsisten dengan text)
        qr_x = x  # Sama dengan posisi x text lainnya
        img.paste(qr_img, (qr_x, y))
        y += qr_size + 8  # Kurangi spacing dari 10 ke 8
        
        # Text resi di bawah QR (rata kiri)
        resi_label = "RESI:"
        draw.text((x, y), resi_label, font=font_bold_small, fill=0)  # Rata kiri, tidak center
        y += 14  # Kurangi spacing dari 16 ke 14
        
        # Resi code (rata kiri)
        draw.text((x, y), shipping_code, font=font_bold_medium, fill=0)  # Rata kiri, tidak center
        y += 15  # Kurangi spacing dari 20 ke 15

    # ======= Finishing =======
    # Crop area kosong agar tidak terlalu panjang
    img_cropped = img.crop((0, 0, label_width, min(y + 10, label_height)))

    # Generate filename berdasarkan ukuran dan ada tidaknya shipping code
    if shipping_code and shipping_code.strip():
        filename = f"thermal_label_{label_size}_{label_id}_{shipping_code}.bmp"
    else:
        filename = f"thermal_label_{label_size}_{label_id}_nocode.bmp"
    
    filepath = os.path.join(labels_dir, filename)
    img_cropped.save(filepath, format="BMP")

    return filepath
