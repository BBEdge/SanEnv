import re
import gzip

def get_porterror(switchname, datess, sshowfile):
    skip = True
    switchname = ''.join(switchname)
    porterrshow = []

    with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            uline = line.strip()
            words = uline.split()

            if skip:
                key = re.search(r'g_eof', uline)
                if key:
                    skip = False
            else:
                ports = re.search(r' \d{1,3}|^\d{1,3}:', uline)
                if ports:
#                        words[0] = ''.join(re.findall(r'\d{1,3}', words[0]))
                    print(porterrshow)
                    #porterrshow.append(words)
                else:
                    skip = True

        #print(porterrshow)
        #return porterrshow
