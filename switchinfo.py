import re
import gzip


def get_swinfo(switchname, datess, sshowfile):
    skip = True
    switchname = ''.join(switchname)
    switchinfo = []
    sw_dict = {}

    ''' open file to parsing '''
    with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            uline = line.strip()

            if skip:
                key = re.search(r'(?=switchshow\:)|(?=switchshow\s\:)|(?=switchshow\s*\:)', uline)
                if key:
                    skip = False
                    #print('KEY: False')
            else:
                sw_name = re.search(r'(?<=switchName\:\s).*', uline)
                if sw_name:
                    sw_dict['sw_name'] = sw_name.group(0)
                    switchinfo.append(sw_name.group(0))

                sw_type = re.search(r'(?<=switchType\:\s)\d{1,3}', uline)
                if sw_type:
                    sw_dict['sw_type'] = sw_type.group(0)
                    switchinfo.append(sw_type.group(0))

                sw_domain = re.search(r'(?<=switchDomain\:\s)\d{1,3}', uline)
                if sw_domain:
                    sw_dict['sw_domain'] = sw_domain.group(0)
                    switchinfo.append(sw_domain.group(0))

                sw_id = re.search(r'(?<=switchId\:\s).*', uline)
                if sw_id:
                    sw_dict['sw_id'] = sw_id.group(0)
                    switchinfo.append(sw_id.group(0))

                sw_wwn = re.search(r'(?<=switchWwn\:\s).*', uline)
                if sw_wwn:
                    sw_dict['sw_wwn'] = sw_wwn.group(0)
                    switchinfo.append(sw_wwn.group(0))

                sw_fid = re.search(r'(?<=FID\:\s)\d{1,3}', uline)
                if sw_fid:
                    #fid = ''.join(sw_fid.group(0))
                    #if fid == '128':
                        #switchinfo.append('128')
                        #switchinfo.append(sw_fid.group(0))
                    #else:
                    switchinfo.append(sw_fid.group(0))

                key = re.search(r'========================', uline)
                if key:
                    skip = True
                    #print('KEY: True')

        ''' add default FID if not found '''
        if not sw_fid:
            print('FID: none')
        #if len(switchinfo) == 5:
            #switchinfo.insert(len(switchinfo), '128')

        ''' Break a list into chunks of size N '''
        if len(switchinfo) > 6:
            n = 6
            switchinfo = [switchinfo[i * n:(i + 1) * n] for i in range((len(switchinfo) + n - 1) // n)]

        print(switchinfo)
        return switchinfo