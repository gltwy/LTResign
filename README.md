# LTResign

## 准备工作
```bash
1. 已解密（脱壳）的App， 从PP助手或者使用经过越狱设备解密的App
2. 开发者证书
```
## 使用说明

```bash
python ltresign.py -s .app文件路径 -d 证书id -m 描述文件 -o 导出路径
```
示例
```bash
python ltresign.py -s WeChat.app -d "iPhone Developer: test test (XXXXX)" -m embedded.mobileprovision -o glt_WeChat.ipa 
```

## Author
- Email:  1282990794@qq.com
- -Blog:  https://blog.csdn.net/glt_code

## License

LTResign is available under the MIT license. See the LICENSE file for more info.
