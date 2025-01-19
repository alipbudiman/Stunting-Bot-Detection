import random

def convert_months_to_years(months):
    return float(months) / 12

class Messager:
    def __init__(self) -> None:
        pass
    
    def CognitiveImpairmentMessage(self, age):
        age = convert_months_to_years(age)
        if age < 1.0:return "Apakah anak Anda tidak memiliki respon yang baik jika diajak berkomunikasi dan tidak mengenali wajah ataupun suara orang terdekat (Orangtua) ?"
        if age >= 1.0 and age < 2.0:return "Apakah anak Anda belum mampu mengucap kata atau belum bisa makan sendiri?"
        if age >= 2.0 and age < 3.0:return "Apakah anak Anda belum dapat mengenali benda, baik bentuk, warna, ukuran ataupun rasa?"
        if age >= 3.0 and age < 4.0:return  "Apakah anak Anda Belum dapat mengenal konsep banyak dan sedikit ataupun belum mampu menempatkan benda dalam urutan ukuran (paling kecil - paling besar)?"
        if age >= 4.0 and age < 5.0:return "Apakah anak Anda Belum mampu mengenal benda berdasarkan fungsi, bentuk atau warna atau ukuran (seperti pisau untuk memotong, pensil untuk menulis)?"
        if age >= 5.0:return "Apakah anak Anda belum mampu menunjukkan aktivitas yang bersifat eksploratif dan menyelidik atau mengenal sebab-akibat tentang lingkungannya (seperti: apa yang terjadi ketika air ditumpahkan) atau belum dapat menunjukkan inisiatif dalam memilih tema permainan (seperti: ”ayo kita bermain pura-pura seperti harimau”)?"

    
    def StuntingSolution(self, age, stunting_precentage):
        age = convert_months_to_years(age)
        if age < 1.0:
            narasi_list = [
                "Memberikan stimulasi dini perkembangan bayi sangat penting, terutama jika panjang badan lahir atau stunting telah terdeteksi. ASI eksklusif harus diberikan hingga bayi berusia 6 bulan, dan setelah itu dilanjutkan dengan ASI serta Makanan Pendamping ASI (MPASI). Jangan lupa untuk melakukan konsultasi kesehatan anak secara rutin di Posyandu, Puskesmas, atau fasilitas kesehatan terdekat.",
                
                "Jika bayi menunjukkan tanda-tanda stunting atau memiliki panjang badan lahir yang kurang optimal, stimulasi dini perkembangan sangat diperlukan. Bayi sebaiknya mendapatkan ASI eksklusif selama 6 bulan pertama, diikuti dengan pemberian MPASI bersamaan dengan ASI. Selalu periksakan kesehatan anak secara rutin di Posyandu, Puskesmas, atau pusat kesehatan terdekat.",
                
                "Stimulasi dini pada bayi, terutama jika panjang badan lahir rendah atau risiko stunting muncul, sangat penting. Selama 6 bulan pertama, bayi perlu diberi ASI eksklusif, lalu dilanjutkan dengan pemberian MPASI sambil tetap memberikan ASI. Jangan lupa untuk rutin memeriksakan anak di Posyandu, Puskesmas, atau pusat pelayanan kesehatan.",
                
                "Penting untuk memberikan stimulasi dini perkembangan bayi, terutama jika bayi mengalami masalah panjang badan lahir atau stunting. ASI eksklusif harus diberikan hingga usia 6 bulan, dan setelahnya, bayi juga perlu mendapatkan MPASI sambil tetap melanjutkan ASI. Konsultasi kesehatan anak di Posyandu, Puskesmas, atau fasilitas kesehatan terdekat harus dilakukan secara rutin.",
                
                "Stimulasi dini pada bayi, khususnya yang memiliki panjang badan lahir rendah atau risiko stunting, perlu dilakukan. ASI eksklusif diberikan hingga 6 bulan, lalu dilanjutkan dengan MPASI bersama ASI. Selalu rutin konsultasi kesehatan anak di Posyandu, Puskesmas, atau pusat kesehatan.",
                
                "Apabila bayi terdeteksi mengalami masalah stunting atau panjang badan lahir yang kurang, stimulasi dini harus segera dilakukan. Berikan ASI eksklusif selama 6 bulan pertama, kemudian dilanjutkan dengan MPASI dan ASI. Rutin konsultasi kesehatan di Posyandu atau Puskesmas juga sangat penting.",
                
                "Untuk bayi yang memiliki panjang badan lahir rendah atau terdeteksi stunting, stimulasi dini perkembangan harus dilakukan. Berikan ASI eksklusif sampai bayi berusia 6 bulan, lalu mulai tambahkan MPASI sambil terus memberi ASI. Konsultasi kesehatan anak secara rutin di Posyandu atau Puskesmas perlu dilakukan.",
                
                "Melakukan stimulasi dini perkembangan bayi penting, terutama bagi bayi yang panjang badan lahirnya rendah atau berisiko stunting. ASI eksklusif diberikan hingga usia 6 bulan, kemudian dilanjutkan dengan MPASI bersama ASI. Pastikan juga anak rutin diperiksa di Posyandu, Puskesmas, atau fasilitas kesehatan terdekat.",
                
                "Bayi yang memiliki panjang badan lahir kurang atau terdeteksi stunting memerlukan stimulasi dini perkembangan. ASI eksklusif diberikan sampai usia 6 bulan, dan setelah itu dilanjutkan dengan MPASI serta ASI. Jangan lupa untuk selalu melakukan konsultasi rutin kesehatan anak di Posyandu atau Puskesmas.",
                
                "Jika bayi mengalami masalah panjang badan lahir atau stunting, stimulasi dini sangat dibutuhkan. ASI eksklusif harus diberikan selama 6 bulan, diikuti dengan pemberian MPASI dan ASI. Pastikan anak rutin diperiksakan di Posyandu atau Puskesmas untuk memantau kesehatannya."
            ]
        elif age <= 2.0:
            narasi_list = [
                "Berikan ASI bersama dengan Makanan Pendamping ASI (MPASI) untuk memenuhi kebutuhan nutrisi anak. Jangan lupa untuk memastikan asupan protein harian anak terpenuhi, yaitu sekitar 1,2 gram per kilogram berat badan. Lakukan konsultasi kesehatan anak secara rutin di Posyandu, Puskesmas, atau pusat pelayanan kesehatan untuk memastikan perawatan dan pelayanan kesehatan yang optimal.",
                
                "Pemberian ASI bersamaan dengan Makanan Pendamping ASI (MPASI) sangat penting bagi perkembangan anak. Asupan protein harian anak juga harus diperhatikan, dengan jumlah 1,2 gram per kilogram berat badan. Pastikan anak mendapat perawatan kesehatan terbaik dengan melakukan konsultasi rutin di Posyandu atau Puskesmas.",
                
                "ASI bersama MPASI harus diberikan secara teratur untuk mendukung tumbuh kembang anak. Selain itu, pastikan anak mendapatkan asupan protein harian sebanyak 1,2 gram per kilogram berat badan. Jangan lupa untuk melakukan konsultasi kesehatan secara rutin di Posyandu atau Puskesmas agar anak mendapatkan perawatan yang optimal.",
                
                "Penting untuk memberikan ASI bersama dengan MPASI setelah usia 6 bulan. Asupan protein harian anak juga perlu diperhatikan, yaitu sekitar 1,2 gram per kilogram berat badan. Pastikan anak mendapatkan pelayanan kesehatan yang optimal dengan melakukan konsultasi rutin di Posyandu atau Puskesmas.",
                
                "Setelah usia 6 bulan, berikan ASI bersama MPASI untuk memenuhi kebutuhan nutrisi anak. Selain itu, berikan protein harian sekitar 1,2 gram per kilogram berat badan anak. Rutin melakukan konsultasi di Posyandu atau Puskesmas penting agar anak mendapatkan perawatan kesehatan yang terbaik.",
                
                "Pemberian ASI bersama MPASI merupakan langkah penting untuk menjaga kesehatan anak. Pastikan juga anak mendapatkan asupan protein harian sebesar 1,2 gram per kilogram berat badan. Konsultasi rutin di Posyandu atau Puskesmas sangat dianjurkan untuk memberikan perawatan dan pelayanan kesehatan yang maksimal.",
                
                "MPASI harus diberikan bersamaan dengan ASI untuk memenuhi kebutuhan nutrisi anak. Selain itu, perhatikan asupan protein harian anak dengan jumlah 1,2 gram per kilogram berat badan. Konsultasi kesehatan secara rutin di Posyandu atau Puskesmas sangat penting untuk memastikan perawatan kesehatan anak berjalan dengan baik.",
                
                "ASI bersama MPASI perlu diberikan kepada anak setelah usia 6 bulan. Anak juga harus mendapatkan asupan protein sebanyak 1,2 gram per kilogram berat badan setiap hari. Lakukan pemeriksaan kesehatan secara rutin di Posyandu atau Puskesmas untuk memastikan anak tumbuh dengan sehat dan optimal.",
                
                "Berikan ASI dan MPASI secara teratur untuk memenuhi kebutuhan gizi anak. Juga pastikan bahwa anak menerima protein harian sebesar 1,2 gram per kilogram berat badannya. Rutin konsultasi ke Posyandu atau Puskesmas sangat penting agar anak mendapatkan pelayanan kesehatan yang baik.",
                
                "Setelah anak mulai mengonsumsi MPASI bersama ASI, pastikan juga bahwa asupan protein harian tercukupi sebesar 1,2 gram per kilogram berat badan. Konsultasi kesehatan anak di Posyandu atau Puskesmas harus dilakukan secara rutin agar anak memperoleh perawatan yang optimal."
            ]

        elif age > 2.0:
            narasi_list = [
                "Pemberian nutrisi yang cukup sesuai dengan usia anak sangat penting. Selain itu, pastikan anak mengonsumsi susu pertumbuhan dan mendapatkan variasi makanan sehat yang beragam, seperti serealia, kacang-kacangan, produk olahan susu, telur, atau sumber protein lainnya. Jangan lupa untuk rutin memeriksakan kesehatan anak di Posyandu atau Puskesmas guna memastikan perawatan yang optimal.",
                
                "Untuk mendukung tumbuh kembang anak, berikan nutrisi yang cukup sesuai usianya, termasuk konsumsi susu pertumbuhan. Pastikan juga anak mendapatkan variasi makanan sehat, seperti serealia, kacang-kacangan, telur, dan makanan kaya vitamin. Konsultasi rutin di Posyandu atau Puskesmas penting untuk memantau kesehatan anak.",
                
                "Nutrisi yang cukup sesuai usia anak harus diberikan, termasuk susu pertumbuhan untuk mendukung kesehatan mereka. Selain itu, berikan variasi makanan sehat seperti serealia, kacang-kacangan, telur, dan sumber vitamin A. Lakukan pemeriksaan kesehatan secara rutin di Posyandu atau Puskesmas untuk memastikan perawatan optimal.",
                
                "Anak perlu mendapatkan nutrisi yang cukup, sesuai dengan usianya, dan konsumsi susu pertumbuhan juga sangat dianjurkan. Makanan yang sehat dan beragam seperti serealia, kacang-kacangan, produk susu, dan telur juga perlu diberikan. Jangan lupa untuk rutin berkonsultasi di Posyandu atau Puskesmas untuk memantau kesehatan anak.",
                
                "Berikan nutrisi yang tepat sesuai dengan usia anak, dan tambahkan konsumsi susu pertumbuhan. Variasi makanan sehat seperti serealia, kacang-kacangan, dan makanan kaya vitamin harus selalu ada dalam menu harian anak. Pastikan anak mendapatkan perawatan kesehatan yang optimal dengan rutin berkonsultasi di Posyandu atau Puskesmas.",
                
                "Nutrisi yang sesuai usia anak sangat penting, termasuk konsumsi susu pertumbuhan. Berikan juga makanan yang bervariasi, seperti serealia, kacang-kacangan, dan makanan yang mengandung vitamin A. Jangan lupa untuk rutin membawa anak ke Posyandu atau Puskesmas untuk pemeriksaan kesehatan secara berkala.",
                
                "Untuk mendukung perkembangan anak, pastikan ia menerima nutrisi yang cukup sesuai dengan usianya dan konsumsi susu pertumbuhan. Variasikan makanannya dengan serealia, kacang-kacangan, produk susu, dan sumber protein lain. Rutin berkonsultasi di Posyandu atau Puskesmas sangat penting untuk memastikan kesehatan anak terjaga.",
                
                "Anak memerlukan nutrisi yang tepat sesuai usianya, termasuk susu pertumbuhan untuk mendukung perkembangan optimal. Berikan variasi makanan sehat, seperti serealia, kacang-kacangan, telur, dan produk kaya vitamin. Rutin konsultasi di Posyandu atau Puskesmas sangat dianjurkan untuk memastikan kesehatan anak selalu terpantau.",
                
                "Nutrisi yang mencukupi sesuai dengan usia anak harus diberikan, termasuk susu pertumbuhan dan makanan yang bervariasi seperti serealia, kacang-kacangan, dan sumber protein lainnya. Jangan lupa untuk rutin memeriksakan kesehatan anak di Posyandu atau Puskesmas untuk memastikan perawatan yang optimal.",
                
                "Berikan nutrisi yang cukup sesuai dengan usia anak, konsumsi susu pertumbuhan, serta variasi makanan sehat seperti serealia, kacang-kacangan, dan produk olahan susu. Pemeriksaan rutin di Posyandu atau Puskesmas sangat penting untuk menjaga kesehatan anak dan memberikan perawatan yang optimal."
            ]
        
        data = "Anak anda mengalami Stunting\n\nSolusi yang saya barikan:\n"
        data += random.choice(narasi_list)
        return data
            
