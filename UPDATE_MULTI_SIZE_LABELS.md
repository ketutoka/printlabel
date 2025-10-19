# 📏 Update: Multi-Size Label Support (58mm & 80mm)

## 🎯 **Fitur Baru Yang Ditambahkan**

### **Opsi Ukuran Label**
Aplikasi sekarang mendukung **2 ukuran thermal printer**:
- **58mm** - Thermal mini (203px width) 
- **80mm** - Thermal standar (284px width)

---

## 🔧 **Frontend Changes**

### 1. **CreateShippingLabel.vue**
- ✅ **Radio button selector** untuk ukuran label (58mm/80mm)
- ✅ **Visual design** dengan icon dan deskripsi
- ✅ **Default selection**: 58mm
- ✅ **Responsive layout** untuk mobile dan desktop
- ✅ **Validation rules** untuk ukuran label
- ✅ **Reset form** include label_size

### 2. **Form Data Structure**
```javascript
shippingForm = {
  sender_name: '',
  sender_phone: '',
  recipient_name: '',     // Optional
  recipient_address: '',  // Optional  
  recipient_phone: '',    // Optional
  shipping_code: '',      // Optional
  label_size: '58mm'      // NEW: Default 58mm
}
```

### 3. **UI Components**
- ✅ **Radio Button Group** dengan style custom
- ✅ **Visual feedback** saat hover dan selected
- ✅ **Icon indicators**: 📱 untuk 58mm, 🖨️ untuk 80mm
- ✅ **Descriptive text**: "Thermal mini" vs "Thermal standar"

---

## 🔧 **Backend Changes**

### 1. **Schema (schemas.py)**
```python
class ShippingLabelCreate(BaseModel):
    # ... existing fields ...
    label_size: Optional[str] = "58mm"  # NEW

class ShippingLabelResponse(BaseModel):
    # ... existing fields ...
    label_size: Optional[str] = "58mm"  # NEW
```

### 2. **Model (models.py)**
```python
class ShippingLabel(Base):
    # ... existing columns ...
    label_size = Column(String(10), nullable=False, default="58mm")  # NEW
```

### 3. **CRUD (crud.py)**
- ✅ **create_shipping_label**: Include label_size field
- ✅ **Default handling**: Fallback ke "58mm" jika kosong

---

## 🏷️ **Smart Label Generator**

### **Adaptive Layout Engine**
Label generator sekarang **intelligently adapts** berdasarkan ukuran:

#### **58mm Labels (203px width)**:
- Font sizes: Large=13, Medium=11, Small=10
- QR Code: 60x60px dengan version=2, box_size=3
- Max characters per line: 28
- Compact layout optimized untuk space

#### **80mm Labels (284px width)**:
- Font sizes: Large=15, Medium=13, Small=11  
- QR Code: 80x80px dengan version=3, box_size=4
- Max characters per line: 38
- Expanded layout dengan more spacing

### **Layout Features**:
- ✅ **Header identifier**: "LABEL 58MM" atau "LABEL 80MM"
- ✅ **Separator lines**: Visual dividers antar section
- ✅ **Center-aligned elements**: QR code, resi text, tanggal
- ✅ **Dynamic height**: Auto-crop based on content
- ✅ **Smart spacing**: Proportional padding dan margins

---

## 📐 **Technical Specifications**

### **Label Dimensions**:
| Size | Width (mm) | Width (px) | DPI | Typical Use |
|------|------------|------------|-----|-------------|
| 58mm | 58         | 203        | 203 | Mobile, compact printers |
| 80mm | 80         | 284        | 203 | Standard thermal printers |

### **Font Scaling**:
| Element | 58mm Size | 80mm Size | Purpose |
|---------|-----------|-----------|---------|
| Large   | 13px      | 15px      | Headers, names |
| Medium  | 11px      | 13px      | Content text |
| Small   | 10px      | 11px      | Labels, metadata |

### **QR Code Specs**:
| Size | QR Dimensions | Version | Box Size | Error Correction |
|------|---------------|---------|----------|------------------|
| 58mm | 60x60px      | 2       | 3        | L (Low) |
| 80mm | 80x80px      | 3       | 4        | L (Low) |

---

## 🗄️ **Database Migration**

### **New Migration Script**: `migrate_optional_fields.py`
```sql
-- Make recipient fields nullable (previous)
ALTER TABLE shipping_labels ALTER COLUMN recipient_name DROP NOT NULL;
ALTER TABLE shipping_labels ALTER COLUMN recipient_address DROP NOT NULL;
ALTER TABLE shipping_labels ALTER COLUMN recipient_phone DROP NOT NULL;

-- Add label_size column (NEW)
ALTER TABLE shipping_labels ADD COLUMN label_size VARCHAR(10) NOT NULL DEFAULT '58mm';
```

### **Run Migration**:
```bash
cd backend
run-optional-migration.bat
# Or manually: python migrate_optional_fields.py
```

---

## 🎨 **Label Layout Examples**

### **58mm Label Layout**:
```
     LABEL 58MM
   ──────────────────
   KEPADA:
   John Doe
   Jl. Sudirman 123
   Jakarta 10110
   HP: 081234567890
   ──────────────────
   PENGIRIM:
   Jane Smith
   HP: 087654321098
   ──────────────────
      [QR 60x60]
       
       RESI:
    ABC123456789
   ──────────────────
    19/10/2025 14:30
```

### **80mm Label Layout**:
```
          LABEL 80MM
   ────────────────────────────────
   KEPADA:
   John Doe
   Jl. Sudirman No. 123, RT 01/RW 02
   Kelurahan Menteng, Jakarta Pusat 10110
   HP: 081234567890
   ────────────────────────────────
   PENGIRIM:
   Jane Smith Corporation
   HP: 087654321098
   ────────────────────────────────
         [QR 80x80]
          
          RESI:
       ABC123456789
   ────────────────────────────────
       19/10/2025 14:30
```

---

## 🎛️ **User Interface**

### **Label Size Selector**:
```
┌─────────────────┐  ┌─────────────────┐
│   📱 58mm       │  │   🖨️ 80mm      │
│ Thermal mini    │  │ Thermal standar │  
│   (203px)       │  │   (284px)       │
└─────────────────┘  └─────────────────┘
```

### **Responsive Behavior**:
- **Desktop**: Side-by-side radio buttons
- **Mobile**: Stacked vertically untuk easier selection
- **Visual feedback**: Hover effects dan selected states
- **Accessibility**: Clear labels dan keyboard navigation

---

## 🚀 **Benefits**

1. **Flexibility**: Support multiple printer types
2. **Quality**: Optimized layouts untuk each size
3. **User Choice**: Let user decide based on hardware
4. **Future Ready**: Easy to add more sizes (104mm, etc.)
5. **Professional**: Proper scaling dan proportions
6. **Backward Compatible**: Existing labels remain functional

---

## 📊 **Testing Scenarios**

### **Size Comparison Tests**:
1. **Same content, different sizes**:
   - Create label dengan 58mm → compact layout
   - Create label dengan 80mm → expanded layout
   - Compare readability dan proportions

2. **Content variations**:
   - **Minimal**: Hanya pengirim + 58mm
   - **Medium**: Pengirim + penerima + 80mm  
   - **Full**: All fields + resi + QR + either size

3. **Mobile responsive**:
   - Test radio button selection di mobile
   - Verify form layout pada small screens
   - Ensure preview works untuk both sizes

---

## 🛠️ **Implementation Status**

- ✅ **Frontend**: Radio selector implemented
- ✅ **Backend**: Schema, model, API updated
- ✅ **Label Generator**: Adaptive layouts ready
- ✅ **Database**: Migration script prepared
- 🔄 **Testing**: Ready for user testing
- 🔄 **Migration**: Needs to be executed

---

## 📞 **Next Steps**

1. **Run database migration**:
   ```bash
   cd backend
   run-optional-migration.bat
   ```

2. **Test both label sizes**:
   - Create 58mm label dengan content minimal
   - Create 80mm label dengan content lengkap
   - Verify layout proportions

3. **User acceptance testing**:
   - Test form responsiveness
   - Verify print quality pada actual printers
   - Confirm size selection UX

4. **Production deployment** setelah testing

---

**🎉 Multi-size label support is ready! Users can now choose between 58mm and 80mm thermal printers with optimized layouts for each size.**