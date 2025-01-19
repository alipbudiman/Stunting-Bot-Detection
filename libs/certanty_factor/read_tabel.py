import pandas as pd

class ReadTabel:
    def __init__(self) -> None:
        pass
    
    # Load data referensi stunting dari file CSV
    def load_rules(self, file_path):
        # Pastikan kolom USIA adalah numerik
        df = pd.read_csv(file_path)
        # Sesuaikan nama kolom dengan struktur yang diberikan
        df.columns = ['USIA', '-SD 3', '-SD 2', '-SD 1', 'Median', '+SD 1', '+SD 2', '+SD 3']
        df['USIA'] = pd.to_numeric(df['USIA'], errors='coerce')  # Ubah ke numerik untuk kolom 'USIA'
        return df


    # Fungsi untuk menemukan usia terdekat
    def find_closest_age(self, age, rules_df):
        # Cari usia yang terdekat
        closest_age = rules_df.iloc[(rules_df['USIA'] - age).abs().argmin()]
        return closest_age

    # Fungsi untuk menentukan status stunting
    def stunting_status_by_age_height(self, age, height, rules_df):
        # Cari usia terdekat dari tabel
        closest_age_row = self.find_closest_age(age, rules_df)
        
        # Tambahkan log untuk memeriksa data yang diambil
        print(f"Closest Age Row: {closest_age_row}")
        
        try:
            # Ambil batas tinggi badan dari baris yang sesuai
            sd_3 = closest_age_row['-SD 3']
            sd_2 = closest_age_row['-SD 2']
            sd_0 = closest_age_row['Median']
            sd_3_plus = closest_age_row['+SD 3']
        except KeyError as e:
            raise KeyError(f"Kolom yang diperlukan tidak ditemukan: {e}")

        # Tentukan status berdasarkan tinggi badan
        if height < sd_3:
            return 1  # Sangat Pendek
        elif sd_3 <= height < sd_2:
            return 0.8  # Pendek
        elif sd_2 <= height <= sd_3_plus:
            return 0.6  # Normal
        else:
            return 0.4  # Tinggi

    def load_rules2(self, file_path):
        df = pd.read_csv(file_path)
        # Atur ulang nama kolom secara manual sesuai dengan struktur data
        df.columns = ['Panjang Badan (cm)', '-3 SD', '-2 SD', '-1 SD', 'Median', '+1 SD', '+2 SD', '+3 SD']
        
        # Konversi semua kolom kecuali 'Panjang Badan (cm)' ke tipe float dan paksa konversi
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Ubah ke numerik, coerce ubah error jadi NaN
        
        return df

    # Fungsi untuk menemukan data tinggi badan terdekat
    def find_closest_height2(self, height, rules_df):
        # Pastikan kolom 'Panjang Badan (cm)' dikonversi menjadi tipe float
        rules_df['Panjang Badan (cm)'] = pd.to_numeric(rules_df['Panjang Badan (cm)'], errors='coerce')
        closest_row = rules_df.iloc[(rules_df['Panjang Badan (cm)'] - height).abs().argmin()]
        return closest_row

    # Fungsi untuk menentukan status gizi berdasarkan tinggi badan dan berat badan
    def nutrition_status(self, height, weight, rules_df):
        # Cari baris panjang badan terdekat
        closest_row = self.find_closest_height2(height, rules_df)
        
        # Ambil batas berat badan dari baris yang sesuai
        sd_3_minus = closest_row['-3 SD']
        sd_2_minus = closest_row['-2 SD']
        sd_1_plus = closest_row['+1 SD']
        sd_2_plus = closest_row['+2 SD']
        sd_3_plus = closest_row['+3 SD']

        # Tentukan status berdasarkan berat badan
        if weight < sd_3_minus:
            return 1  # Gizi Buruk
        elif sd_3_minus <= weight < sd_2_minus:
            return 0.8  # Gizi Kurang
        elif sd_2_minus <= weight <= sd_1_plus:
            return 0.6  # Gizi Baik
        elif sd_1_plus < weight <= sd_2_plus:
            return 0.4  # Berisiko Gizi Lebih
        elif sd_2_plus < weight <= sd_3_plus:
            return 0.2  # Gizi Lebih
        else:
            return 0.8  # Obesitas