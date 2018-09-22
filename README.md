# LTResign
iOS一键重签名，轻松制作iOS App分身、以及动态注入dylib后重签名安装到设备等

## 准备工作
```bash
1. 已解密（脱壳）的App， 从PP助手或者使用经过越狱设备解密的ipa
2. 开发者证书
```
## 使用说明
#### 证书id获取：
```bash
python ltresign.py -l
```
#### embedded.mobileprovision获取
```bash
新建Xcode项目，选择设备，然后Build -> Products -> .app显示包内容，在包内容中找到embedded.mobileprovision文件
```
#### 命令说明（注意有些参数为可选）
使用帮助效果图
![image](https://github.com/gltwy/LTResign/blob/master/show.png)

- 使用方式1：ipa导出路径为当前目录，Display Name为原始，BundleIdentifier为原始
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision
```

- 使用方式2：ipa导出路径为当前目录下的glttest.ipa文件，Display Name为原始，BundleIdentifier为原始
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa
```

- 使用方式3：ipa导出路径为当前目录下的glttest.ipa文件，Display Name为原始，BundleIdentifier为设置的值
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa -b "新的bundleId"
```

- 使用方式4：ipa导出路径为当前目录下的glttest.ipa文件，Display Name为设置的新的名称，BundleIdentifier为设置的值
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa -b "新的bundleId" -n "新的名称"
```
- ...
```bash
根据自己的情况配置参数
```

#### 使用示例（仅供参考）
示例中test.app可以为ipa文件， -o为可选参数，-b为可选参数， -n为可选参数
```bash
python ltresign.py -s test.app -d "iPhone Developer: test test (XXXXX)" -m embedded.mobileprovision -o ./glttest.ipa -b "com.xxx.xxxx" -n "分身1"
```

#### 命令执行过程
命令执行过程效果图
![image](https://github.com/gltwy/LTResign/blob/master/process.jpeg)

## 安装效果图
![image](https://github.com/gltwy/LTResign/blob/master/finished.jpeg)

## Author
- Email:  1282990794@qq.com
- -Blog:  https://blog.csdn.net/glt_code

## 免责声明
仅供学习、交流使用，不具有任何商业用途，如有问题请及时联系本人以作处理。本声明未涉及的问题参见国家有关法律法规，当本声明与国家法律法规冲突时，以国家法律法规为准。

## License

LTResign is available under the MIT license. See the LICENSE file for more info.
