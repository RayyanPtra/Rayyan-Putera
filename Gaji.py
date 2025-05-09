import csv
import os
from datetime import datetime

DATA_FILE = 'gaji_pegawai.csv'

def load_data():
    """Load data from the CSV file."""
    data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error membaca file data: {e}")
    return data

def save_data(data):
    """Save data to the CSV file."""  
    try:
        with open(DATA_FILE, mode='w', newline='') as file:
            fieldnames = ['NoPegawai', 'NamaPegawai', 'JenisKelamin', 'TanggalAwal', 'TanggalAkhir', 'GajiPerHari']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

 
    except Exception as e:
        print(f"Error menyimpan data: {e}")

def view_data(data):
    """Display the salary data in a formatted table."""  
    if not data:
        print("Data gaji pegawai kosong.")
        return
    print(f"{'NoPegawai':<12} {'NamaPegawai':<20} {'JenisKelamin':<12} {'TanggalAwal':<12} {'TanggalAkhir':<12} {'GajiPerHari':<15} {'TotalGaji':<12}")
    print("-" * 100)
    for row in data:
        total_gaji = calculate_total_gaji(row['TanggalAwal'], row['TanggalAkhir'], float(row['GajiPerHari']))
        print(f"{row['NoPegawai']:<12} {row['NamaPegawai']:<20} {row.get('JenisKelamin', ''):<12} {row['TanggalAwal']:<12} {row['TanggalAkhir']:<12} {row['GajiPerHari']:<15} {total_gaji:<12.2f}")

def add_data(data):
    """Add a new employee salary record."""  
    while True:
        no_pegawai = input("Masukkan No.Pegawai: ")
        if any(row['NoPegawai'] == no_pegawai for row in data):
            print("No.Pegawai sudah ada. Silakan masukkan No.Pegawai lain.")
        else:
            break
    nama_pegawai = input("Masukkan Nama Pegawai: ")
    while True:
        jenis_kelamin = input("Masukkan Jenis Kelamin (L/P): ").upper()
        if jenis_kelamin not in ['L', 'P']:
            print("Jenis Kelamin harus 'L' atau 'P'.")
            continue
        break
    while True:
        tanggal_awal = input("Masukkan Tanggal Awal (YYYY-MM-DD): ")
        if not validate_date(tanggal_awal):
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
            continue
        break
    while True:
        tanggal_akhir = input("Masukkan Tanggal Akhir (YYYY-MM-DD): ")
        if not validate_date(tanggal_akhir):
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
            continue
        if not validate_date_order(tanggal_awal, tanggal_akhir):
            print("Tanggal Akhir harus sama atau setelah Tanggal Awal.")
            continue
        break
    while True:
        gaji_per_hari = input("Masukkan Gaji Perhari: ")
        if not is_valid_decimal(gaji_per_hari):
            print("Gaji Perhari harus berupa angka yang valid.")
            continue
        break
    data.append({
        'NoPegawai': no_pegawai,
        'NamaPegawai': nama_pegawai,
        'JenisKelamin': jenis_kelamin,
        'TanggalAwal': tanggal_awal,
        'TanggalAkhir': tanggal_akhir,
        'GajiPerHari': gaji_per_hari
    })
    save_data(data)
    print("Data berhasil ditambahkan.")

def edit_data(data):
    """Edit an existing employee salary record."""  
    no_pegawai = input("Masukkan No.Pegawai yang akan diedit: ")
    for row in data:
        if row['NoPegawai'] == no_pegawai:
            print(f"Data ditemukan: {row}")
            nama_pegawai = input(f"Masukkan Nama Pegawai baru [{row['NamaPegawai']}]: ") or row['NamaPegawai']
            while True:
                jenis_kelamin = input(f"Masukkan Jenis Kelamin baru (L/P) [{row.get('JenisKelamin', '')}]: ").upper() or row.get('JenisKelamin', '')
                if jenis_kelamin not in ['L', 'P', '']:
                    print("Jenis Kelamin harus 'L' atau 'P'.")
                    continue
                break
            while True:
                tanggal_awal = input(f"Masukkan Tanggal Awal baru (YYYY-MM-DD) [{row['TanggalAwal']}]: ") or row['TanggalAwal']
                if not validate_date(tanggal_awal):
                    print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
                    continue
                break
            while True:
                tanggal_akhir = input(f"Masukkan Tanggal Akhir baru (YYYY-MM-DD) [{row['TanggalAkhir']}]: ") or row['TanggalAkhir']
                if not validate_date(tanggal_akhir):
                    print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
                    continue
                if not validate_date_order(tanggal_awal, tanggal_akhir):
                    print("Tanggal Akhir harus sama atau setelah Tanggal Awal.")
                    continue
                break
            while True:
                gaji_per_hari = input(f"Masukkan Gaji Perhari baru [{row['GajiPerHari']}]: ") or row['GajiPerHari']
                if not is_valid_decimal(gaji_per_hari):
                    print("Gaji Perhari harus berupa angka yang valid.")
                    continue
                break
            row['NamaPegawai'] = nama_pegawai
            row['JenisKelamin'] = jenis_kelamin
            row['TanggalAwal'] = tanggal_awal
            row['TanggalAkhir'] = tanggal_akhir
            row['GajiPerHari'] = gaji_per_hari
            save_data(data)
            print("Data berhasil diupdate.")
            return
    print("No.Pegawai tidak ditemukan.")

def delete_data(data):
    """Delete an employee salary record."""
    no_pegawai = input("Masukkan No.Pegawai yang akan dihapus: ")
    for i, row in enumerate(data):
        if row['NoPegawai'] == no_pegawai:
            confirm = input(f"Yakin ingin menghapus data {row['NamaPegawai']}? (y/n): ")
            if confirm.lower() == 'y':
                data.pop(i)
                save_data(data)
                print("Data berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
            return
    print("No.Pegawai tidak ditemukan.")

def search_data(data):
    """Search employee data by NoPegawai or NamaPegawai."""  
    keyword = input("Masukkan No.Pegawai atau Nama Pegawai yang dicari: ").lower()
    results = [row for row in data if keyword in row['NoPegawai'].lower() or keyword in row['NamaPegawai'].lower()]
    if not results:
        print("Data tidak ditemukan.")
        return
    print(f"{'NoPegawai':<12} {'NamaPegawai':<20} {'JenisKelamin':<12} {'TanggalAwal':<12} {'TanggalAkhir':<12} {'GajiPerHari':<15} {'TotalGaji':<12}")
    print("-" * 100)
    for row in results:
        total_gaji = calculate_total_gaji(row['TanggalAwal'], row['TanggalAkhir'], float(row['GajiPerHari']))
        print(f"{row['NoPegawai']:<12} {row['NamaPegawai']:<20} {row.get('JenisKelamin', ''):<12} {row['TanggalAwal']:<12} {row['TanggalAkhir']:<12} {row['GajiPerHari']:<15} {total_gaji:<12.2f}")

def calculate_total_gaji(tanggal_awal, tanggal_akhir, gaji_per_hari):
    """Calculate total salary based on date range and daily salary."""
    try:
        start_date = datetime.strptime(tanggal_awal, "%Y-%m-%d")
        end_date = datetime.strptime(tanggal_akhir, "%Y-%m-%d")
        delta = (end_date - start_date).days + 1
        if delta < 0:
            return 0
        return delta * gaji_per_hari
    except Exception:
        return 0

def validate_date(date_text):
    """Validate date format YYYY-MM-DD."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_date_order(start_date_text, end_date_text):
    """Validate that end date is same or after start date."""
    try:
        start_date = datetime.strptime(start_date_text, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_text, "%Y-%m-%d")
        return end_date >= start_date
    except ValueError:
        return False

def is_valid_decimal(value):
    """Check if the value is a valid decimal number."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def main_menu():
    """Main menu for managing employee salary data."""
    data = load_data()
    while True:
        print("\nMenu Pengelolaan Gaji Pegawai")
        print("1. Lihat Data Gaji Pegawai")
        print("2. Tambah Data Gaji Pegawai")
        print("3. Edit Data Gaji Pegawai")
        print("4. Hapus Data Gaji Pegawai")
        print("5. Cari Data Gaji Pegawai")
        print("6. Keluar")
        choice = input("Pilih menu (1-6): ")
        if choice == '1':
            view_data(data)
        elif choice == '2':
            add_data(data)
        elif choice == '3':
            edit_data(data)
        elif choice == '4':
            delete_data(data)
        elif choice == '5':
            search_data(data)
        elif choice == '6':
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main_menu()
    