from collections import OrderedDict

colors_trans = OrderedDict(
    [
        ('黑', 'NERO'),

        ('蓝', 'BLU'), ('湖蓝', 'AZZURRO'), ('新湖蓝', 'NUOVO\n AZZURRO'), ('天蓝', 'CELESTE'),
            ('牛仔蓝', 'DENIM'), ('蓝灰', 'BLU \nGRIGIO'), ('浅蓝', 'BLU \nCHIARO'),
            ('新宝蓝', 'BLU \nROYAL'), ('宝蓝', 'BLU \nROYAL'),

        ('灰', 'GRIGIO'), ('浅灰', 'GRIGIO \nCHIARO'), ('中灰', 'GRIGIO'),

        ('白', 'PANNA'), ('米白', 'PANNA'), ('奶白', 'PANNA'),

        ('米', 'BEIGE'), ('卡其', 'KHAKI'), ('驼', 'CAMELLO'),

        ('棕', 'MARRONE'), ('土', 'MARRONE'), ('浅棕', 'MARRONE \nCHIARO'),

        ('绿', 'VERDE'), ('墨绿', 'VERDE \nSCURO'), ('军绿', 'VERDE\nMILITARE'),
            ('草绿', 'VERDE \nERBA'), ('水绿', 'VERDE \nACQUA'), ('深绿', 'VERDE SCURO'),
            ('牛油绿', 'AVOCADO'), ('豆绿', 'AVOCADO'),

        ('红', 'ROSSO'), ('酒红', 'BORDEAUX'), ('大红', 'ROSSO \nFUOCO'),  ('玫红', 'FUCSIA'),

        ('紫', 'VIOLA'), ('浅紫', 'LILLA'),

        ('粉', 'ROSA'), ('粉红', 'ROSA'), ('皮粉', 'ROSA \nCHIARO'),

        ('草黄', 'GIALLO'), ('浅金', 'ORO \nCHIARO'),

        ('桔', 'ARANCIONE')
    ]
)


def rename_color(color: str):
    if not isinstance(color, str):
        raise ValueError(f"{color} is not a color.")
    color = str(color)
    color = color.replace("兰", "蓝").replace("色", "").replace("淡", "浅")
    return color

