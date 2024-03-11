import os;
infos = [
    {
        'sno': str(os.environ['XUHAO']),         # 学号
        'pwd': str(os.environ['MIMA']),         # 密码
        'devName': '101-026',   # 预约的座位号（不足3位数的要补零）
        'name': '猪猪侠',        # 随便起个名字
        'periods': (            # 预约时间段（每段时间不能超过4小时）
            ('8:30:00', '12:30:00'),
            ('14:00:00', '18:00:00'),
            ('18:00:00', '22:00:00')
        ),
        'pushplus': '',         # pushplus 的 token（用于推送消息到微信）
    },

    # # 如果只是一个人预约座位，不需要帮别人预约签到，则可把下面三个字典注释/删除
    {
        'sno': str(os.environ['XUHAO1']),
        'pwd': str(os.environ['MIMA1']),
        'devName': '3C-049',
        'name': '皮卡丘',
        'periods': (
            ('8:30:00', '12:30:00'),
            ('14:00:00', '18:00:00'),
            ('18:00:00', '22:00:00')
        ),
        'pushplus': '',
    },
    {
        'sno': str(os.environ['XUHAO2']),
        'pwd': str(os.environ['MIMA2']),
        'devName': '3c-054',
        'name': '熊猫',
        'periods': (
            ('8:30:00', '12:30:00'),
            ('14:00:00', '18:00:00'),
            ('18:00:00', '22:00:00')
        ),
        'pushplus': '',
    },
    # {
    #     'sno': '******',
    #     'pwd': '******',
    #     'devName': 'M301-001',
    #     'name': '小白',
    #     'periods': (
    #         ('8:30:00', '12:30:00'),
    #         ('12:30:00', '16:30:00'),
    #         ('16:30:00', '20:30:00'),
    #         ('20:30:00', '21:45:00')
    #     ),
    #     'pushplus': '',
    # },
]
