import re
import gzip

#global switchinfo
#global sw_dict
#switchinfo = []
#sw_dict = {}

def get_swinfo(self, datess, sshowfile):
    skip = True
    switchname = ''.join(self)
    switchinfo = []
    sw_dict = {}

    ''' date formating '''
    tmp = ', '.join(datess)
    datess = tmp[0:4] + '-' + tmp[4:6] + '-' + tmp[6:8]

    ''' open file to parsing '''
    with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            uline = line.strip()
            words = uline.split()

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
                    fid = ''.join(sw_fid.group(0))
                    if fid == '128':
                        switchinfo.append('128')
                        #return switchinfo
                    else:
                        switchinfo.append(sw_fid.group(0))
                        #return switchinfo

                #return switchinfo
                key = re.search(r'========================', uline)
                if key:
                    skip = True
                    #print('KEY: True')

        ''' add default FID if not found '''
        if len(switchinfo) == 5:
            switchinfo.insert(len(switchinfo), '128')

        print(switchinfo)

