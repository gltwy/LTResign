# coding=utf-8

import getopt
import os
import shutil
import sys
import time
import zipfile

glt_version = '0.0.1'
glt_tmp = 'glt_tmp'
glt_tmpAppPath = '%s/glt_tmp.app' % glt_tmp
glt_frameworksFile = '%s/glt_frameworks.txt' % glt_tmp
glt_tmpPlist = '%s/entitlements_tmp.plist' % glt_tmp
glt_entitlePlist = '%s/entitlements.plist' % glt_tmp
glt_devicesTxt = '%s/devices.txt' % glt_tmp
glt_developerCodeSign = ''
glt_exportPath = ''
glt_mobile = ''
glt_source = ''
glt_name = ''
glt_bundleid = ''
glt_encrypt = ''


def glt_print_help():
    source = '\n重签名需要传入的参数:\n-s, --source\t源App/ipa的路径（必传）\n'
    devloper = '-d, --developer\t证书签名id（必传）\n'
    mobile = '-m, --mobile\tembedded.mobileprovision路径（必传）\n'
    output = '-o, --output\tipa导出路径（可选，默认当前路径）\n'
    name = '-n, --name\t指定导出后的Display Name（可选，默认为原始）\n'
    bundleid = '-b, --bundleid\t指定导出后的BundleIdentifier（可选，默认为原始）\n\n'

    encrypt = 'app/ipa是否加密:\n-e, --encrypt\t根据app/ipa路径判断可执行文件是否加密\n\n'

    codesignID = '获取证书签名id:\n-l, --codesigningid\t证书签名id\n\n'

    version = '当前工具的版本:\n-V, --version \t版本号\n\n'

    help = '显示帮助信息:\n-h, --help \t帮助\n'

    printInfo = '%s%s%s%s%s%s%s%s%s%s' % (
        source, devloper, mobile, output, name, bundleid, codesignID, encrypt, version, help)
    printInfo = printInfo.expandtabs(26)
    print(printInfo)


def glt_exit():
    sys.exit()


def glt_handle_argExcept():
    glt_print_help()
    glt_exit()


def glt_cmd(cmd):
    process = os.popen(cmd)
    output = process.read()
    process.close()
    return output


def glt_handleWhiteSpace(name):
    space = name.lstrip().rstrip()
    return space.replace('\n', '')


def glt_parser_args(argv):
    if len(argv) == 1:
        glt_handle_argExcept()

    try:
        shortParamters = "Vhs:n:b:d:m:o:e:l"
        longParamters = ["version", "help", "source", "name", "bundleid", "developer", "mobile", "output", "encrypt",
                         "codesignid"]
        opts, args = getopt.getopt(argv[1:], shortParamters, longParamters)
    except getopt.GetoptError:
        glt_handle_argExcept()

    source = ''
    developer = ''
    mobile = ''
    output = ''
    version = ''
    codesignID = ''
    name = ''
    bundleid = ''
    encrypt = ''

    for opt, arg in opts:
        if opt == '-V' or opt == '--version':
            version = glt_version
        elif opt in ('-h', 'help'):
            glt_handle_argExcept()
        elif opt in ('-s', 'source'):
            source = arg
        elif opt in ('-n', 'name'):
            name = arg
        elif opt in ('-b', 'bundleid'):
            bundleid = arg
        elif opt in ('-d', 'developer'):
            developer = arg
        elif opt in ('-m', 'mobile'):
            mobile = arg
        elif opt in ('-o', 'output'):
            output = arg
        elif opt in ('-e', 'encrypt'):
            encrypt = arg
        elif opt in ('-l', 'codesignid'):
            codesignID = 'security find-identity -v -p codesigning'
        else:
            glt_handle_argExcept()
    return source, name, bundleid, developer, mobile, output, codesignID, encrypt, version


def glt_userChooseIsDelete(filePath):
    if os.path.exists(glt_tmp):
        isWhile = True
        while isWhile:
            glt_input = raw_input('Aleady Exists %s, Are you sure want to remove it? [y/n]: ' % glt_tmp)
            if 'y' in glt_input or 'Y' in glt_input:
                shutil.rmtree(glt_tmp)
                isWhile = False
                print('Remove it done!')
            elif 'n' in glt_input or 'N' in glt_input:
                print('Please backup your %s and try again!\nDone!' % glt_tmp)
                glt_exit()
    os.mkdir(glt_tmp)


def glt_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()


def glt_unzipFile(sourceFile, outputPath):
    zipObj = zipfile.ZipFile(sourceFile, 'r')
    zipObj.extractall(outputPath)
    zipObj.close()


def glt_handle_source(source):
    global glt_tmp
    global glt_tmpAppPath
    global glt_isIPA
    glt_tmp = 'glt_tmp'
    glt_userChooseIsDelete(glt_tmp)
    path, fileName = os.path.split(source)
    if '.ipa' in source:
        glt_unzipFile(source, '%s/glt_test' % glt_tmp)
        glt_tmp = '%s/glt_test/Payload' % (glt_tmp)
        appPackageName = glt_cmd('ls %s' % (glt_tmp))
        appPath = '%s/%s' % (glt_tmp, appPackageName)
        glt_tmpAppPath = glt_handleWhiteSpace(appPath)
        glt_isIPA = True
    elif '.app' in source:
        if os.path.exists(source):
            print('\nCreating temp file...\n')
            shutil.copytree(source, glt_tmpAppPath)
        else:
            print('\nSource app file path not exists\n')
            glt_exit()
        glt_tmpAppPath = '%s/glt_tmp.app' % glt_tmp
        glt_isIPA = False
    else:
        glt_handle_argExcept()


def glt_configAppToIpa():
    resultPath, fileName = os.path.split(glt_exportPath)
    sourcePath, sourceName = os.path.split(glt_source)
    if os.path.exists(resultPath) == False:
        os.mkdir(resultPath)
    payloadPath = '%s/Payload' % resultPath
    if os.path.exists(payloadPath):
        shutil.rmtree(payloadPath)
    os.mkdir(payloadPath)
    shutil.copytree(glt_tmpAppPath, '%s/%s' % (payloadPath, sourceName))
    glt_zip(payloadPath, '%s/%s' % (resultPath, fileName))
    if os.path.exists(payloadPath):
        shutil.rmtree(payloadPath)
    if os.path.exists(glt_tmp):
        shutil.rmtree(glt_tmp)
    print('\n重新签名完成，可以去安装了！（%s）' % time.strftime("%F %H:%M:%S"))


def glt_remove_glt_tmp_path():
    if os.path.exists('./glt_tmp'):
        shutil.rmtree('./glt_tmp')


def glt_configIpaToIpa():
    resultPath, fileName = os.path.split(glt_exportPath)
    if os.path.exists(resultPath) == False:
        os.mkdir(resultPath)
    glt_zip(glt_tmp, '%s/%s' % (resultPath, fileName))
    glt_remove_glt_tmp_path()
    print('\n重新签名完成，可以去安装了！（%s）' % time.strftime("%F %H:%M:%S"))


def glt_readToFile(handleLineFuncName):
    contentFile = open(glt_frameworksFile)
    line = contentFile.readline()
    while line:
        handleLineFuncName(glt_handleWhiteSpace(line))
        line = contentFile.readline()
    contentFile.flush()
    contentFile.close()
    if os.path.exists(glt_frameworksFile):
        os.remove('./%s' % glt_frameworksFile)


def glt_writeToFile(content):
    if os.path.exists(glt_frameworksFile):
        os.remove('./%s' % glt_frameworksFile)
    glt_file = file(glt_frameworksFile, 'a+')
    result = glt_file.write(content)
    glt_file.close()


def glt_resignappWithPath(filePath):
    sys_cmd = 'codesign -f -s "%s" --entitlements %s "%s"' % (glt_developerCodeSign, glt_entitlePlist, filePath)
    glt_cmd(sys_cmd)


def glt_handle_resignFiles():
    findCondition = '\\( -name "*.app" -o -name "*.appex" -o -name "*.framework" -o -name "*.dylib" \\)'
    cmd = 'find -d \"%s\" %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)
    glt_readToFile(glt_resignappWithPath)


def glt_readToFile_delete_Watch_PlugIns(filePath):
    if os.path.exists(filePath):
        shutil.rmtree(filePath)


def glt_delete_Watch_PlugIns():
    findCondition = '\\( -name "Watch" -o -name "PlugIns" \\)'
    cmd = 'find -d "./%s" %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)
    glt_readToFile(glt_readToFile_delete_Watch_PlugIns)


def glt_begain_resign():
    print('\n正在开始签名...')
    shutil.copy(glt_mobile, './%s' % glt_tmpAppPath)


def glt_supportdevices_count():
    cmd = '/usr/libexec/PlistBuddy -x -c "Print:ProvisionedDevices" %s | grep "string" > %s' % (
        glt_tmpPlist, glt_devicesTxt)
    result = glt_cmd(cmd)
    contentFile = open(glt_devicesTxt)
    line = contentFile.readline()
    count = 0
    while line:
        line = contentFile.readline()
        count += 1
    contentFile.flush()
    contentFile.close()
    if os.path.exists(glt_devicesTxt):
        os.remove(glt_devicesTxt)
    print('\n支持的设备数：%d台' % count)


def glt_export_signInfo(embeddedMobileprovision):
    cmd = 'security cms -D -i %s > %s' % (embeddedMobileprovision, glt_tmpPlist)
    os.system(cmd)
    cmd = '/usr/libexec/PlistBuddy -x -c "Print:Entitlements" %s > %s' % (glt_tmpPlist, glt_entitlePlist)
    glt_cmd(cmd)
    glt_begain_resign()
    glt_supportdevices_count()


def glt_configDisplayName(filePath):
    printcmd = '/usr/libexec/PlistBuddy -x -c "Print :CFBundleDisplayName" %s >/dev/null 2>&1' % filePath
    result = os.system(printcmd)
    if result == 0:
        cmd = '/usr/libexec/PlistBuddy -x -c "Set :CFBundleDisplayName %s" %s  >/dev/null 2>&1' % (
            glt_name, filePath)
        glt_cmd(cmd)
    else:
        cmd = '/usr/libexec/PlistBuddy -x -c "Set :CFBundleName %s" %s > /dev/null 2>&1' % (glt_name, filePath)
        result = os.system(cmd)
        if result != 0:
            cmd = '/usr/libexec/PlistBuddy -x -c "Add :CFBundleDisplayName string %s" %s' % (
                glt_name, filePath)
            glt_cmd(cmd)


def glt_updateNameWithPath(filePath):
    glt_configDisplayName(filePath)


def glt_updateNameWithInfoPlistPath(filePath):
    if filePath.endswith('.app/Info.plist'):
        glt_configDisplayName(filePath)


def glt_findInfoPlist():
    findCondition = '\\( -name "Info.plist" \\)'
    cmd = 'find -d \"%s\" %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)


def glt_findInfoPlistStrings():
    findCondition = '\\( -name "InfoPlist.strings" \\)'
    cmd = 'find -d \"%s\" %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)


def glt_handle_app_names():
    glt_findInfoPlistStrings()
    glt_readToFile(glt_updateNameWithPath)
    glt_findInfoPlist()
    glt_readToFile(glt_updateNameWithInfoPlistPath)


def glt_updateBundleIDWithInfoPlistPath(filePath):
    if filePath.endswith('.app/Info.plist'):
        cmd = '/usr/libexec/PlistBuddy -x -c "Set :CFBundleIdentifier %s" %s' % (glt_bundleid, filePath)
        glt_cmd(cmd)


def glt_handle_bundleid_infoplist():
    findCondition = '\\( -name "Info.plist" \\)'
    cmd = 'find -d \"%s\" %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)
    glt_readToFile(glt_updateBundleIDWithInfoPlistPath)


def glt_judge_isEncrypt(filePath):
    if filePath.endswith('.app/Info.plist'):
        printcmd = '/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" %s ' % filePath
        result = glt_cmd(printcmd)
        resultPath, _ = os.path.split(filePath)
        execPath = '%s/%s' % (resultPath, result.strip('\n'))
        is_encrypt = glt_cmd('otool -l %s | grep cryptid' % execPath)
        if 'cryptid 1' in is_encrypt:
            if glt_encrypt == '':
                print('\ncryptid 1 (未解密)\n')
                print('请解密 %s 后重试\n' % glt_source)
            else:
                print('\ncryptid 1 (未解密)\n')
            glt_remove_glt_tmp_path()
            glt_exit()
        else:
            print('\ncryptid 0 (已解密)\n')
            if glt_encrypt != '':
                glt_remove_glt_tmp_path()


def glt_handle_encrypt():
    glt_findInfoPlist()
    glt_readToFile(glt_judge_isEncrypt)


def glt_handle_developer():
    glt_delete_Watch_PlugIns()

    if glt_encrypt != '':
        glt_handle_encrypt()
        glt_exit()

    if glt_source:
        glt_handle_encrypt()

    if glt_name != '':
        glt_handle_app_names()

    if glt_bundleid != '':
        glt_handle_bundleid_infoplist()

    glt_handle_resignFiles()

    if glt_isIPA:
        glt_configIpaToIpa()
    else:
        glt_configAppToIpa()


def glt_handle_outputName():
    global glt_exportPath
    if glt_exportPath == '':
        glt_exportPath = "./glt_output.ipa"
    if glt_exportPath.endswith(".ipa") == False:
        glt_exportPath = "%s/glt_output.ipa" % glt_exportPath


if __name__ == "__main__":

    source, name, bundleid, developer, mobile, output, codesignID, encrypt, version = glt_parser_args(sys.argv)

    if codesignID:
        print(glt_cmd(codesignID))
        glt_exit()

    if version:
        print(version)
        glt_exit()

    if source and developer and mobile:

        if name:
            glt_name = name

        if bundleid:
            glt_bundleid = bundleid

        if output:
            glt_exportPath = output

        glt_source = source
        glt_developerCodeSign = developer
        glt_mobile = mobile

        glt_handle_source(glt_source)
        glt_export_signInfo(glt_mobile)
        glt_handle_outputName()
        glt_handle_developer()

    elif encrypt:
        glt_source = encrypt
        glt_encrypt = encrypt
        glt_handle_source(glt_source)
        glt_handle_developer()

    else:
        glt_handle_argExcept()
