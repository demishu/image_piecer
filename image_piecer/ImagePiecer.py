from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pandas as pd
from collections.abc import Iterable
from pathlib import Path
from .color_translation import colors_trans, rename_color
from collections import OrderedDict

class ImagePiecer:
    """piece style's pics in a Huger Pic"""

    def __init__(
            self, style_name, style_sizes, pcs_box,
            pics: Iterable[Path], enhance_level, output: Path = None
    ):
        self._style_name = str(style_name)
        self._style_sizes = str(style_sizes)
        self._pcs_box = int(pcs_box)
        self._enhance_level = int(enhance_level)
        self._pics = []
        if all([isinstance(pic, Path) for pic in pics]):
            self._pics_path = pics
        else:
            raise ValueError(f"input pics = {pics} is an illegal input.")

        self._output_path = output or Path("./output/")
        if output and not isinstance(output, Path):
            try:
                output = Path(output)
            except Exception:
                raise IOError(f"output path = {output} is not a valid path.")

        self._output_path.mkdir(exist_ok=True)
        self._initialize_pics()
        self._piece()

    @staticmethod
    def _get_color_from_stem(stem):
        stem = stem.replace('加单', "")
        stem = stem.split(" ")[1]
        stem = stem.lstrip("0123456789#")
        stem = rename_color(stem)
        return stem

    def _initialize_pics(self):
        od = OrderedDict([(self._get_color_from_stem(path.stem), path) for path in self._pics_path])
        pics_path = []
        for color in colors_trans:
            if color in od.keys():
                pics_path.append(od[color])

        self._pics_path = pics_path
        for pic_path in self._pics_path:
            self._load_img_and_add_color_topleft(pic_path)

    def _enhance_img(self, img: Image) -> Image:
        """enhance img details."""
        enhancer = ImageEnhance.Sharpness(img)

        enhanced_img = enhancer.enhance(self._enhance_level)
        return enhanced_img

    @staticmethod
    def _adj_img_size(img: Image) -> Image:
        """adj img to 1600 width or 1600 height, to make img uniform"""
        width, height = img.size
        if width < height:
            ratio = 1600 / height

        else:
            ratio = 1600 / width
        width, height = (int(width * ratio), int(height * ratio))

        img = img.resize((width, height), Image.LANCZOS)
        left = int(img.size[0] / 2 - 1600 / 2)
        upper = int(img.size[1] / 2 - 1600 / 2)
        right = left + 1600
        lower = upper + 1600
        img = img.crop((left, upper, right, lower))
        img = img.convert('RGBA')
        new_img = Image.new('RGBA', (1600, 1600), color=(255, 255, 255))
        new_img.paste(img, (0, 0), img)
        new_img = new_img.convert('RGB')
        return new_img

    @staticmethod
    def _add_text(img: Image, text: str, coordinate: tuple[int, int], color: tuple[int, int, int],
                  font_size, central_alignment=False):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("msyhbd.ttc", font_size)
        if central_alignment is True:
            img_width, img_height = img.size
            font_w = font.getlength(text)
            coordinate = ((img_width - font_w) / 2, coordinate[1])
        draw.text(xy=coordinate, text=text, fill=color, font=font)  # 写字
        return img

    def _load_img_and_add_color_topleft(self, img_path: Path):
        img = Image.open(img_path)
        img = self._adj_img_size(img)
        img = self._enhance_img(img)
        color = self._get_color_from_stem (img_path.stem.replace(self._style_name, ""))
        color_text_on_pic = f'{color}\n{colors_trans[rename_color(color)]}'
        img = self._add_text(img, color_text_on_pic, (100, 100), (0, 0, 0), 70)
        self._pics.append(img)

    def _add_style_info(self, img: Image) -> Image:
        text = f"""
款号/ARTICOLO:{self._style_name}      尺码/TAGLIE:{self._style_sizes}       件数/箱 / PZ/BOX:{self._pcs_box}"""
        size = img.size
        place = (size[0] / 3, size[1] - 300)
        img = self._add_text(img, text, place, color=(100, 100, 100), font_size=100, central_alignment=True)
        return img

    def _piece(self):
        """拼接图片，并输出到输出目录去。"""
        print(f'\n开始拼接{self._style_name}款：')
        tot_pcs = len(self._pics)
        if tot_pcs % 3 == 0 or tot_pcs % 5 == 0:
            col = 3
        elif tot_pcs == 4:
            col = 2
        else:
            col = 4

        row = tot_pcs // col + 1 if tot_pcs % col else tot_pcs // col
        pic_height = 1600
        pic_width = 1600
        save_quality = 50
        pieced_pic_width = min(3500, pic_width * col) if tot_pcs < 3 else pic_width * col
        pieced_pic = Image.new('RGB', (pieced_pic_width, pic_height * row), color=(255, 255, 255))
        print(f'行数={col},\n列数={row}.\n图片数量={tot_pcs}')
        for i in range(row):
            pics_col_n = min(col, len(self._pics))
            pics_on_col = Image.new('RGB', (pic_width * pics_col_n, pic_height), color=(255, 255, 255))
            for j in range(col):
                if len(self._pics) == 0:
                    break
                img = self._pics.pop(0)
                print(f'第{i + 1}行   第{j + 1}列')
                pics_on_col.paste(img, (0 + pic_width * j, 0))
            pieced_pic.paste(pics_on_col, (int((pieced_pic_width - pics_on_col.size[0]) / 2), pic_height * i))
        size = pieced_pic.size
        size = (size[0], size[1] + 400)

        output_pic = Image.new('RGB', size, color=(0, 0, 0))
        output_pic.paste(pieced_pic, (0, 200))
        output_pic = self._add_style_info(output_pic)
        output_pic.save(f'{self._output_path}/{self._style_name}.jpg', quality=save_quality)

    @staticmethod
    def group_pics(path):
        input_pics_path = Path(path)
        pics = list(input_pics_path.glob('**/*.jpg')) + list(input_pics_path.glob('**/*.jpeg'))\
               + list(input_pics_path.glob('**/*.png'))
        pics = [(pic.stem.split(' ')[0].replace('加单', ''), pic) for pic in pics]
        styles_dict = {styles: set() for styles, _ in pics}
        for styles, pic in pics:
            styles_dict[styles].add(pic)
        return styles_dict
    
    @staticmethod
    def run(input_pics_path: Path, info_df: pd.DataFrame, enhance_level=2, output_path=None):
        cols = ['款号', '尺码', '件数/箱']
        if isinstance(info_df, pd.DataFrame):
            if not info_df.empty:
                for col in cols:
                    if col not in info_df.columns:
                        raise Exception(f"input dataframe hasn't got {cols}")
            else:
                raise Exception(f"dataframe empty!!")
        else:
            raise Exception(f"plz input dataframe!!!")

        styles_dict = ImagePiecer.group_pics(input_pics_path)
        [print(style, len(styles_dict[style])) for style in styles_dict]
        for style, pics in styles_dict.items():
            df = info_df.loc[info_df['款号'] == style, cols]
            style, size, pcs_box = df.values[0]
            ImagePiecer(style_name=style, style_sizes=size, pcs_box=pcs_box, pics=pics,
                        enhance_level=enhance_level, output=output_path)
