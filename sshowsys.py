import re
import gzip
import dbhelper
import datetime
import switchinfo

class SshowSys:
    sw = []
    def parse_switchinfo(self, datess, sshowfile):
        skip = True
        switch = ''.join(self)

        ''' date formating '''
        tmp = ', '.join(datess)
        datess = tmp[0:4] + '-' + tmp[4:6] + '-' + tmp[6:8]
#        print(datess)

        ''' open file to parsing '''
        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()

                if skip:
                    key = re.search(r'(?=switchshow\:)|(?=switchshow\s\:)|(?=switchshow\s*\:)', uline)
                    if key:
                        skip = False
                        print('KEY: False')

                else:
                    sw = switchinfo.get_swinfo(uline)
                    key = re.search(r'========================', uline)
                    if key:
                        skip = True
                        print('KEY: True')

                    print(sw)

        '''  '''
#            sql = "INSERT INTO switch (sw_date,sw_name,sw_type,sw_domain,sw_id,sw_wwn,sw_fid) " \
#                  "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING switch_id" % ("'" + datess + "'",
#                                                                      "'" + switchinfo[0] + "'",
#                                                                      switchinfo[1],
#                                                                      switchinfo[2],
#                                                                      "'" + switchinfo[3] + "'",
#                                                                      "'" + switchinfo[4] + "'",
#                                                                      "'" + sw_fid + "'")

#            print(sql)
#            switch_id = dbhelper.db_insert(sql)



    def parse_alias(self, datess, sshowfile):
        alias = []

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                match = re.search(r'alias.(\w*):(\S*)', line)
                if match:
                    words = (match.group(1) + ' ' + match.group(2).replace(';', ' ')).split()
                    alias.append(words)

        return alias


    def parse_switchshow(self, sshowfile):
        skip = True
        switch = ''.join(self)
        switchshow = []
        switchinfo = []
        switchshow.append(['index', 'slot', 'port', 'address', 'speed', 'state', 'proto', 'alias'])

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()

                if skip:
                    key = re.search(r'========================', uline)
                    if key:
                        skip = False
                else:
                    ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                    if ports:
#                        words[1] = '/'.join(words[1:3])
#                        del (words[2])
#                        del (words[3])
                        del(words[4])
                        speed = re.findall(r'\d{1,2}', words[4])
                        words[4] = ' '.join(speed)
                        words[6] = ' '.join(str(e) for e in words[6:])
#                        del(words[7:]) '''proto'''
#                        print('{:6s} {:7s} {:9s} {:6s} {:12s} {} {}'.format(*words))

                        switchshow.append(words)
                    else:
                        skip = True

        return switchshow


    def parse_porterrshow(self, datess, sshowfile):
        skip = True
        porterrshow = []

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()
#                key, match = search_line(uline)
                if skip:
                    key = re.search(r'g_eof', uline)
                    if key:
                        skip = False
                else:
                    ports = re.search(r' \d{1,3}|^\d{1,3}:', uline)
                    if ports:
#                        words[0] = ''.join(re.findall(r'\d{1,3}', words[0]))
                        porterrshow.append(words)
                    else:
                        skip = True

        return porterrshow


    def count_porterrs(self):
        words = self

        for ele in words:
            if re.match(r'\d{1,3}.\d{1}(?=k)|\d{1,3}.\d{1}(?=g)|\d{1,3}.\d{1}(?=m)', ele):

                ''' kilo '''
                match = re.findall(r'\d{1,3}.\d{1}(?=k)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000)
                    return words

                ''' mega '''
                match = re.findall(r'\d{1,3}.\d{1}(?=m)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000000)
                    return words

                ''' giga '''
                match = re.findall(r'\d{1,3}.\d{1}(?=g)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000000000)
                    return words
            else:
                return self