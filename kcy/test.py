import os.path
import traceback
from docxtpl import DocxTemplate

import pandas as pd
from decimal import Decimal

read_excel = r"C:\Users\11830\Desktop\成都市第一人民医院中西结合提升项目\成都市第一人民医院中西结合提升项目.xlsx"
title = ["楼层", "名称", "长", "宽", "个数", "合计", "单价", "总价"]
result_dict = {}
df_data = pd.read_excel(read_excel, skiprows=1).fillna("")
data_eff = df_data.iloc[0:393]  # 393
data_eff.columns = title
print(len(data_eff))
lou_sum = 0
lc_square = []
lc_name = ""
erro_index = 0
for index, row in data_eff.iterrows():
    # print(f"当前行数：{index}")
    # print(f"以下是数据：\n{row}")
    # 楼岑有值的时候添加楼层
    if row["楼层"] != "":
        lc_name = row["楼层"]
        print(f"当前行数：{index + 1},需要添加楼层")
        print(row["楼层"])
        result_dict[lc_name] = []
        lou_sum = 0  # 当楼层跳到下一层的时候，需要对累计的合计平方数进行初始化
        lc_square = []
    if row["长"] == "合计":
        erro_index += 1
        print(f"当前行数：{index + 1},需要累计合计")
        try:
            if data_eff.iloc[index + 1, 0] != '':  # 当前这一行的下一行
                print(f"当前行数：{index + 1},需要将这层楼的数据添加到字典")
        except:
            print(traceback.format_exc())
        finally:
            lou_sum = round(Decimal(row["合计"]) + lou_sum, 2)
            print(lou_sum)
            result_dict[lc_name] = {"内容": lc_square, "合计": lou_sum}

    else:
        # 组装数据：(长*宽*个数) round(Decimal(row['长']),2)保留两位小数
        element_square = f"({row['长']}*{row['宽']}*{row['个数']})"
        print(f"当前行数：{index + 1},正在将数据添加到列表中")
        lc_square.append(element_square)

    # print(f"当前行数：{index}")
    # print(f"以下是数据：\n{row}")
# print(erro_index)
# print(result_dict)
# print(len(result_dict))
# for key,value in result_dict.items():
#     print(f"当前楼层-{key}：一共{value['合计']}")

# 根据模板表生成文件
base_path = r"C:\Users\11830\Desktop\成都市第一人民医院中西结合提升项目\生成文件\模板.docx"
s_path = r"C:\Users\11830\Desktop\成都市第一人民医院中西结合提升项目\生成文件"
doc = DocxTemplate(base_path)
for key, value in result_dict.items():
    floor = key
    area_sum = value['合计']
    content = "+".join(value['内容']) + "\n" + "共计：" + str(area_sum) + "m²"
    save_path = os.path.join(s_path, key + ".docx")
    doc.render({"floor": floor, "content": content})
    doc.save(save_path)
