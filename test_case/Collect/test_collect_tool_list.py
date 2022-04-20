#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022-04-20 14:01:41
# @Author : 七月


import allure
import pytest
from common.setting import ConfigHandler
from utils.readFilesUtils.get_yaml_data_analysis import CaseData
from utils.assertUtils.assertControl import Assert
from utils.requestsUtils.requestControl import RequestControl


TestData = CaseData(ConfigHandler.data_path + r'Collect/collect_tool_list.yaml').case_process()


@allure.epic("开发平台接口")
@allure.feature("收藏模块")
class TestCollectToolList:

    @allure.story("收藏网址列表接口")
    @pytest.mark.parametrize('in_data', TestData, ids=[i['detail'] for i in TestData])
    def test_collect_tool_list(self, in_data, case_skip):
        """
        :param :
        :return:
        """

        res = RequestControl().http_request(in_data)
        Assert(in_data['assert']).assert_equality(response_data=res['response_data'], 
                                                  sql_data=res['sql_data'])


if __name__ == '__main__':
    pytest.main(['test_collect_tool_list.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
