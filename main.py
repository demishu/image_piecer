import pandas as pd
from pathlib import Path
import re
import image_piecer as ip

if __name__ == "__main__":
    df = pd.read_excel('尺码竖排商品数据.xlsx')
    ip.ImagePiecer.run(r"D:\wdir\扣好的图/", df, enhance_level=2)
#
# if __name__ == "__main__":
#     df = pd.read_excel('尺码竖排商品数据.xlsx')
#     path = Path(r'D:\wdir\原图')
#     pics = path.glob("**/*.jpg")
#     for pic in pics:
#         if "款号" in pic.stem:
#             new_pic_name = Path(f'{pic.parent.as_posix()}/{pic.name.replace("款号", "")}')
#             pic.rename(new_pic_name)
#             pic = new_pic_name
#         if " " not in pic.stem:
#             pattern = r'(\d+)(\D+)'
#             repl = r'\1 \2'
#             filename = re.sub(pattern, repl, pic.stem)
#             re.sub(r'\.+', r'\.', filename)
#             print(filename)
#             pic.rename(f'{pic.parent.as_posix()}/{re.sub(pattern, repl, pic.stem)}{pic.suffix}')
#     ip.ImagePiecer.run(path, df, enhance_level=3)
#
