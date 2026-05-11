import time
import socket

LOG_FILE = 'access.log'

def log_yaz(ip, istek):
    satir = f'{ip} - - [{time.ctime()}] "GET {istek} HTTP/1.1" 200\n'
    with open(LOG_FILE, 'a') as f:
        f.write(satir)
    print(f"[*] Gönderildi: {ip} -> {istek}")

print("\n--- 🛡️ JANUS WARRIOR Saldiri Simulasyonu başliyor... ---")

# 1. TEST: SQL Injection (Web Koruması)
print("\n[!] Senaryo 1: SQL Injection Saldirisi")
log_yaz("172.16.0.1", "/products.php?id=10' OR '1'='1")

time.sleep(2)

# 2. TEST: Web Honeypot (Tuzak Dosya)
print("\n[!] Senaryo 2: Yasakli Dosyaya Erişim (Honeypot)")
log_yaz("172.16.0.2", "/config_backup.sql")

time.sleep(2)

# 3. TEST: DDoS Saldırısı (Hız Limiti)
print("\n[!] Senaryo 3: DDoS Saldiisi Başlatiliyor (35 İstek)")
for i in range(35):
    log_yaz("172.16.0.3", "/")

time.sleep(2)

# 4. TEST: Port Honeypot (TCP Bağlantısı)
print("\n[!] Senaryo 4: Port 8080 Taramasi(TCP)")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s.connect(('127.0.0.1', 8080))
    s.close()
    print("[*] Port 8080 bağlantisi yapildi.")
except:
    print("[-] Port 8080 bağlantisi başarisiz (Janus çalişiyor mu?)")

print("\n--- ✅ TEST TAMAMLANDI ---")