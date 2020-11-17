import re
import gzip

def get_portinfo(switchname, datess, sshowfile):
    skip = True
    switchname = ''.join(switchname)
    portinfo = []

    #portinfo.append(['index', 'slot', 'port', 'address', 'speed', 'state', 'proto', 'alias'])

    with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            uline = line.strip()
            words = uline.split()

            if skip:
                key = re.search(r'(?=switchshow\:)|(?=switchshow\s\:)|(?=switchshow\s*\:)', uline)
                #key = re.search(r'========================', uline)
                if key:
                    skip = False
                    #print('KEY: False')
            else:
                sw_fid = re.search(r'(?<=FID\:\s)\d{1,3}', uline)
                if sw_fid:
                    fid = ''.join(sw_fid.group(0))
                    if fid == '128':
                        fid = '128'
                    else:
                        fid = sw_fid.group(0)

                ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                if ports:
                    del (words[4])
                    speed = re.findall(r'\d{1,2}', words[4])
                    words[4] = ' '.join(speed)
                    words[6] = ' '.join(str(e) for e in words[6:])
                    del (words[7:]) #proto
                    words.extend(datess.split())
                    words.extend(fid.split())
                    print('{:6s} {:7s} {:9s} {:6s} {:12s} {} {} {} {}'.format(*words))

                    portinfo.append(words)

                key = re.search(r'(?=SS CMD END)', uline)
                if key:
                    skip = True
                    #print('KEY: True')

    #print(portinfo)