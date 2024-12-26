# OpenLoop.SO Sentry Node BOT
OpenLoop.SO Sentry Node BOT

Download Extension Here : [OpenLoop.SO Sentry Node](https://chromewebstore.google.com/detail/openloopso-sentry-node-ex/effapmdildnpkiaeghlkicpfflpiambm) | Use Code : ol92f69d11

## Fitur

  - Auto Get Account Information
  - Auto Run With Auto Proxy if u Choose 1
  - Auto Use [Monosans Proxy](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) if u Choose Run With Auto Proxy
  - Auto Run With Manual Proxy if u Choose 2
  - Auto Run Without Proxy if u Choose 3
  - Auto Complete Tasks
  - Auto Send Ping
  - Multi Account With Thread

## Prasyarat

Pastikan Anda telah menginstal Python3.9 dan PIP.

## Instalasi

1. **Kloning repositori:**
   ```bash
   git clone https://github.com/vonssy/OpenLoop-BOT.git
   ```
   ```bash
   cd OpenLoop-BOT
   ```

2. **Instal Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Konfigurasi

- **tokens.txt:** Anda akan menemukan file `tokens.txt` di dalam direktori proyek. Pastikan `tokens.txt` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:

  ```bash
    eyjxxxxx1
    eyjxxxxx2
  ```
- **manual_proxy.txt:** Anda akan menemukan file `manual_proxy.txt` di dalam direktori proyek. Pastikan `manual_proxy.txt` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:
  ```bash
    ip:port #http or socks5 - change schemes in line 108
    http://ip:port
    socks4://ip:port
    socks5://ip:port
    http://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
    socks4://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
    socks5://ip:port@user:pass #idk its work or not, cuase i don't have authentic proxy
  ```

## Jalankan

```bash
python bot.py #or python3 bot.py
```

## Penutup

Terima kasih telah mengunjungi repository ini, jangan lupa untuk memberikan kontribusi berupa follow dan stars.
Jika Anda memiliki pertanyaan, menemukan masalah, atau memiliki saran untuk perbaikan, jangan ragu untuk menghubungi saya atau membuka *issue* di repositori GitHub ini.

**vonssy**