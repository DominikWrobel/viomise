## Home Assistant integration for Viomi SE and Xiaomi STY02YM, STYJ02YM vacuums

![logo](https://github.com/user-attachments/assets/398cdf45-c36b-4cf2-b458-af00832aa092)

_Original code by [@nqkdev](https://github.com/nqkdev/home-assistant-vacuum-styj02ym) and [@KrzysztofHajdamowicz](https://github.com/KrzysztofHajdamowicz/home-assistant-vacuum-styj02ym) then I forked it and added HACS support, unique_id and fixed some deprevation notices._  
_I will try, with your help, to have this integration working as long as I can._

### This is for V-RVCLM21B, STY02YM and STYJ02YM (apparently EU version) with 3.5.3_0017 firmware

#### Install

- Install it with HACS by adding (https://github.com/DominikWrobel/viomise) as a custom repository

#### Usage

Find Viomi SE in integrations page:

![setup](https://github.com/user-attachments/assets/80a382fb-5a55-49da-a05c-9a31db1f7c8a)

Note: Vacuum token can be extracted by following [this guide](https://www.home-assistant.io/integrations/xiaomi_miio/#retrieving-the-access-token). I recommend using the python script method to extract the token as it is simpler, and only requires you to enter your Xiaomi Cloud username and password. These are the credentials used for the Xiaomi Home app (not ones from Viomi Robot app).

With the great [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor) and [Lovelace Vacuum Map card](https://github.com/PiotrMachowski/lovelace-xiaomi-vacuum-map-card?tab=readme-ov-file#lovelace-vacuum-map-card) you can make a great card for your vacuum:

![mapa](https://github.com/user-attachments/assets/baffebc6-e6fb-490b-9482-1064e897b182)

#### Works with

| Model | Device ID | Aliases | Status |
| ----- | --------- | ------- | ------ |
| **STYJ02YM** | viomi.vacuum.v8 | Mi Robot Vacuum-Mop P <br> MiJia Mi Robot Vacuum Cleaner <br> Xiaomi Mijia Robot Vacuum Cleaner LDS | :white_check_mark: Verified |
| **STY02YM** | viomi.vacuum.v7 | Mi Robot Vacuum-Mop P (CN) | :white_check_mark: Verified |
| **V-RVCLM21B** | viomi.vacuum.v6 | Viomi V2 <br> Xiaomi Viomi Cleaning Robot <br> Viomi Cleaning Robot V2 Pro | :white_check_mark: Verified |


# Support

If you like my work you can support me via:

<figure class="wp-block-image size-large"><a href="https://www.buymeacoffee.com/dominikjwrc"><img src="https://homeassistantwithoutaplan.files.wordpress.com/2023/07/coffe-3.png?w=182" alt="" class="wp-image-64"/></a></figure>
