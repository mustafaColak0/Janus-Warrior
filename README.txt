 JANUS WARRIOR v4.7 - KURULUM VE ENTEGRASYON REHBERİ
------------------------------------------

Bu sistem, sunucu loglarını anlık analiz ederek saldırganları 
Firewall üzerinden (OS düzeyinde) banlayan bir güvenlik katmanıdır.

1. ADIM: SUNUCU AYARLARI
- Sunucuda Python 3.10 veya üzeri yüklü olmalıdır.
- Gerekli kütüphaneler: 'pip install requests plyer'

2. ADIM: LOG ENTEGRASYONU (KRİTİK)
- analiz.py dosyasını açın ve 'LOG_FILE' değişkenine sitemizin 
  gerçek access.log yolunu yazın.
  Örn (Nginx): /var/log/nginx/access.log
  Örn (Apache): /var/log/apache2/access.log

3. ADIM: Log Yolu: analiz.py içindeki LOG_FILE değişkenini sitenin gerçek 
   access.log yoluyla (Örn: /var/log/nginx/access.log) güncelleyin.

4. ADIM: Honeypot Kurulumu: Sitenin ana dizinine (public_html) şu boş dosyaları oluşturun:
   - setup.php
   - admin_backup.zip
   - config.old
   - .env_production
5.Ban kaldırmak için unban "ip adresi" yazıp ban kaldırabiliyorsunuz

7. ADIM: SİSTEMİ BAŞLATMA
- Windows Sunucu: CMD'yi "Yönetici Olarak" açın ve 'python analiz.py' yazın.
- Linux Sunucu: Terminalde 'sudo python3 analiz.py' komutunu çalıştırın.

8. ADIM: YÖNETİM
- Yanlışlıkla bir IP engellenirse konsola 'unban IP_ADRESI' yazarak 
  engeli kaldırabilirsiniz.
- Tüm engellemeler 'blocked_ips.txt' dosyasına raporlanır.

-----------------------------------------------------
Güvenli günler dilerim. Janus Warrior iş başında!
