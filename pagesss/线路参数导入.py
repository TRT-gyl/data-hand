import os

import streamlit as st
import pandas as pd
def show():
    # Streamlit界面
    st.title("线路参数导入数据处理工具")

    col1, col2 = st.columns([1, 1])
    with col1:
        old_file = st.file_uploader("上传报送数据表", type=["xlsm"])

    with col2:
        new_file = st.file_uploader("上传新模板表", type=["xlsx"])

    if old_file is not None and new_file is not None:
        # 读取 Excel 文件
        sheet_name1 = '设备线路参数调研'  # 替换为第一个Excel表的Sheet名称
        df1 = pd.read_excel(old_file, sheet_name=sheet_name1)

        # 筛选包含“高压”两个字的行
        filtered_df = df1[df1.apply(lambda row: row.astype(str).str.contains('线路').any(), axis=1)]

        new_df = pd.read_excel(new_file)

        col1, col2 = st.columns([1, 1])
        with col1:
            # 显示旧表和新表
            st.write("报送数据表筛选后的数据：")
            st.write(filtered_df)
        with col2:
            st.write("新模板表：")
            st.write(new_df)

        # 让用户选择要复制的列
        col1, col2 = st.columns([1, 1])
        with col1:
            # 默认选中一些列名
            default_old_columns = ["所属区域","设备/线路名称", "电压等级","电流/容量限值（A/MVA）"]  # 这里替换为你希望默认选中的列名
            old_columns = st.multiselect("选择原始数据表中的列", filtered_df.columns, default=default_old_columns)
        with col2:
            # 默认选中一些列名
            default_new_columns = ["所属区域", "线路名称", "电压等级","电流/容量限值（A/MVA)"]  # 这里替换为你希望默认选中的列名
            new_columns = st.multiselect("选择新模板表中的列", new_df.columns, default=default_new_columns)

        # 添加“开始复制”按钮
        if old_columns and new_columns:
            if len(old_columns) == len(new_columns):

                if st.button("开始数据处理"):

                    # 将旧表的选定列数据复制到新表的选定列
                    for old_col, new_col in zip(old_columns, new_columns):
                        new_df[new_col] = filtered_df[old_col].copy()

                    column_name = '电压等级'

                    # 定义一个函数来检查并添加“kV”
                    def add_kV(value):
                        # 将值转换为字符串
                        value_str = str(value)
                        if value_str.endswith('kV'):
                            return value_str
                        else:
                            return value_str + 'kV'

                    # 应用函数到指定列
                    new_df[column_name] = new_df[column_name].apply(add_kV)

                    # 假设你要处理的是 '所属区域' 这一列
                    column_name = '所属区域'

                    # 定义要替换的特定值和新值的字典
                    replacement_dict = {
                        '邓庄': '昌平',
                        '回龙观': '昌平',
                        '霍南': '昌平',
                        '吉利': '昌平',
                        '军都': '昌平',
                        '七家庄': '昌平',
                        '未来城': '昌平',
                        '西沙屯': '昌平',
                        '下庄': '昌平',
                        '信息港': '昌平',
                        '于辛庄': '昌平',
                        '奥运村': '朝阳',
                        '定福庄': '朝阳',
                        '东坝东': '朝阳',
                        '东北郊': '朝阳',
                        '垡头': '朝阳',
                        '富力城': '朝阳',
                        '高碑店': '朝阳',
                        '红军营': '朝阳',
                        '酒仙桥': '朝阳',
                        '老君堂': '朝阳',
                        '孙河': '朝阳',
                        '太阳宫': '朝阳',
                        '团结湖': '朝阳',
                        '王四营': '朝阳',
                        '望京': '朝阳',
                        '西大望': '朝阳',
                        '菜市口站': '城区',
                        '草桥站': '城区',
                        '广安门站': '城区',
                        '牛街站': '城区',
                        '东管头站': '城区',
                        '开阳里站': '城区',
                        '右安门站': '城区',
                        '六里桥站': '城区',
                        '北城': '城区',
                        '什刹海站': '城区',
                        '龙潭湖站': '城区',
                        '新街口站': '城区',
                        '东管头': '城区',
                        '沙窝站': '城区',
                        '什刹海': '城区',
                        '新街口': '城区',
                        '人定湖站': '城区',
                        '阜成门站': '城区',
                        '动物园站': '城区',
                        '复兴门站': '城区',
                        '朝阳门': '城区',
                        '天坛站': '城区',
                        '崇文门站': '城区',
                        '万明路站': '城区',
                        '前门站': '城区',
                        '北城站': '城区',
                        '地安门': '城区',
                        '龙潭湖': '城区',
                        '桃园': '城区',
                        '王府井': '城区',
                        '西直门站': '城区',
                        '长椿街': '城区',
                        '宝善庄': '大兴',
                        '陈留庄': '大兴',
                        '大兴': '大兴',
                        '礼贤北': '大兴',
                        '罗奇营': '大兴',
                        '青云店': '大兴',
                        '团河': '大兴',
                        '榆垡北': '大兴',
                        '广阳': '房山',
                        '韩村河': '房山',
                        '芦城': '房山',
                        '阎村北': '房山',
                        '榆管营': '房山',
                        '长安': '房山',
                        '北宫': '丰台',
                        '翠林': '丰台',
                        '吕村': '丰台',
                        '南苑': '丰台',
                        '玉泉营': '丰台',
                        '张仪': '丰台',
                        '左安门': '丰台',
                        '北铁营': '丰台',
                        '宋家庄': '丰台',

                        '八里庄': '海淀',
                        '宝山': '海淀',
                        '东升': '海淀',
                        '昆玉河': '海淀',
                        '清河': '海淀',
                        '上庄': '海淀',
                        '温泉': '海淀',
                        '西北旺': '海淀',
                        '玉渊潭': '海淀',
                        '远大': '海淀',
                        '知春里': '海淀',
                        '怀柔': '怀柔',
                        '栗元': '门头沟',
                        '聂各庄': '门头沟',
                        '密云': '密云',
                        '塘峪': '密云',
                        '平谷': '平谷',
                        '鱼子山': '平谷',
                        '冬奥': '石景山',
                        '新首钢': '石景山',
                        '永定': '石景山',
                        '东府': '顺义',
                        '高丽营': '顺义',
                        '李遂': '顺义',
                        '马坡': '顺义',
                        '仁和': '顺义',
                        '西马': '顺义',
                        '北寺': '通州',
                        '草厂': '通州',
                        '柴务': '通州',
                        '副中心': '通州',
                        '梁各庄': '通州',
                        '商务园': '通州',
                        '台湖': '通州',
                        '通州': '通州',
                        '堰上': '通州',
                        '运河': '通州',
                        '荣华': '亦庄',
                        '路南': '亦庄',
                        '康宁': '亦庄',
                        '经海': '亦庄',

                    }

                    # 替换特定值
                    new_df[column_name] = new_df[column_name].replace(replacement_dict)

                    output_file = new_file.name
                    # 检查 output_file 是否存在，如果不存在则复制 new_file 到 output_file
                    if not os.path.exists(output_file):
                        with open(output_file, "wb") as f:
                            f.write(new_file.getbuffer())
                    # 使用 ExcelWriter 追加数据
                    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                        # 手动计算 startrow，确保从最后一个非空行的下一行开始写入
                        startrow = writer.sheets['Sheet1'].max_row if writer.sheets['Sheet1'].max_row > 0 else 0
                        new_df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=startrow, header=False)

                    st.success(f"更新后的新表已保存到 {output_file}")
                    df3 = pd.read_excel(output_file, engine='openpyxl')
                    # 显示最终的 DataFrame
                    st.write("处理完成的文件内容：")
                    st.dataframe(df3)
                    with open(output_file, "rb") as f:
                        btn = st.download_button(
                            label="下载更新后的新表",
                            data=f,
                            file_name=output_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

            else:
                st.error("原始数据表和新模板表选择的列数必须相同。")
        else:
            st.error("请选择要处理的数据对应的列。")

