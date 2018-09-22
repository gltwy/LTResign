# LTResign
iOS一键重签名，轻松制作iOS上任意应用或游戏分身、以及Hook后重签名安装到非越狱或越狱设备等，以下是功能说明
```bash
1. 自动识别传入的文件为.app文件或.ipa文件，并进行不同的处理
2. 可指定重签名后ipa导出路径（不指定默认导出路径为当前路径下的glt_output.ipa）
3. 可指定app显示名称（Bundle Display Name）
4. 可指定导出ipa的BundleIdentifier
5. 证书id获取
```

![image](https://github.com/gltwy/LTResign/blob/master/show.png)

## 准备工作
```bash
1. 已解密（脱壳）的App， 从越狱助手下载或者使用经过越狱设备解密（使用Clutch、dumpdecrypted、frida等解密工具）的ipa
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

- 使用方式一：默认ipa导出路径为当前目录下的glt_output.ipa，Display Name为原始，BundleIdentifier为原始
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision
```

- 使用方式二：指定ipa导出路径为当前目录下的glttest.ipa文件，Display Name为原始，BundleIdentifier为原始
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa
```

- 使用方式三：指定ipa导出路径为当前目录下的glttest.ipa文件，Display Name为原始，BundleIdentifier为设置的值
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa -b "新的bundleId"
```

- 使用方式四：指定ipa导出路径为当前目录下的glttest.ipa文件，Display Name为设置的新的名称，BundleIdentifier为设置的值
```bash
python ltresign.py -s .app文件路径或.ipa文件路径 -d 证书id -m embedded.mobileprovision -o ./glttest.ipa -b "新的bundleId" -n "新的名称"
```
- 更多
```bash
根据自己的情况配置参数
```

#### 使用示例（仅供参考）
示例中test.app可以为ipa文件， -o为可选参数，-b为可选参数， -n为可选参数
```bash
python ltresign.py -s test.app -d "iPhone Developer: test test (XXXXX)" -m embedded.mobileprovision -o ./glttest.ipa -b "com.xxx.xxxx" -n "分身1"
```

#### 命令执行过程
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
