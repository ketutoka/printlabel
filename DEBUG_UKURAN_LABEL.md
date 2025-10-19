# Debug Kolom Ukuran Label

## Masalah
Kolom "Ukuran" di Riwayat Label hanya menampilkan 58mm walaupun di database ada field `label_size` dengan nilai 80mm.

## Kemungkinan Penyebab

1. **Migration belum dijalankan** - Kolom `label_size` belum ada di database
2. **Data lama tidak memiliki `label_size`** - Menggunakan default "58mm" 
3. **Semua data memang berukuran 58mm** - User belum pernah membuat label 80mm

## Langkah Debug

### 1. Cek struktur database
```bash
cd backend
python debug_label_sizes.py
```

### 2. Jalankan migration (jika kolom belum ada)
```bash
cd backend
python migrate_optional_fields.py
```

### 3. Update beberapa data untuk testing (jika semua 58mm)
```bash
cd backend 
python update_sample_80mm.py
```

### 4. Refresh browser dan cek console log
Buka Developer Tools → Console, lalu refresh Dashboard untuk melihat data label.

## Perbaikan Frontend

Saya sudah menambahkan debug di:

1. **Console log di `recentLabels` computed property** - untuk melihat data mentah dari API
2. **Template debug di kolom Ukuran** - menampilkan nilai `label_size` asli instead of icon

## Hasil Yang Diharapkan

Setelah debug:
- Console log menunjukkan mix `label_size: "58mm"` dan `label_size: "80mm"`
- Kolom Ukuran menampilkan "58mm" dan "80mm" sesuai data
- Tag hijau untuk 58mm, kuning untuk 80mm

## Rollback Debug (setelah fix)

Setelah masalah teridentifikasi, hapus:
1. Console.log di `recentLabels` 
2. Kembalikan template icon: `{{ scope.row.label_size === '58mm' ? '📱 58mm' : '🖨️ 80mm' }}`