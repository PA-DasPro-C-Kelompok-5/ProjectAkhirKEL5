import json
import os
import pwinput 
from prettytable import PrettyTable  
from datetime import datetime, timedelta  

def muat_data(nama_file, data_default=None):
    if os.path.exists(nama_file):
        with open(nama_file, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error membaca file {nama_file}. Format JSON mungkin salah.")
                return data_default if data_default else {}
    else:
        if data_default is not None:
            with open(nama_file, 'w') as file:
                json.dump(data_default, file, indent=4)
        return data_default if data_default else {}


def simpan_data(nama_file, data):
    with open(nama_file, 'w') as file:
        json.dump(data, file, indent=4)

def registrasi_pengguna(pengguna):
    print("\n--- Registrasi Pengguna ---")
    username = input("Masukkan username: ")
    if username in pengguna:
        print("Username sudah terdaftar!")
        return pengguna
    password = pwinput.pwinput("Masukkan password: ")  
    pengguna[username] = {"password": password, "role": "user", "saldo": 0.0}  
    simpan_data('pengguna.json', pengguna)
    print("Registrasi berhasil!")
    return pengguna

def login(pengguna, role):
    print(f"\n--- Login {role} ---")
    username = input("Masukkan username: ")
    password = pwinput.pwinput("Masukkan password: ")  

    if username in pengguna and pengguna[username]["password"] == password and pengguna[username]["role"] == role:
        return username
    else:
        print("Username atau password salah!")
        return None
    
def ubah_status_transaksi(transaksi):
    print("\n--- Ubah Status Transaksi ---")
    table = PrettyTable()
    table.field_names = ["No", "Username", "Layanan", "Status", "Biaya"]

    if transaksi:
        for idx, txn in enumerate(transaksi, 1):
            table.add_row([idx, txn['username'], txn['service'], txn['status'], txn['biaya']])
        print(table)
        
        try:
            nomor = int(input("Masukkan nomor transaksi yang ingin diubah statusnya: "))
            if 1 <= nomor <= len(transaksi):
                txn = transaksi[nomor - 1]
                print(f"Transaksi yang dipilih: {txn['username']} - {txn['service']} (Status: {txn['status']})")
                
                print("\nPilihan Status Transaksi:")
                print("1. Sedang Diproses")
                print("2. Selesai")
                print("3. Batal")
                pilihan_status = input("Masukkan pilihan status (1/2/3): ")

                if pilihan_status == '1':
                    txn['status'] = "Sedang Diproses"
                elif pilihan_status == '2':
                    txn['status'] = "Selesai"
                elif pilihan_status == '3':
                    txn['status'] = "Batal"
                else:
                    print("Pilihan tidak valid.")
                    return
                
                simpan_data('transaksi.json', transaksi)
                print(f"Status transaksi untuk {txn['username']} berhasil diubah menjadi: {txn['status']}")
            else:
                print("Nomor transaksi tidak valid!")
        except ValueError:
            print("Masukkan nomor transaksi yang valid!")


def menu_admin(pengguna, transaksi, layanan):
    while True:
        print("\n--- Menu Admin ---")
        print("1. Lihat Semua Transaksi")
        print("2. Input layanan Baru")
        print("3. Lihat Daftar layanan")
        print("4. Edit layanan")
        print("5. Hapus layanan")
        print("6. Ubah Status Transaksi")  
        print("7. Logout")
        pilihan = input("Pilih opsi: ")

        if pilihan == '1':
            for username in pengguna:
                lihat_status_transaksi(username, transaksi)  
        elif pilihan == '2':
            input_layanan(layanan)
        elif pilihan == '3':
            lihat_layanan(layanan)
        elif pilihan == '4':
            edit_layanan(layanan)
        elif pilihan == '5':
            hapus_layanan(layanan)
        elif pilihan == '6':
            ubah_status_transaksi(transaksi)  
        elif pilihan == '7':
            break
        else:
            print("Pilihan tidak valid!")

def input_layanan(layanan):
    print("\n--- Input layanan Baru ---")
    nama_layanan = input("Masukkan nama layanan: ")
    harga = input("Masukkan harga layanan per kg: ")
    estimasi_waktu = input("Masukkan estimasi waktu pengerjaan (misalnya: 1 hari): ")

    if not estimasi_waktu.endswith("hari"):
        estimasi_waktu = estimasi_waktu + " hari"
    
    layanan[nama_layanan] = {"harga": harga, "estimasi_waktu": estimasi_waktu}
    simpan_data('layanan.json', layanan)
    print(f"Layanan '{nama_layanan}' berhasil ditambahkan dengan estimasi waktu: {estimasi_waktu}")

def lihat_layanan(layanan):
    print("\n--- Daftar layanan ---")
    table = PrettyTable()
    table.field_names = ["No", "Nama Layanan", "Harga per kg", "Estimasi Waktu"]

    if layanan:
        for idx, (nama_layanan, detail) in enumerate(layanan.items(), 1):  
            if isinstance(detail, dict):   
                table.add_row([idx, nama_layanan, detail.get("harga", "N/A"), detail.get("estimasi_waktu", "N/A")])
            else:
                print(f"Data untuk layanan {nama_layanan} tidak valid.")
        print(table)
    else:
        print("Tidak ada layanan yang terdaftar.")

def edit_layanan(layanan):
    print("\n--- Edit layanan ---")
    lihat_layanan(layanan) 
    try:
        nomor = int(input("Masukkan nomor layanan yang ingin diedit: "))
        if 1 <= nomor <= len(layanan):
            nama_layanan = list(layanan.keys())[nomor - 1]
            harga_baru = input(f"Masukkan harga baru untuk layanan '{nama_layanan}': ")
            estimasi_waktu_baru = input(f"Masukkan estimasi waktu baru untuk layanan '{nama_layanan}': ")

            if not estimasi_waktu_baru.endswith("hari"):
                estimasi_waktu_baru = estimasi_waktu_baru + " hari"

            layanan[nama_layanan] = {"harga": harga_baru, "estimasi_waktu": estimasi_waktu_baru}
            simpan_data('layanan.json', layanan)
            print(f"Layanan '{nama_layanan}' berhasil diperbarui dengan estimasi waktu baru: {estimasi_waktu_baru}")
        else:
            print("Nomor layanan tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")

def hapus_layanan(layanan):
    print("\n--- Hapus layanan ---")
    lihat_layanan(layanan)  
    try:
        nomor = int(input("Masukkan nomor layanan yang ingin dihapus: "))
        if 1 <= nomor <= len(layanan):
            nama_layanan = list(layanan.keys())[nomor - 1]
            del layanan[nama_layanan]
            simpan_data('layanan.json', layanan)
            print(f"Layanan '{nama_layanan}' berhasil dihapus!")
        else:
            print("Nomor layanan tidak valid!")
    except ValueError:
        print("Masukkan angka yang valid!")

def lihat_status_transaksi(username, transaksi):
    print(f"\n--- Status Transaksi untuk Pengguna: {username} ---")
    table = PrettyTable()
    table.field_names = ["No", "Layanan", "Status", "Biaya"]

    transaksi_pengguna = [txn for txn in transaksi if txn["username"] == username]

    if transaksi_pengguna:
        for idx, txn in enumerate(transaksi_pengguna, 1):  
            table.add_row([idx, txn['service'], txn['status'], txn['biaya']])
        print(table)
    else:
        print("Anda belum melakukan transaksi apapun.")
def lihat_layanan_urutkan(layanan):
    print("\n--- Daftar layanan Berdasarkan Harga ---")
    table = PrettyTable()
    table.field_names = ["No", "Nama Layanan", "Harga per kg"]

    sorted_layanan = sorted(layanan.items(), key=lambda x: float(x[1]["harga"]))  
    if sorted_layanan:
        for idx, (nama_layanan, detail) in enumerate(sorted_layanan, 1):  
            table.add_row([idx, nama_layanan, detail["harga"]])
        print(table)
    else:
        print("Tidak ada layanan yang terdaftar.")

def topup_saldo(username, pengguna):
    if username not in pengguna:
        print("Pengguna tidak ditemukan!")
        return
    
    try:
        jumlah_topup = float(input("Masukkan jumlah saldo yang ingin di-top-up: Rp "))

        if jumlah_topup <= 0:
            print("Jumlah top-up tidak valid! Pastikan jumlahnya lebih besar dari 0.")
        else:
            pengguna[username]["saldo"] += jumlah_topup

            simpan_data('pengguna.json', pengguna)

            print(f"Top-up berhasil! Saldo Anda sekarang: Rp {pengguna[username]['saldo']:.2f}")
    except ValueError:
        print("Masukkan jumlah top-up yang valid!")

def buat_invoice(username, layanan_pesan, berat, biaya, estimasi_waktu):
    now = datetime.now()
    estimasi_waktu_obj = timedelta(days=int(estimasi_waktu.split()[0]))  
    waktu_selesai = now + estimasi_waktu_obj

    invoice = f"""
    ------------------------------
    Invoice Laundry
    ------------------------------
    Tanggal          : {now.strftime('%Y-%m-%d %H:%M:%S')}
    Nama Pengguna    : {username}
    Layanan          : {layanan_pesan}
    Berat Cucian     : {berat} kg
    Total Biaya      : Rp {biaya:.2f}
    Estimasi Waktu   : {estimasi_waktu} Hari (Selesai pada {waktu_selesai.strftime('%Y-%m-%d %H:%M:%S')})
    ------------------------------
    Terima kasih telah menggunakan layanan kami!
    ------------------------------
    """

    with open(f"invoice_{username}_{now.strftime('%Y%m%d%H%M%S')}.txt", 'w') as file:
        file.write(invoice)

    print(invoice)

def menu_pengguna(username, pengguna, transaksi, layanan):
    while True:
        print(f"\n--- Menu Pengguna ({username}) ---")
        print("1. Lihat Layanan")
        print("2. Pesan Layanan")
        print("3. Top-up Saldo")
        print("4. Lihat Saldo")
        print("5. Lihat Status Transaksi") 
        print("6. Layanan Berdasarkan Harga")
        print("7. Logout")
        pilihan = input("Pilih opsi: ")

        if pilihan == '1':
            lihat_layanan(layanan) 
        elif pilihan == '2':
            print("\n--- Pemesanan Layanan ---")
            try:
                lihat_layanan(layanan)  
                nomor_layanan = int(input("Masukkan nomor layanan yang ingin dipesan: "))
                if 1 <= nomor_layanan <= len(layanan):
                    layanan_pesan = list(layanan.keys())[nomor_layanan - 1]  
                    berat = float(input("Masukkan berat cucian (dalam kg): "))
                    harga = float(layanan[layanan_pesan]["harga"])
                    estimasi_waktu = layanan[layanan_pesan]["estimasi_waktu"]
                    biaya = harga * berat  
                    saldo_user = pengguna[username]["saldo"]
                    if saldo_user < biaya:
                        print("Saldo tidak mencukupi. Silakan top-up saldo terlebih dahulu.")
                    else:
                        pengguna[username]["saldo"] -= biaya  
                        status = "Sedang Diproses"
                        transaksi_baru = {
                            "username": username, 
                            "service": layanan_pesan, 
                            "status": status,
                            "biaya": biaya
                        }
                        transaksi.append(transaksi_baru)
                        simpan_data('transaksi.json', transaksi)
                        simpan_data('pengguna.json', pengguna)
                        print(f"Pemesanan untuk layanan '{layanan_pesan}' berhasil! Status: Sedang Diproses")
                        print(f"Total biaya: Rp {biaya:.2f}")

                        print(f"Sisa saldo Anda setelah pembayaran: Rp {pengguna[username]['saldo']:.2f}")

                        buat_invoice(username, layanan_pesan, berat, biaya, estimasi_waktu)
                else:
                    print("Nomor layanan tidak valid!")
            except ValueError:
                print("Masukkan nomor yang valid!")
        elif pilihan == '3':
            topup_saldo(username, pengguna) 
        elif pilihan == '4':
            print(f"Saldo Anda: Rp {pengguna[username]['saldo']:.2f}")
        elif pilihan == '5':
            lihat_status_transaksi(username, transaksi)
        elif pilihan == '6':
            lihat_layanan_urutkan(layanan)
        elif pilihan == '7':  
            break
        else:
            print("Pilihan tidak valid!")

def main():
    pengguna = muat_data('pengguna.json', data_default={})
    transaksi = muat_data('transaksi.json', data_default=[])
    layanan = muat_data('layanan.json', data_default={})

    while True:
        print("\n--- Aplikasi Laundry ---")
        print("1. Login Pengguna")
        print("2. Login Admin")
        print("3. Registrasi Pengguna")
        print("4. Keluar")
        pilihan = input("Pilih opsi: ")

        if pilihan == '1':
            username = login(pengguna, "user")
            if username:
                menu_pengguna(username, pengguna, transaksi, layanan)
        elif pilihan == '2':
            username = login(pengguna, "admin")
            if username:
                menu_admin(pengguna, transaksi, layanan)
        elif pilihan == '3':
            pengguna = registrasi_pengguna(pengguna)
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nAnda telah menekan Ctrl+C, kembali ke halaman utama...")
            continue
