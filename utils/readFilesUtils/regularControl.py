#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/28 10:52
# @Author : 余少琪

import re
import datetime
import jsonpath
from faker import Faker
from utils.logUtils.logControl import ERROR
from utils.cacheUtils.cacheControl import Cache


class Context:
    def __init__(self):
        self.f = Faker(locale='zh_CN')

    @property
    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.f.phone_number()
        return phone

    @property
    def get_id_number(self) -> int:
        """

        :return: 随机生成身份证号码
        """

        id_number = self.f.ssn()
        return id_number

    @property
    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.f.name_male()
        return female_name

    @property
    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.f.name_female()
        return male_name

    @property
    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.f.email()
        return email

    @property
    def get_time(self) -> datetime.datetime:
        """
        计算当前时间
        :return:
        """

        return datetime.datetime.now()

    @property
    def random_int(self):
        """随机生成 0 - 9999 的数字"""
        numbers = self.f.random_int()
        return numbers

    @property
    def host(self) -> str:
        from utils.readFilesUtils.yamlControl import GetYamlData
        from common.setting import ConfigHandler

        # 从配置文件conf.yaml 文件中获取到域名，然后使用正则替换
        host = GetYamlData(ConfigHandler.config_path) \
            .get_yaml_data()['host']
        return host

    @property
    def app_host(self) -> str:
        """获取app的host"""
        from utils.readFilesUtils.yamlControl import GetYamlData
        from common.setting import ConfigHandler

        # 从配置文件conf.yaml 文件中获取到域名，然后使用正则替换
        host = GetYamlData(ConfigHandler.config_path) \
            .get_yaml_data()['app_host']
        return host


def sql_json(js_path, res):
    return jsonpath.jsonpath(res, js_path)[0]


def sql_regular(value, res=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    :param res: jsonpath使用的返回结果
    :param value:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)

    for i in sql_json_list:
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res))
        value = re.sub(pattern, key, value, count=1)

    return value


def cache_regular(value):
    """
    通过正则的方式，读取缓存中的内容
    例：$cache{login_init}
    :param value:
    :return:
    """
    # 正则获取 $cache{login_init}中的值 --> login_init
    regular_data = re.findall(r"\$cache\{(.*?)\}", value)

    # 拿到的是一个list，循环数据
    for i in regular_data:
        pattern = re.compile(r'\$cache\{' + i.replace('$', "\$").replace('[', '\[') + r'\}')
        cache_data = Cache(i).get_cache()
        # 使用sub方法，替换已经拿到的内容
        value = re.sub(pattern, cache_data, value)
    return value


def regular(target):
    """
    使用正则替换请求数据
    :return:
    """
    try:
        regular_pattern = r'\${{(.*?)}}'
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)
            value_data = getattr(Context(), key)
            if isinstance(value_data, (int, float)):
                regular_pattern = r'\'\${{(.*?)}}\''
                target = re.sub(regular_pattern, str(value_data), target, 1)
            else:
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target

    except AttributeError:
        ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确", target)
        raise
