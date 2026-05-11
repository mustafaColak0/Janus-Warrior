 JANUS WARRIOR - KURULUM VE ENTEGRASYON REHBERİ
------------------------------------------

Bu sistem, sunucu loglarını anlık analiz ederek saldırganları 
Firewall üzerinden (OS düzeyinde) banlayan bir güvenlik katmanıdır.


<img width="800" height="437" alt="janus_demo" src="https://github.com/user-attachments/assets/36b18f52-40e3-4f12-b58f-f77d6d460a55" />


1. ADIM: SUNUCU AYARLARI
- Sunucuda Python 3.10 veya üzeri yüklü olmalıdır.
- Gerekli kütüphaneler: 'pip install requests plyer' komutuyla yükleyebilirsiniz.

2. ADIM: LOG ENTEGRASYONU (KRİTİK)
- analiz.py dosyasını açın ve 'LOG_FILE' değişkenine sitemizin 
  gerçek access.log yolunu yazın.

  Örn (Nginx): /var/log/nginx/access.log
  Örn (Apache): /var/log/apache2/access.log

Not: Eğer dosya yoksa, aynı dizinde boş bir access.log dosyası oluşturun

3. ADIM: Honeypot Kurulumu: Sitenin ana dizinine (public_html) şu boş dosyaları oluşturun:
   - setup.php
   - admin_backup.zip
   - config.old
   - .env_production

4. ADIM: TELEGRAM ENTEGRASYONU (OPSİYONEL)
analiz.py içindeki TELEGRAM_TOKEN ve CHAT_ID alanlarını doldurarak saldırı raporlarını anlık olarak cebinize alabilirsiniz.

5. ADIM: SİSTEMİ BAŞLATMA
- Windows: CMD'yi "Yönetici Olarak" açın ve 'python analiz.py' (veya direkt Janus_Warrior.exe) çalıştırın.
- Linux: Terminalde 'sudo python3 analiz.py' komutunu çalıştırın.

6. ADIM: YÖNETİM VE KOMUTLAR
- Ban Kaldırma: Konsola unban IP_ADRESI yazarak yanlışlıkla engellenen kişilerin banını kaldırabilirsiniz.
- Beyaz Liste: list yazarak güvenli IP'leri görebilirsiniz.

7. ADIM: RAPORLAMA
Tüm engelleme kayıtları ve saldırı detayları blocked_ips.txt dosyasına otomatik olarak kaydedilir.

8. ADIM : SİSTEMİ TEST ETME
Sistemin çalıştığını doğrulamak için "python sim.py" yazarak sim.py dosyasını çalıştırarak yapay bir saldırı simülasyonu başlatabilir ve Janus'un anlık tepkisini ölçebilirsiniz.

-----------------------------------------------------
Güvenli günler dilerim. Janus Warrior iş başında!
