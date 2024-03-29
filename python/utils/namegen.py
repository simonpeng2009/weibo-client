# -*- coding: UTF-8 -*-
import random

surname = ["李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
           "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
           "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
           "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕",
           "苏", "卢", "蒋", "蔡", "贾", "丁", "魏", "薛", "叶", "阎",
           "余", "潘", "杜", "戴", "夏", "钟", "汪", "田", "任", "姜",
           "范", "方", "石", "姚", "谭", "廖", "邹", "熊", "金", "陆",
           "郝", "孔", "白", "崔", "康", "毛", "邱", "秦", "江", "史",
           "顾", "侯", "邵", "孟", "龙", "万", "段", "章", "钱", "汤",
           "尹", "黎", "易", "常", "武", "乔", "贺", "赖", "龚", "文" ]

boyname = ["伟", "刚", "勇", "毅", "俊", "峰", "强", "军", "平", "保",
           "东", "文", "辉", "力", "明", "永", "健", "世", "广", "志",
           "义", "兴", "良", "海", "山", "仁", "波", "宁", "贵", "福",
           "生", "龙", "元", "全", "国", "胜", "学", "祥", "才", "发",
           "武", "新", "利", "清", "飞", "彬", "富", "顺", "信", "子",
           "杰", "涛", "昌", "成", "康", "星", "光", "天", "达", "安",
           "岩", "中", "茂", "进", "林", "有", "坚", "和", "彪", "博",
           "诚", "先", "敬", "震", "振", "壮", "会", "思", "群", "豪",
           "心", "邦", "承", "乐", "绍", "功", "松", "善", "厚", "庆",
           "磊", "民", "友", "裕", "河", "哲", "江", "超", "浩", "亮",
           "政", "谦", "亨", "奇", "固", "之", "轮", "翰", "朗", "伯",
           "宏", "言", "若", "鸣", "朋", "斌", "梁", "栋", "维", "启",
           "克", "伦", "翔", "旭", "鹏", "泽", "晨", "辰", "士", "以",
           "建", "家", "致", "树", "炎", "德", "行", "时", "泰", "盛",
           "雄", "琛", "钧", "冠", "策", "腾", "楠", "榕", "风", "航",
           "弘"]

girlname = ["秀", "娟", "英", "慧", "巧", "美", "娜", "静", "淑", "惠",
            "珠", "翠", "雅", "芝", "玉", "萍", "红", "娥", "玲", "芬",
            "芳", "燕", "彩", "春", "菊", "兰", "凤", "洁", "梅", "琳",
            "素", "云", "莲", "环", "雪", "爱", "妹", "霞", "香", "月",
            "莺", "媛", "艳", "琼", "珍", "贞", "莉", "桂", "娣", "叶",
            "璧", "璐", "娅", "琦", "晶", "妍", "茜", "秋", "珊", "莎",
            "锦", "黛", "青", "倩", "婷", "姣", "婉", "娴", "瑾", "颖",
            "露", "瑶", "怡", "婵", "雁", "蓓", "纨", "仪", "丹", "蓉",
            "眉", "君", "琴", "蕊", "薇", "菁", "梦", "岚", "苑", "婕",
            "馨", "瑗", "琰", "韵", "融", "园", "艺", "咏", "卿", "澜",
            "纯", "毓", "悦", "昭", "冰", "琬", "茗", "希", "宁", "欣",
            "飘", "育", "滢", "馥", "筠", "柔", "竹", "霭", "凝", "霄",
            "枫", "芸", "菲", "伊", "宜", "可", "姬", "舒", "影", "荔",
            "枝", "思", "丽"]

def getBoyName():
    return random.choice(surname)+random.choice(boyname)+random.choice(boyname)

def getGirlName():
    return random.choice(surname)+random.choice(girlname)+random.choice(girlname)

if __name__ == "__main__":
    for i in range(1,100):
        print getBoyName(),getGirlName()