from collections import OrderedDict
import re
chinese_pattern = re.compile(r'([\u4e00-\u9fa5]+)')
colors_trans = OrderedDict(
    [
        ('主图', "FOTO"),
        ('黑', 'NERO'),

        ('蓝', 'BLU'), ('湖蓝', 'AZZURRO'), ('新湖蓝', 'NUOVO\n AZZURRO'), ('天蓝', 'CELESTE'),
            ('牛仔蓝', 'DENIM'), ('蓝灰', 'BLU \nGRIGIO'), ('浅蓝', 'BLU \nCHIARO'),
            ('新宝蓝', 'BLU \nROYAL'), ('宝蓝', 'BLU \nROYAL'), ('新蓝', 'BLU'), ('灰蓝', 'GRIGIO BLU'),
            ('藏青', 'BLU\nSCURO'), ('新雾蓝', 'BLU\nMITICO'), ('老蓝', 'BLU\nSCURO'),

        ('灰', 'GRIGIO'), ('灰绿', 'GRIGIO\nVERDE'), ('浅灰', 'GRIGIO \nCHIARO'), ('中灰', 'GRIGIO'), ('银灰', 'ARGENTO'),
        ('灰蓝', 'GRIGIO\nBLU'),

        ('白', 'PANNA'), ('米白', 'PANNA'), ('奶白', 'PANNA'),

        ('米', 'BEIGE'), ('卡其', 'KHAKI'), ('驼', 'CAMELLO'),

        ('棕', 'MARRONE'),('新棕', 'MARRONE\nMITICO'), ('土', 'MARRONE'), ('浅棕', 'MARRONE \nCHIARO'), ('铁锈红', 'MARRONE'),('咖', 'CAFFE'),
            ('棕灰', 'MARRONE\nMITICO'),

        ('绿', 'VERDE'), ('墨绿', 'VERDE \nSCURO'), ('军绿', 'VERDE\nMILITARE'),
            ('草绿', 'VERDE \nERBA'), ('水绿', 'VERDE \nACQUA'), ('深绿', 'VERDE SCURO'),
            ('牛油绿', 'AVOCADO'), ('豆绿', 'AVOCADO'),

        ('红', 'ROSSO'), ('酒红', 'BORDEAUX'), ('大红', 'ROSSO \nFUOCO'),  ('玫红', 'FUCSIA'),

        ('紫', 'VIOLA'), ('浅紫', 'LILLA'), ('新紫', 'VIOLA\nMITICO'),

        ('粉', 'ROSA'), ('粉红', 'ROSA'), ('皮粉', 'ROSA \nCHIARO'),

        ('黄', 'GIALLO'), ('草黄', 'GIALLO'), ('浅金', 'ORO \nCHIARO'),

        ('桔', 'ARANCIONE')
    ]
)


def rename_color(color: str):
    if not isinstance(color, str):
        raise ValueError(f"{color} is not a color.")
    color = str(color)

    color = color.replace("兰", "蓝").replace("色", "").replace("淡", "浅").replace("#", "")
    m = re.search(chinese_pattern, color)
    chinese_color = m.group(1)
    chinese_color = re.sub(r'[A-Za-z0-9]*', '', chinese_color)
    result = colors_trans.get(chinese_color)
    if not result:
        print(f'\n\n{chinese_color} not in colors_trans, check original stem{color}\n\n')
        return
    if chinese_color:
        return chinese_color
    else:
        raise ValueError(f'color {color} is illegal! result is {chinese_color}')
