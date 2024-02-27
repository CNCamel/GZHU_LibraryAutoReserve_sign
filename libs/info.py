infos = [
    {
        'sno': '',         # 学号
        'pwd': '',         # 密码
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
    # {
    #     'sno': '******',
    #     'pwd': '******',
    #     'devName': 'G101-008',
    #     'name': '皮卡丘',
    #     'periods': (
    #         ('8:30:00', '12:30:00'),
    #         ('12:30:00', '16:30:00'),
    #         ('16:30:00', '20:30:00'),
    #         ('20:30:00', '21:45:00')
    #     ),
    #     'pushplus': '',
    # },
    # {
    #     'sno': '******',
    #     'pwd': '******',
    #     'devName': '3c-016',
    #     'name': '熊猫',
    #     'periods': (
    #         ('8:30:00', '12:30:00'),
    #         ('12:30:00', '16:30:00'),
    #         ('16:30:00', '20:30:00'),
    #         ('20:30:00', '21:45:00')
    #     ),
    #     'pushplus': '',
    # },
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
