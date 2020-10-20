#!/usr/bin/env python3
import os, re
import fnmatch
import shutil
import tempfile
import zipfile
from sshowsys import SshowSys


def extract_files(zip, switch, datess, ssfiles, tempdir, acp, sshowfiles):
    switch = ''.join(switch)
    datess = ''.join(datess)
    acp = ''.join(acp)
    ssfiles = ' '.join(ssfiles)
    gzfiles = []

    for item in sshowfiles:
        match = re.search(r'((?:\S+-)' + acp + '\-\d+\.' + item + '\.gz)', ssfiles)
        if match:
            zip.extract(match.group(0), tempdir)
            gz = os.path.join(tempdir, match.group(0))
            words = (switch, datess, item, gz)
            gzfiles.append(words)

    return gzfiles


def main():
    sshowfiles = ['SSHOW_SYS.txt',
                 'SSHOW_PORT.txt',
                 'SSHOW_SERVICE.txt',
                 'SSHOW_FABRIC.txt']
    dinput = '/tmp/ss'
    output = '/tmp/out'


    try:
        if os.path.isdir(dinput) and fnmatch.filter(os.listdir(dinput), '*.zip'):
            with tempfile.TemporaryDirectory() as tempdir:
                print('The created temp directory is %s.' % tempdir)

            if not os.path.exists(output):
                try:
                    os.mkdir(output)
                except Exception as e:
                    print('Unable to create directory %s.' % output, e)

            ''' get archive supportsave files '''
            for files in sorted([f for f in os.listdir(dinput) if os.path.isfile(os.path.join(dinput, f))]):
                if re.match(r'supportsave_\w*\S*_\d+.zip', files):
                    zip = zipfile.ZipFile(os.path.join(dinput, files))
                    f = zipfile.ZipFile.namelist(zip)

                    ''' get switchname from file name '''
                    switch = re.findall(r'(?<=_)\w*\S*(?=_)', files)

                    ''' get date from file name '''
                    datess = re.findall(r'(?<=\_)\d+', files)

                    ''' get ACP '''
                    for ssfiles in f:
                        if re.findall(r'\w*\S*(S\dcp)\-\d+.SSHOW_PORT.txt.gz', ssfiles):
                            acp = re.findall(r'(?<=\-)\S\dcp', ssfiles)
                            gzfiles = extract_files(zip, switch, datess, f, tempdir, acp, sshowfiles)
#                            print(gzfiles)

                    ''' parse switchshow '''
                    for item in gzfiles:
                        if item[2] in sshowfiles[0]:
                            #switchinfo = SshowSys.parse_switchinfo(switch, item[3])
                            switchinfo = SshowSys.switch(switch, item[3])


                    ''' parse alias '''
                    for item in gzfiles:
                        if item[2] in sshowfiles[0]:
                            alias = SshowSys.parse_alias(item[0], item[1], item[3])
#                        return alias

                    ''' parse switchshow '''
                    for item in gzfiles:
                        if item[2] in sshowfiles[0]:
#                            print(switch, datess, sshowfiles[0])
                            ''' switch, datess, sshowfiles[0] '''
#                            switchshow = SshowSys.parse_switchshow(item[0], item[1], item[3])
                            switchshow = SshowSys.parse_switchshow(switch, item[3])

                    ''' parce porterrshow '''
                    for item in gzfiles:
                        if item[2] in sshowfiles[0]:
#                            print(switch, datess, sshowfiles[1])
                            porterrshow = SshowSys.parse_porterrshow(item[0], item[1], item[3])

            try:
                shutil.rmtree(tempdir)
                print("Temp directory '%s' has been removed successfully." % tempdir)
            except OSError as e:
                print('Delete of the directory %s failed.' % tempdir, e)

        else:
            print('The diretory %s not exist.' % dinput)

    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()