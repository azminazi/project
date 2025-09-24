PERANCANGAN SISTEM DETEKSI TRAFFIC COUNTING MENGGUNAKAN YOLO VERSI 4

Penelitian ini bertujuan untuk mengembangkan sistem deteksi dan penghitungan jenis kendaraan secara otomatis menggunakan algoritma YOLO (You Only Look Once) berbasis video, guna menggantikan metode manual yang memakan waktu dan biaya. Sistem ini dirancang untuk mengenali 8 kelas kendaraan sesuai klasifikasi Bina Marga dan diuji menggunakan YOLOv4. Berdasarkan hasil evaluasi, YOLOv4 memperoleh mAP 78%. Model yang telah dilatih kemudian diimplementasikan ke dalam situs web menggunakan framework Flask.

Cara menjalankan project ini adalah sebagai berikut.
1. Download project ke komputer lokal
2. Jalankan folder pada kode editor
3. Pada terminal kode editor, jalankan perintah python app.py
4. Ikuti perintah pada terminal kode editor
5. Komputer akan menjalankan website sistem deteksi jenis kendaraan

Jika website berhasil dijalankan, berikut adalah cara menjalankan website sistem deteksi jenis kendaraan.
1. Klik tombol Choose File
2. Pilih video yang mau dideteksi dan pilih Open
3. Kemudian klik tombol Proses
4. Tunggu sampai sistem selesai mendeteksi video
5. Setelah video berhasil dideteksi, halaman akan berpindah secara otomatis ke Hasil Deteksi

Perlu diperhatikan!

Sistem hanya akan menghitung kendaraan yang berjalan dari atas video ke bawah video. Untuk mendapatkan hasil yang maksimal, kualitas video yang digunakan, baik pada siang maupun malam hari, harus memenuhi standar tertentu. Pada kondisi siang hari, pencahayaan alami membantu sistem mengenali objek dengan lebih mudah, sehingga video dengan resolusi minimal 720p atau idealnya 1080p (Full HD) dan frame rate antara 15 hingga 30 fps untuk menangkap detail kendaraan dengan jelas. Sebaliknya, pada malam hari, video sebaiknya memiliki resolusi minimal 1080p, dengan tingkat kecerahan dan kontras yang cukup tinggi agar kendaraan dapat dibedakan dari latar belakang yang gelap. Frame rate minimal 15 fps untuk menghindari blur pada objek yang bergerak. Selain itu, video harus mampu menangani perbedaan cahaya ekstrem, seperti sorotan lampu kendaraan, tanpa menyebabkan overexposure.
