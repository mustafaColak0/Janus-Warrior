import os
import time
import re
import requests
import socket
import threading
import sys
from plyer import notification

# --- AYARLAR ---
LOG_FILE = 'access.log'
BLOCKED_IPS_FILE = 'blocked_ips.txt'
HONEYPOT_PORT = 8080  # Hackerlar için yem portu
WHITE_LIST = ["127.0.0.1"]

# --- TELEGRAM AYARLARI ---
TELEGRAM_TOKEN = "BOT_TOKEN_BURAYA" #  kendi bot tokenın varsa
TELEGRAM_CHAT_ID = "CHAT_ID_BURAYA" # kendi chat ID'ni gir

# --- DDoS AYARLARI ---
REQUEST_HISTORY = {} 
DDOS_THRESHOLD = 30  
TIME_WINDOW = 5      

# --- TUZAK VE SALDIRI TANIMLAMALARI ---
attack_definitions = {
    # 1. Honeypot (Tuzak Dosyalar)
    "Honeypot Tuzaği": r'(config_backup\.sql|admin_v2\.php|db_dump\.zip|secrets\.txt|\.env_old)',
    
    # 2. Klasik Web Saldırıları
    "SQL Injection": r'(union\s+select|insert\s+into|drop\s+table|select\s+\*|having\s+1=1)',
    "XSS (Scripting)": r'(<script>|alert\(|eval\(|javascript:|<img\s+src=x)',
    "Path Traversal": r'(\/\.\.\/|\.\.\/|etc\/passwd|win\.ini)',
    
    # 3. Tarama ve Bilgi Toplama
    "Zararlı Bot/Scanner": r'(sqlmap|nmap|nikto|acunetix|masscan|zgrab|dirbuster)',
    "Hassas Dosya Tarama": r'(\.git|\.env|wp-config\.php|phpinfo\(\)|config\.php)'
}

def KONUM_VE_ISP_BUL(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        if res['status'] == 'success':
            return f"{res['country']} / {res['city']} | ISP: {res['isp']}"
    except: pass
    return "Konum Alınamadı"
def TELEGRAM_BILDIRIM_GONDER(mesaj):
    if TELEGRAM_TOKEN == "BOT_TOKEN_BURAYA": return 
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj}
        requests.post(url, data=payload, timeout=5)
    except:
        print("\033[91m[!] Telegram bildirimi gönderilemedi.\033[0m")

# 2. Ban Atma:
def GERCEK_BAN_AT(ip, sebep, konum="Bilinmiyor"):
    if ip in WHITE_LIST: 
        return
    
    # OS bazlı ban komutu (Windows/Linux)
    if os.name == 'nt':
        os.system(f'netsh advfirewall firewall add rule name="Janus_Ban_{ip}" dir=in action=block remoteip={ip}')
    else:
        os.system(f'sudo ufw deny from {ip}')
    
    # Ekrana rapor basma
    rapor = f"\n🛡️ JANUS İNFAZ GERÇEKLEŞTİ\n--------------------------\n🚨 Sebep: {sebep}\n🌐 IP: {ip}\n🌍 Konum: {konum}\n⏰ Zaman: {time.ctime()}"
    print(f"\033[1;91m{rapor}\033[0m")

    # --- SENİN EKLEDİĞİN TELEGRAM BLOĞU ---
    telegram_mesaj = f"🛡️ JANUS INFAZ 🛡️\n\n🚨 Sebep: {sebep}\n🌐 IP: {ip}\n🌍 Konum: {konum}\n⏰ Zaman: {time.ctime()}"
    TELEGRAM_BILDIRIM_GONDER(telegram_mesaj)
    # -------------------------------------

    print(f"\033[1;36m[Janus-Console]> \033[0m", end="", flush=True)

    # Bildirim (Masaüstü)
    try:
        notification.notify(title='🛡️ Janus Warrior', message=f'IP: {ip} engellendi!', timeout=5)
    except: pass
    
    # Kayıt dosyasına yaz
    with open(BLOCKED_IPS_FILE, 'a', encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {ip} | {sebep} | {konum}\n")

def BAN_KALDIR(ip):
    print(f"\033[94m[*] {ip} için ban kaldirma işlemi başlatildi...\033[0m")
    
    if os.name == 'nt':
        cmd = f'netsh advfirewall firewall delete rule name="Janus_Ban_{ip}"'
    else:
        cmd = f'sudo ufw delete deny from {ip}'
    
    result = os.system(cmd)
    
    if result == 0:
        print(f"\033[92m[+] {ip} üzerindeki engel başariyla kaldirildi! ✅\033[0m")
        if ip not in WHITE_LIST:
            WHITE_LIST.append(ip)
    else:
        print(f"\033[91m[-] Ban kaldirilamadi. IP listede olmayabilir.\033[0m")

# --- KULLANICI ETKİLEŞİMİ ---
def komut_dinle():
    while True:
        try:
            user_input = input("\033[1;36m[Janus-Console]> \033[0m").strip().split()
            if not user_input: continue
            
            komut = user_input[0].lower()
            
            if komut == "unban" and len(user_input) > 1:
                BAN_KALDIR(user_input[1])
            elif komut == "list":
                print(f"\033[94m[*] Mevcut Beyaz Liste: {WHITE_LIST}\033[0m")
            elif komut == "help":
                print("\033[93mKomutlar: \n- unban [IP] : Belirtilen IP'nin engelini kaldirir.\n- list       : Güvenli listeyi gösterir.\n- help       : Bu menüyü açar.\033[0m")
            elif komut == "exit":
                print("Janus kapatiliyor...")
                sys.exit()
        except EOFError: break

# --- HONEYPOT MODÜLÜ ---
def start_honeypot():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', HONEYPOT_PORT))
        server.listen(5)
        while True:
            client, addr = server.accept()
            ip = addr[0]
            konum = KONUM_VE_ISP_BUL(ip)
            GERCEK_BAN_AT(ip, f"Honeypot Port Tuzaği ({HONEYPOT_PORT})", konum)
            client.send(b"HTTP/1.1 200 OK\n\nWelcome to Admin Panel...")
            client.close()
    except Exception as e:
        print(f"\033[91m[!] Honeypot Hatası: {e}\033[0m")

# --- LOG ANALİZ MODÜLÜ ---
def monitor_logs():
    print(f"\033[93m[*] Log izleme aktif: {LOG_FILE}\033[0m")
    son_pozisyon = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0
    
    while True:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                f.seek(son_pozisyon)
                satirlar = f.readlines()
                son_pozisyon = f.tell()
                
                for satir in satirlar:
                    ip_match = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', satir)
                    if not ip_match: continue
                    ip = ip_match.group(1)

                    # DDoS Kontrolü
                    simdi = time.time()
                    if ip not in REQUEST_HISTORY: REQUEST_HISTORY[ip] = []
                    REQUEST_HISTORY[ip] = [t for t in REQUEST_HISTORY[ip] if simdi - t < TIME_WINDOW]
                    REQUEST_HISTORY[ip].append(simdi)
                    
                    if len(REQUEST_HISTORY[ip]) > DDOS_THRESHOLD:
                        konum = KONUM_VE_ISP_BUL(ip)
                        GERCEK_BAN_AT(ip, "DDoS / Flood", konum)
                        continue

                    # Saldırı Kontrolü
                    for tip, desen in attack_definitions.items():
                        if re.search(desen, satir, re.IGNORECASE):
                            konum = KONUM_VE_ISP_BUL(ip)
                            GERCEK_BAN_AT(ip, tip, konum)
                            break
        time.sleep(0.1)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n\033[1;36m[#] JANUS v4.7 UNBLOCKER | KARIYER PUSULAN SAVUNMA SISTEMI\033[0m")
    print(f"\033[1;36m--------------------------------------------------------\033[0m")
    
    # Threading başlatma
    threading.Thread(target=monitor_logs, daemon=True).start()
    threading.Thread(target=start_honeypot, daemon=True).start()
    
    print(f"\033[92m[*] Honeypot aktif! Port: {HONEYPOT_PORT}\033[0m")
    print("[*] Yardim için 'help' yazin.")
    
    # Ana thread komut dinlemede kalmalı
    komut_dinle()