import hashlib
import json
import sys
import time
from random import random
def custom_print(*args, sep=' ', end='\n', file=None):
    """
    print补丁
    :param x:
    :return:
    """
    # 获取被调用函数在被调用时所处代码行数
    line = sys._getframe().f_back.f_lineno
    # 获取被调用函数所在模块文件名
    # file_name = sys._getframe(1).f_code.co_filename
    # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    sys.stdout.write(f'{line}:  \033[0;32m{" ".join(args)}\033[0m\n')



def create_digest(username):
    KEY = b'xdf'
    PERSON = b'xzz'
    timestamp = time.time()
    salt = str(random()).encode('utf-8')[:16]
    digest = hashlib.blake2b((username + str(timestamp)).encode('utf-8'), key=KEY, salt=salt, person=PERSON).hexdigest()
    return digest
    # print(digest.hexdigest())

def postman_to_markdown(postmanfilename, postman_varname, postman_varname_global, markdowndocname=None):
    with open(postmanfilename, 'r', encoding='UTF-8') as f1:
        content = json.load(f1)
    markdowndocname = content['info']['name'] + '接口文档.md'
    with open(markdowndocname, 'w', encoding='UTF-8') as f:
        f.write('# ' + content['info']['name'] + '\n')
        for item in content['item']:
            custom_print(68)
            f.write('## ' + item['request']['method'] + ' ' + item['name'] + '\n')
            f.write(item['request']['url']['raw'] + '\n')

            try:
                formdata = item['request']['body']['formdata']

            except KeyError:
                pass
            else:
                if formdata:
                    f.write('### ' + 'BODY formdata' + '\n')
                    f.write('参数名|参数值' + '\n')
                    f.write('---:|---:|' + '\n')
                    for i in formdata:
                        custom_print(72)
                        f.write(i['key'] + '|' + i['value'] + '\n')
    with open(postman_varname, 'r', encoding='UTF-8') as f:
        content = json.load(f)
    with open(postman_varname_global, 'r', encoding='UTF-8') as f2:
        content2 = json.load(f2)
    key_values = {value['key']: value['value'] for value in content['values']}
    key2_values = {value['key']: value['value'] for value in content2['values']}
    key_values.update(key2_values)
    with open(markdowndocname, 'r', encoding='UTF-8') as f1:
        content1 = f1.read()
    for k, v in key_values.items():
        custom_print(k, v)
        if k in content1:
            custom_print(k)
            content1 = content1.replace('{{' + k + '}}', v)
    with open(markdowndocname, 'w', encoding='UTF-8') as f2:
        f2.write(content1)

if __name__ == '__main__':
    postman_to_markdown('logreport.postman_collection.json', 'logreport_outer_net.postman_environment.json', 'global.postman_environment.json')

