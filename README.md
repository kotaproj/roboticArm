# ロボットアーム - roboticArm

本レポジトリは、[EEZYbotARM MK3](http://www.eezyrobots.it/eba_mk3.html)を使ったロボットアームの制御のプログラムです。

# DEMO

![out1](https://user-images.githubusercontent.com/59393206/116836150-6c301500-ac00-11eb-9ecd-ff5924b08161.gif)

# System

![image](https://user-images.githubusercontent.com/59393206/116837583-0181d800-ac06-11eb-8aab-61661368b649.png)

# Features

- MQTTを経由し、ロボットアームを制御

# Requirement

## ロボットアーム側
### ハードウェア

- [EEZYbotARM MK3](http://www.eezyrobots.it/eba_mk3.html)
  - 3Dプリンタで印刷
- [サーボモータ x 1](https://www.amazon.co.jp/Miuzei-%E3%82%B5%E3%83%BC%E3%83%9C%E3%83%A2%E3%83%BC%E3%82%BF%E3%83%BC-%E3%83%9E%E3%82%A4%E3%82%AF%E3%83%AD%E3%82%B5%E3%83%BC%E3%83%9C-10%E5%80%8B%E3%82%BB%E3%83%83%E3%83%88-%E3%83%87%E3%82%B8%E3%82%BF%E3%83%AB%E3%83%BB%E3%82%B5%E3%83%BC%E3%83%9C/dp/B07PHFQY6B/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%82%B5%E3%83%BC%E3%83%9C%E3%83%A2%E3%83%BC%E3%82%BF&qid=1620008419&s=instant-video&sr=1-1)
  - つかむ動作
- [ステッピングモータ x3](https://www.amazon.co.jp/gp/product/B07LBRNZB6/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
  - アームの駆動
- [ESP32 DevKitC](https://www.amazon.co.jp/waves-ESP32-DevKitC-ESP-WROOM-32-ESP-32/dp/B06XWP81GP)
  - マイコン評価ボード
- ジャンパーワイヤー 適量
- [ボールベアリング](https://www.amazon.co.jp/gp/product/B07HK9YKBM/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1)
- ネジM6, M3
- USB電源ケーブル

### ソフトウェア

* [MicroPython - ESP32](https://micropython.org/download/esp32/)
  * GENERIC : esp32-20210418-v1.15.bin

* [fizista/micropython-umqtt.simple2](https://github.com/fizista/micropython-umqtt.simple2)
  * 本レポジトリのsrc_minimized/umqttを配置すること

## MQTTサーバ、パブリッシャ

- paho.mqtt
  - pip install paho.mqtt


# Memo

大まかな流れ

1. EEZYbotARM MK3データを印刷
   1. ステッピングモータの⚙とアームの🦴は2つ印刷が必要
2. 組み立てる
   1. なぜか公式サイトに組み立て方が記載されていないyoutubeとかを見る
3. 接続する
   1. コードをベースに確認する
4. 別のシステムからmqttを経由し、コマンドを送信する
   1. ESP32は、MQTT - Subcriberとして動作
   2. MQTTサーバは別途用意すること
   3. Pulisherは、後述のコマンドを送付する

## コマンド

- topic
  - "topic_dev"
- メッセージ例
  - "_smotor_no1_val_-512_"
  - "_smotor_no1_val_512_"
  - "_servo_no1_val_70_"

# Note

- 組み立て方の紹介ページがないので大変。
- 本レポジトリは自分用メモ

# Author

* kotaproj

# License

"roboticArm" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

