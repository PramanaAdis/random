import firebase_admin
from firebase_admin import credentials, db
import random
import time

# --- Konfigurasi Firebase ---
# Ganti dengan kredensial dan URL database Anda
try:
    cred = credentials.Certificate('greenhouse.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://kondisigreenhouse-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
except Exception as e:
    print(f"Error inisialisasi Firebase: {e}\nPastikan path kredensial dan URL database sudah benar.")
    exit()


# Langsung menunjuk ke path '/sensor'
ref = db.reference('/sensor')

# --- Konfigurasi Sensor dengan Waktu Random Individual ---
# 'min_interval': Jeda waktu minimum (detik) sebelum update berikutnya
# 'max_interval': Jeda waktu maksimum (detik) sebelum update berikutnya
sensors_config = {
    'suhu_air': {
        'min_interval': 20,
        'max_interval': 40,
        'value_func': lambda: round(random.uniform(22.1, 22.5), 1),
        'next_update': time.time() # Waktu update berikutnya (diinisialisasi sekarang)
    },
    'ph_air': {
        'min_interval': 360,
        'max_interval': 500,
        'value_func': lambda: round(random.uniform(6.1, 6.3), 1),
        'next_update': time.time()
    },
    'cahaya': {
        'min_interval': 35,
        'max_interval': 50,
        'value_func': lambda: random.randint(70, 75),
        'next_update': time.time()
    },
    'co2': {
        'min_interval': 20,
        'max_interval': 40,
        'value_func': lambda: random.randint(996, 1015),
        'next_update': time.time()
    }
}


def main():
    """
    Loop utama untuk memeriksa dan memperbarui setiap sensor
    berdasarkan interval waktunya masing-masing.
    """
    print("Memulai pengiriman data sensor dengan interval individual...")
    while True:
        try:
            # Dapatkan waktu saat ini sekali per iterasi loop
            current_time = time.time()

            # Periksa setiap sensor dalam konfigurasi
            for sensor_name, config in sensors_config.items():
                
                # Cek apakah sudah waktunya untuk update sensor ini
                if current_time >= config['next_update']:
                    # 1. Hasilkan nilai baru
                    new_value = config['value_func']()

                    # 2. Update nilai di Firebase
                    ref.update({sensor_name: new_value})
                    print(f"✅ [{sensor_name}] diperbarui -> {new_value}")

                    # 3. Jadwalkan ulang waktu update berikutnya
                    random_interval = random.randint(config['min_interval'], config['max_interval'])
                    config['next_update'] = current_time + random_interval
                    print(f"   -> Update berikutnya dalam {random_interval} detik.")

            # Beri jeda singkat agar loop tidak memakai 100% CPU
            time.sleep(1)

        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh pengguna.")
            break
        except Exception as e:
            print(f"\nTerjadi error: {e}")
            time.sleep(10) # Tunggu sebentar sebelum mencoba lagi

if __name__ == '__main__':
    main()