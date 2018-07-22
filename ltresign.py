# coding=utf-8

import getopt
import sys
import os
import shutil
import zipfile

glt_version = '0.0.1'
glt_tmpAppPath = 'glt_tmp.app'
glt_frameworksFile = 'glt_frameworks.txt'
glt_developerCodeSign = ''
glt_exportPath = ''
glt_mobile = ''
glt_source = ''


def glt_print_help():
    source = '\n-s: [source]\tsource app file path\n'
    devloper = '-d: [developer]\tdeveloper code sign\n'
    mobile = '-m: [mobile]\tmobile provision\n'
    output = '-o: [output]\toutput app file path\n'
    help = '-V: \tversion\n'
    printInfo = '%s%s%s%s%s' % (source, devloper, mobile, output, help)
    printInfo = printInfo.expandtabs(20)
    print(printInfo)


def glt_exit():
    sys.exit()


def glt_handle_argExcept():
    glt_print_help()
    glt_exit()


def glt_parser_args(argv):
    if len(argv) == 1:
        glt_handle_argExcept()

    try:
        opts, args = getopt.getopt(argv[1:], "Vs:i:d:m:o:", ["Version", "source", "developer", "mobile", "output"])
    except getopt.GetoptError:
        glt_handle_argExcept()

    source = ''
    developer = ''
    mobile = ''
    output = ''
    version = ''
    for opt, arg in opts:
        if opt == '-V':
            version = arg
            glt_exit()
        elif opt in ('-s', 'source'):
            source = arg
        elif opt in ('-d', 'developer'):
            developer = arg
        elif opt in ('-m', 'mobile'):
            mobile = arg
        elif opt in ('-o', 'output'):
            output = arg
        else:
            glt_handle_argExcept()
    return source, developer, mobile, output, version


def glt_cmd(cmd):
    process = os.popen(cmd)
    output = process.read()
    process.close()
    return output


def glt_copyFile(file, target):
    os.system('cp -r \"%s\" \"%s\"' % (file, target))


# 拷贝app文件
def glt_handle_source(source):
    # glt_cmd('cp -R %s %s' % (glt_tmpAppPath, glt_exportPath))
    # return

    if os.path.exists(glt_tmpAppPath):
        isWhile = True
        while isWhile:
            glt_input = raw_input('Aleady Exists %s, Are you sure want to remove it? [y/n]: ' % glt_tmpAppPath)
            if 'y' in glt_input or 'Y' in glt_input:
                isWhile = False
            elif 'n' in glt_input or 'N' in glt_input:
                print('Please backup your %s and try again!\nDone!' % glt_tmpAppPath)
                glt_exit()
        os.system('rm -rf %s' % glt_tmpAppPath)
        print('Remove it done!')
    glt_copyFile(source, glt_tmpAppPath)


# 导出签名信息
def glt_export_signInfo(embeddedMobileprovision):
    print('导出签名信息')
    tmpPlist = 'entitlements_tmp.plist'
    # 导出签名信息
    glt_cmd('security cms -D -i %s > %s' % (embeddedMobileprovision, tmpPlist))
    # 导出签名信息中entitlements信息
    glt_cmd('/usr/libexec/PlistBuddy -x -c "Print:Entitlements" %s > entitlements.plist' % tmpPlist)
    if os.path.exists(tmpPlist):
        os.remove(tmpPlist)


# 将结果写入到文件
def glt_writeToFile(content):
    if os.path.exists(glt_frameworksFile):
        os.remove('./%s' % glt_frameworksFile)
    glt_file = file(glt_frameworksFile, 'a+')
    result = glt_file.write(content)
    glt_file.close()


def glt_resignappWithPath(filePath):
    print('Resigning... -> %s' % filePath)
    glt_cmd('codesign -f -s "%s" --entitlements=entitlements.plist %s' % (glt_developerCodeSign, glt_tmpAppPath))


def glt_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)
      zipf.write(pathfile, arcname)
  zipf.close()

# 读取文件
def glt_readToFile():
    print('\nBegain resigning:')
    contentFile = open(glt_frameworksFile)
    line = contentFile.readline()
    while line:
        glt_resignappWithPath(line)
        line = contentFile.readline()
    contentFile.close()
    print('\nResigning done!')
    resultPath, fileName = os.path.split(glt_exportPath)
    sourcePath, sourceName = os.path.split(glt_source)
    payloadPath = '%s/Payload' % resultPath
    os.mkdir(payloadPath)
    shutil.copytree(glt_tmpAppPath, '%s/%s' % (payloadPath, sourceName))
    glt_zip(payloadPath, '%s/%s' % (resultPath, fileName))
    shutil.rmtree(payloadPath)
    if os.path.exists(glt_frameworksFile):
        os.remove(glt_frameworksFile)


def glt_handle_resignFiles():
    findCondition = '\\( -name "*.app" -o -name "*.appex" -o -name "*.framework" -o -name "*.dylib" \\)'
    cmd = 'find -d ./%s %s' % (glt_tmpAppPath, findCondition)
    result = glt_cmd(cmd)
    glt_writeToFile(result)
    glt_readToFile()


# 拷贝embedded.mobileprovision到app
def glt_handle_developer(mobile):
    glt_copyFile(mobile, './%s' % glt_tmpAppPath)
    glt_handle_resignFiles()


if __name__ == "__main__":
    source, developer, mobile, output, version = glt_parser_args(sys.argv)
    if source:
        glt_source = source
        glt_handle_source(source)
    if developer:
        glt_developerCodeSign = developer
    if mobile:
        glt_export_signInfo(mobile)
        glt_mobile = mobile
    if output:
        print(output)
        glt_exportPath = output
        glt_handle_developer(glt_mobile)
    if version:
        print(version)
