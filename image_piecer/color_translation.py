from collections import OrderedDict
import re
chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
colors_trans = OrderedDict(
    [
        ('黑', 'NERO'),

        ('蓝', 'BLU'), ('湖蓝', 'AZZURRO'), ('新湖蓝', 'NUOVO\n AZZURRO'), ('天蓝', 'CELESTE'),
            ('牛仔蓝', 'DENIM'), ('蓝灰', 'BLU \nGRIGIO'), ('浅蓝', 'BLU \nCHIARO'),
            ('新宝蓝', 'BLU \nROYAL'), ('宝蓝', 'BLU \nROYAL'), ('新蓝', 'BLU'), ('灰蓝', 'GRIGIO BLU'),
            ('藏青', 'BLU\nSCURO'),

        ('灰', 'GRIGIO'), ('浅灰', 'GRIGIO \nCHIARO'), ('中灰', 'GRIGIO'),

        ('白', 'PANNA'), ('米白', 'PANNA'), ('奶白', 'PANNA'),

        ('米', 'BEIGE'), ('卡其', 'KHAKI'), ('驼', 'CAMELLO'),

        ('棕', 'MARRONE'), ('土', 'MARRONE'), ('浅棕', 'MARRONE \nCHIARO'), ('铁锈红', 'MARRONE'),('咖', 'CAFFE'),

        ('绿', 'VERDE'), ('墨绿', 'VERDE \nSCURO'), ('军绿', 'VERDE\nMILITARE'),
            ('草绿', 'VERDE \nERBA'), ('水绿', 'VERDE \nACQUA'), ('深绿', 'VERDE SCURO'),
            ('牛油绿', 'AVOCADO'), ('豆绿', 'AVOCADO'),

        ('红', 'ROSSO'), ('酒红', 'BORDEAUX'), ('大红', 'ROSSO \nFUOCO'),  ('玫红', 'FUCSIA'),

        ('紫', 'VIOLA'), ('浅紫', 'LILLA'),

        ('粉', 'ROSA'), ('粉红', 'ROSA'), ('皮粉', 'ROSA \nCHIARO'),

        ('黄', 'GIALLO'), ('草黄', 'GIALLO'), ('浅金', 'ORO \nCHIARO'),

        ('桔', 'ARANCIONE')
    ]
)


def rename_color(color: str):
    if not isinstance(color, str):
        raise ValueError(f"{color} is not a color.")
    color = str(color)

    color = color.replace("兰", "蓝").replace("色", "").replace("淡", "浅")
    chinese_color = re.findall(chinese_pattern, color)
    chinese_color = "".join(chinese_color)
    print(chinese_color)
    chinese_color = re.sub(r'[A-Z0-9]#', '', chinese_color)
    if chinese_color:
        return chinese_color
    else:
        raise ValueError(f'color {color} is illegal! result is {chinese_color}')
