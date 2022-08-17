## ishikawa-kosen A

## team member
加藤真輝
長澤建琉
越野亮（コーチ）

## Content
schemes:電気機械部品の模式図が入っている
src:競技用のすべてのソースコードが入っている
t-photos:私達のチームの２つの写真が入っている
v-photos:私達の車体の六枚の写真が入っている
video:私達の車体の動作が見れるYoutubeへのリンクが入っている

## 使用した電子部品：
RaspberryPi4
バッテリー：INIU POWERBANK BI-B3
広角カメラ:RPi Camera(G)
SPIKEプライム：
LEGO Technique Large Hub
LEGO Technique L angular motor × 2

これらの電子部品の配線はschemesフォルダ内に示されています

## チームのロボットの概要：
私達のロボットの車体は[RaspberryPi （raspi）]と[LEGO SPIKE]によって構成されています
また車体の基本部分はほぼ全てLEGOブロックによって構成されています。
raspiには広角カメラが接続されており、SPIKEにはステアリングモータと駆動モータが接続されています
raspiとSPIKEはシリアル通信を行っており、raspiはカメラから得られたコース上の情報をSPIKEに送信しています
SPIKEは送られてきた情報をもとにモータを動作させています

raspi・SPIKE共にPythonでコードが書かれおり、raspiはcolor_avoid_wideangle.pyをSPIKEはmain.pyを本番では実行させます
詳細な実行方法はsrcフォルダ内のREAD.mdに記載されています



