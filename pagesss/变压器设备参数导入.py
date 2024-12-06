import streamlit as st
import pandas as pd
def show():
    # Streamlit界面
    st.title("变压器设备参数导入数据处理工具")
    col1, col2 = st.columns([1, 1])
    with col1:
        # 上传第一个Excel文件
        uploaded_file1 = st.file_uploader("上传报送数据文件", type=["xlsm"])
        if uploaded_file1 is not None:
            sheet_name1 = '设备线路参数调研'  # 替换为第一个Excel表的Sheet名称
            df1 = pd.read_excel(uploaded_file1, sheet_name=sheet_name1)

            # 筛选包含“高压”两个字的行
            filtered_df = df1[df1.apply(lambda row: row.astype(str).str.contains('设备').any(), axis=1)]
            st.write("筛选后的数据：")
            st.write(filtered_df)
    with col2:
        # 上传第二个Excel文件
        uploaded_file2 = st.file_uploader("上传导入模板文件", type=["xlsx"])
        if uploaded_file2 is not None:
            df2 = pd.read_excel(uploaded_file2)

            # 手动映射列名
            column_mapping = {
                '设备/线路名称': '变压器绕组名称',
                '电压等级': '电压等级',
                '电流/容量限值（A/MVA）':'设备限值（MVA)'
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
            output_file = '变压器设备参数导入模板.xlsx'  # 替换为输出Excel文件的路径
            # 将填充后的数据追加到第二个文件中
            with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df2.to_excel(writer, index=False, startrow=writer.sheets['Sheet1'].max_row, header=False)

            st.write("数据已成功写回到原始文件中。")
    st.divider()
    st.subheader("请先上传所有数据文件后进行数据模板统一")
    button = st.button("数据模板统一",key="button")
    if button:
        # 读取 Excel 文件
        file_path = '变压器设备参数导入模板.xlsx'
        df = pd.read_excel(file_path)

        # 定义一个函数来删除后三个字符
        def remove_last_three_chars(text):
            if isinstance(text, str) and len(text) > 3:
                return text[:-3]
            return text

        # 应用函数到第二列，并将结果复制到第一列
        df['所属变压器'] = df['变压器绕组名称'].apply(remove_last_three_chars)
        # 提取第二列的最后三个字符并复制到第一列
        df['绕组类型'] = df['变压器绕组名称'].str[-3:]

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


        output_file_path = '变压器设备参数导入模板.xlsx'
        df.to_excel(output_file_path, index=False)
        st.write(df)
        st.success("数据格式统一完成")
