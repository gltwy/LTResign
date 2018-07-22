# LTResign
iOS一键重签名，轻松制作iOS App分身、以及动态注入dylib后重签名安装到设备等

## 准备工作
```bash
1. 已解密（脱壳）的App， 从PP助手或者使用经过越狱设备解密的ipa
2. 开发者证书
```
## 使用说明
- 命令说明
```bash
python ltresign.py -s .app文件路径 -d 证书id -m embedded.mobileprovision -o 导出路径
```
- 证书id获取：
```bash
security find-identity -v -p codesigning
```
- embedded.mobileprovision获取
```bash
新建Xcode项目，选择设备，然后Build -> Products -> .app显示包内容，在包内容中找到embedded.mobileprovision文件
```
- 使用示例
1. 解压ipa 
2. 修改info.plist的Bundle identifier(CFBundleIdentifier), 此步可忽略，若忽略会覆盖已安装的同名（Bundle identifier）App
```bash
python ltresign.py -s WeChat.app -d "iPhone Developer: test test (XXXXX)" -m embedded.mobileprovision -o glt_WeChat.ipa 
```

## Author
- Email:  1282990794@qq.com
- -Blog:  https://blog.csdn.net/glt_code

## License

LTResign is available under the MIT license. See the LICENSE file for more info.
