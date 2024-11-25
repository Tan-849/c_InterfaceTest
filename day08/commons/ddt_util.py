import yaml


def read_testcase(yaml_path):
    with open(yaml_path, 'r', encoding="utf-8") as f:
        case_list = yaml.safe_load(f)
        if len(case_list) >=2:
            # print("流程用例，多个接口请求 [[{接口1},{接口2},....正例],[{接口1},{接口2},....反例]]")
            # for case in case_list:
            #     new_caseinfo = ddts(dict(*case))
            return [case_list]
        else:
            if "parametrize" in dict(*case_list).keys():
                # print("数据驱动用例 [{正例},{反例1},{反例2},...]")
                new_caseinfo=ddts(*case_list)
                return new_caseinfo
            else:
                return case_list

def ddts(caseinfo:dict):
    # 数据驱动用例 [{正例},{反例1},{反例2},...]
    # parametrize:
    # - ["username", "password"]
    # - ["admin", "123"]
    # - ["admin", "admin"]
    # - ["123", "123"]
    parameterize_list =  caseinfo["parametrize"]
    len_flag = True #检查数据列表的各个元素长度是否一样
    args_count = len(parameterize_list[0]) # 参数名的长度
    for param in parameterize_list:
        if  len(param) != args_count:
            len_flag = False
            print("parameterize 数据长度不一致")
            break
    # 长度没问题
    str_caseinfo = yaml.safe_dump(caseinfo,allow_unicode=True)
    new_caseinfo = []
    if len_flag:
        # 因为第一行放的是参数名字，因此要跳过[0]
        for x in range(1,len(parameterize_list)):
            raw_cassinfo = str_caseinfo
            for y in range(0,args_count):
                if isinstance(parameterize_list[x][y],str) and parameterize_list[x][y].isdigit():
                    parameterize_list[x][y]="'"+parameterize_list[x][y]+"'"
                raw_cassinfo = raw_cassinfo.replace("$ddt{"+parameterize_list[0][y]+"}",str(parameterize_list[x][y]))
            case_dict = yaml.safe_load(raw_cassinfo)
            case_dict.pop("parametrize")
            new_caseinfo.append(case_dict)
    return new_caseinfo
