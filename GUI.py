import sys
from collections import OrderedDict
from pathlib import Path
from PySide6.QtCore import QFile, Qt, QThread
from PySide6.QtGui import QTextCursor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QFileDialog, QFrame
import image_piecer
import pandas as pd


class MyThread(QThread):
    def __init__(self, style_dict: Path, info_df: pd.DataFrame, enhance_level=2, output_path=None):
        super().__init__()
        self.style_dict = style_dict
        self.info_df = info_df
        self.enhance_level = enhance_level
        self.output_path = output_path

    def run(self):
        style_dict = self.style_dict
        info_df = self.info_df
        enhance_level = self.enhance_level
        output_path = self.output_path
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
        for style, pics in style_dict.items():
            df = info_df.loc[info_df['款号'] == style, cols]
            if df.empty:
                print(f'{style}不存在于excel内，请检查！！！！\n\n\n\n')
            else:
                style, size, pcs_box = df.values[0]
                image_piecer.ImagePiecer(style_name=style, style_sizes=size, pcs_box=pcs_box, pics=pics,
                                         enhance_level=enhance_level, output=output_path)

        print('完成拼图！')


class MyWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.__load_ui()  # load UI

        self.style_dict = OrderedDict()

        'redirect stdout to self.form.myConsole'
        sys.stdout = self
        sys.stderr = self

        self._cursor = self.form.myConsole.textCursor()
        self.form.myConsole.setTextCursor(self._cursor)

        self.form.myConsole.document().setMaximumBlockCount(20)

        'set connections'
        self.__connect_functions()

        self.form.show()

    def __load_ui(self):
        loader = QUiLoader()
        uifile = QFile("GUI.ui")
        uifile.open(QFile.ReadOnly)
        self.form = loader.load(uifile)
        uifile.close()

    def __connect_functions(self):
        self.form.run_pushButton.clicked.connect(self.__run)
        self.form.open_file_pushButton.clicked.connect(self.__open_input_file)
        self.form.open_input_pushButton.clicked.connect(self.__open_input_folder)

        self.form.open_style_info_pushButton.clicked.connect(self.__open_style_info_file)
        self.form.add_input_pushButton.clicked.connect(self.__add_path_to_tree)
        self.form.delete_path_pushButton.clicked.connect(self.__delete_paths)
        self.form.open_output_pushButton.clicked.connect(self.__open_output_folder)

    def __delete_paths(self):
        selected_items = self.form.tree.selectedItems()
        for item in selected_items:
            parent = item.parent()
            if isinstance(parent, QTreeWidgetItem):
                toplevel = parent
                style = toplevel.text(0)
                path = Path(item.text(1))
                if style in self.style_dict:
                    self.style_dict[style].remove(path)
                else:
                    print(f'{style}不在{self.style_dict}里')

                toplevel.removeChild(item)
                toplevel.setText(1, f'{toplevel.childCount()}张图')
                print('删除成功')
            elif parent is None:
                style = item.text(0)
                del self.style_dict[style]
                item.removeChild(item)
                print('删除成功')

    def __add_path_to_tree(self):
        paths = self.form.input_path_lineEdit.text()
        if ";" in paths:
            paths = paths.split(";")
            paths = [Path(path) for path in paths]
        else:
            paths = (Path(paths),)
        for path in paths:
            if path.exists():
                if path.is_file():
                    item = self.form.tree.findItems(str(path), Qt.MatchFlag.MatchRecursive, 1)
                    if not item:
                        style = path.stem.split(" ")[0]
                        if style not in self.style_dict:
                            if not isinstance(path, set):
                                paths = set((path,))
                            self.style_dict[style] = paths
                        else:
                            self.style_dict[style].add(path)
                        if self.form.tree.topLevelItemCount() == 0:
                            top_item = QTreeWidgetItem(self.form.tree, [str(style), '1张图'])

                            QTreeWidgetItem(top_item, [None, path.as_posix()])
                        else:
                            for i in range(self.form.tree.topLevelItemCount()):
                                top_item = self.form.tree.topLevelItem(i)
                                if style == top_item.text(0):
                                    QTreeWidgetItem(top_item, [None, str(path)])
                                    top_item.setText(1, f"{top_item.childCount()}张图")
                                    break
                                else:
                                    top_item = QTreeWidgetItem(self.form.tree, [str(style), '1张图'])

                                    QTreeWidgetItem(top_item, [None, str(path)])
                                    break

                    else:
                        print(f'该路径已经存在{item.count}')
                        return

                elif path.is_dir():
                    style_dict = image_piecer.ImagePiecer.group_pics(path)
                    for k, v in style_dict.items():

                        if k not in self.style_dict:
                            if isinstance(v, set):
                                self.style_dict[k] = v
                            else:
                                raise ValueError(f"输入的字典的values必须是set！{v}")
                        else:
                            if isinstance(v, Path):
                                self.style_dict[k].add(v)
                            elif isinstance(v, set):
                                self.style_dict[k].update(v)
                            else:
                                print(f'无法将以下元素加入self.style_dict里:\n{k, v}')

                    self.__refresh_tree()
                else:
                    return

            else:
                print(f'输入的路径{str(path)}不存在。')

        self.form.tree.sortItems(0, Qt.AscendingOrder)

    def __refresh_tree(self):
        self.form.tree.clear()
        for style, paths in self.style_dict.items():
            toplevel_item = QTreeWidgetItem(self.form.tree, [style, f"{len(paths)}张图"])
            for path in paths:
                QTreeWidgetItem(toplevel_item, ["", str(path)])

    def __open_input_file(self):
        path, file_type = QFileDialog.getOpenFileNames(None,
                                                       '选取文件',
                                                       str(Path.cwd()),
                                                       "jpg/png 文件 *.jpg *.jpeg *.png")
        if path:
            match len(path):
                case 0:
                    return
                case 1:
                    if path[0] != "":
                        self.form.input_path_lineEdit.setText(path[0])
                        return
                case _:
                    paths = ';'.join(path)
                    self.form.input_path_lineEdit.setText(paths)
                    return
        else:
            return

    def __open_style_info_file(self):
        path, file_type = QFileDialog.getOpenFileName(None,
                                                      '选取文件',
                                                      str(Path.cwd()),
                                                      "xls/xlsx/csv 文件 *.xls *.xlsx *.csv;; 所有文件 *.*")
        if path != '':
            self.form.style_info_lineEdit.setText(path)
        else:
            pass

    def __open_input_folder(self):
        path = QFileDialog.getExistingDirectory(self,
                                                "选取文件夹",
                                                str(Path.cwd()))
        if path != '':
            self.form.input_path_lineEdit.setText(path)
        else:
            pass

    def __open_output_folder(self):
        path = QFileDialog.getExistingDirectory(self,
                                                "选取文件夹",
                                                str(Path.cwd()))
        path = Path(path)
        if path != "":
            self.form.output_path_lineEdit.setText(str(path))
        else:
            pass

    def __run(self):
        excel_path = self.form.style_info_lineEdit.text()
        excel_path = Path(excel_path)
        if excel_path.suffix in (".xls", ".xlsx"):
            info_df = pd.read_excel(excel_path)
        elif excel_path.suffix == ".csv":
            info_df = pd.read_csv(excel_path)
        else:
            try:
                info_df = pd.read_table(excel_path)
            except Exception as e:
                print(e)
                print(f'输入的产品数据:{excel_path.as_posix()}不是xls/xlsx/csv文件, 请转换格式后重试！')
                return
        enhance_level = self.form.enhance_spinBox.value()

        output_path = self.form.output_path_lineEdit.text() or Path("./output/")

        self.thread = MyThread(
            style_dict=self.style_dict, info_df=info_df,
            enhance_level=enhance_level, output_path=output_path
        )
        self.thread.start()

    def write(self, text):
        sys.__stderr__.write(text)
        self._cursor.movePosition(QTextCursor.MoveOperation.End)
        self._cursor.insertText(text)
        self.form.myConsole.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def flush(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    sys.exit(app.exec())
