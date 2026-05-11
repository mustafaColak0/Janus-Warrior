 JANUS WARRIOR - KURULUM VE ENTEGRASYON REHBERİ
------------------------------------------

Bu sistem, sunucu loglarını anlık analiz ederek saldırganları 
Firewall üzerinden (OS düzeyinde) banlayan bir güvenlik katmanıdır.

1. ADIM: SUNUCU AYARLARI
- Sunucuda Python 3.10 veya üzeri yüklü olmalıdır.
- Gerekli kütüphaneler: 'pip install requests plyer' komutuyla yükleyebilirsiniz.

2. ADIM: LOG ENTEGRASYONU (KRİTİK)
- analiz.py dosyasını açın ve 'LOG_FILE' değişkenine sitemizin 
  gerçek access.log yolunu yazın.

  Örn (Nginx): /var/log/nginx/access.log
  Örn (Apache): /var/log/apache2/access.log

Not: Eğer dosya yoksa, aynı dizinde boş bir access.log dosyası oluşturun

4. ADIM: Honeypot Kurulumu: Sitenin ana dizinine (public_html) şu boş dosyaları oluşturun:
   - setup.php
   - admin_backup.zip
   - config.old
   - .env_production

5. ADIM: TELEGRAM ENTEGRASYONU (OPSİYONEL)
analiz.py içindeki TELEGRAM_TOKEN ve CHAT_ID alanlarını doldurarak saldırı raporlarını anlık olarak cebinize alabilirsiniz.

6. ADIM: SİSTEMİ BAŞLATMA
- Windows: CMD'yi "Yönetici Olarak" açın ve 'python analiz.py' (veya direkt Janus_Warrior.exe) çalıştırın.
- Linux: Terminalde 'sudo python3 analiz.py' komutunu çalıştırın.

7. ADIM: YÖNETİM VE KOMUTLAR
- Ban Kaldırma: Konsola unban IP_ADRESI yazarak yanlışlıkla engellenen kişilerin banını kaldırabilirsiniz.
- Beyaz Liste: list yazarak güvenli IP'leri görebilirsiniz.

8. ADIM: RAPORLAMA
Tüm engelleme kayıtları ve saldırı detayları blocked_ips.txt dosyasına otomatik olarak kaydedilir.

-----------------------------------------------------
Güvenli günler dilerim. Janus Warrior iş başında!
