import streamlit as st
import pandas as pd
def show():
    # Streamlit界面
    st.title("变电站参数导入数据处理工具")
    col1, col2 = st.columns([1, 1])
    with col1:
        # 上传第一个Excel文件
        uploaded_file1 = st.file_uploader("上传报送数据文件", type=["xlsm"])
        if uploaded_file1 is not None:
            sheet_name1 = '设备线路参数调研'  # 替换为第一个Excel表的Sheet名称
            df1 = pd.read_excel(uploaded_file1, sheet_name=sheet_name1)

            # 筛选包含“高压”两个字的行
            filtered_df = df1[df1.apply(lambda row: row.astype(str).str.contains('高压').any(), axis=1)]
            st.write("筛选后的数据：")
            st.write(filtered_df)
    with col2:
        # 上传第二个Excel文件
        uploaded_file2 = st.file_uploader("上传导入模板文件", type=["xlsx"])
        if uploaded_file2 is not None:
            df2 = pd.read_excel(uploaded_file2)

            # 手动映射列名
            column_mapping = {
                '所属区域': '所属区域',
                '设备/线路名称': '变电站名称',
                '电压等级': '电压等级',
                # 添加更多的列名映射
            }

            # 将筛选出的行插入到第二个Excel表中
            # 创建一个新的DataFrame来存储映射后的数据
            mapped_df = pd.DataFrame()

            for col_in_df1, col_in_df2 in column_mapping.items():
                if col_in_df1 in filtered_df.columns:
                    mapped_df[col_in_df2] = filtered_df[col_in_df1]

            # 追加数据到第二个Excel表
            df2 = pd.concat([df2, mapped_df], ignore_index=True)

            # 保存第二个Excel表
            output_file = '变电站参数导入模板.xlsx'  # 替换为输出Excel文件的路径
            # 将填充后的数据追加到第二个文件中
            with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df2.to_excel(writer, index=False, startrow=writer.sheets['Sheet1'].max_row, header=False)

            st.write("数据已成功写回到原始文件中。")
    st.divider()
    st.subheader("请先上传所有数据文件后进行数据模板统一")
    button = st.button("数据模板统一",key="button")
    if button:
        # 读取 Excel 文件
        file_path = '变电站参数导入模板.xlsx'
        df = pd.read_excel(file_path)

        # 假设你要处理的列是 'Column_Name'
        column_name = '变电站名称'  # 替换为你要处理的列名

        # 使用 str.replace() 方法删除句子中的“高压侧”
        df[column_name] = df[column_name].str.replace('高压侧', '')

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
        df[column_name] = df[column_name].apply(add_kV)

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
        df[column_name] = df[column_name].replace(replacement_dict)

        output_file_path = '变电站参数导入模板.xlsx'
        df.to_excel(output_file_path, index=False)

        # 读取第二个 Excel 文件
        file_path = '变电站参数导入模板.xlsx'
        df3 = pd.read_excel(file_path)
        # 显示最终的 DataFrame
        st.write("运行方式参数导入模板文件内容：")
        st.write(df3)
        st.success("数据格式统一完成")
