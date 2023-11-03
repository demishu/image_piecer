import pandas as pd

import image_piecer as ip
if __name__ == "__main__":
    df = pd.read_excel('尺码竖排商品数据.xlsx')
    ip.ImagePiecer.run(r"D:\wdir\扣好的图/", df, enhance_level=5)
