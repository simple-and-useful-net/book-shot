"""
------------------------------------------------------------------------
連番付きファイル名生成関数

この関数は、指定された接頭語と接尾語に基づいて、次に利用可能な連番付きのファイル名を生成します。
ファイル名の連番を管理し、新しいファイル名を自動的に決定する際に役立ちます。

    # 連番を保存するリスト
    numbers = [
        int(file.replace(prefix, "").replace(suffix, ""))  # 数字に変換
        for file in files
        if file.startswith(prefix) and file.endswith(suffix)
    ]
    # 連番を保存するリスト(数字変換チェックあり)
    numbers = [
        int(file[len(prefix):-len(suffix)])  # 数字に変換
        for file in files
        if file.startswith(prefix) and file.endswith(suffix)
        # 数字に変換できるかどうかをチェック
        if file[len(prefix):-len(suffix)].isdigit()
    ]    
------------------------------------------------------------------------
"""

import glob

dbg_flg = False

def get_filename(prefix, ext):

    suffix = "." + ext
    # file_pattern
    file_pattern = f"{prefix}*{suffix}"
    # パターンにマッチするファイルを取得
    files = glob.glob(file_pattern)
   
    
   # 連番を保存するリスト
    numbers = []
    for file in files:
        if file.startswith(prefix) and file.endswith(suffix):
            # ファイル名から数字の部分を取り出す
            number_str = file.replace(prefix, "").replace(suffix, "")
            try:
                number = int(number_str)
                numbers.append(number)
            except ValueError:
                # 数値に変換できない場合は無視
                pass    
    
    if dbg_flg:
        print("numbers=", numbers)

    # 最大値を求める、無い場合は０
    no = max(numbers, default=0)

    return f"{prefix}{no+1}{suffix}"


if  __name__ == "__main__":

  dbg_flg =True
  # 使用例
  prefix = "file"
  ext    = "txt"

  filename = get_filename(prefix, ext)
  print(f"ファイル名は: {filename}")

  with open(filename, "w") as f:
    f.write("test")

