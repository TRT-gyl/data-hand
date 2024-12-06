import streamlit as st
import pandas as pd

def show():
    # Streamlit界面
    st.title("变压器参数导入数据处理工具")
    col1, col2 = st.columns([1, 1])
    with col1:
        # 上传第一个 Excel 文件
        file1 = st.file_uploader("上传变压器设备参数文件", type=["xlsx"])

    with col2:
        # 上传第二个 Excel 文件
        file2 = st.file_uploader("上传变压器参数导入文件", type=["xlsx"])

    if file1 is not None and file2 is not None:
        # 读取第一个 Excel 文件
        df1 = pd.read_excel(file1)
        st.write("变压器设备参数文件内容：")
        st.write(df1)

        # 读取第二个 Excel 文件
        df2 = pd.read_excel(file2)

        # 复制列内容
        df2['变压器名称'] = df1['变压器绕组名称']

        # 显示修改后的第二个 Excel 文件
        st.write("变压器参数异常值：")

        # 提取“主变”前面的字
        df2['所属变电站'] = df2['变压器名称'].str.extract(r'(.*?)主变')

        # 统计每个站点名称出现的次数
        site_counts = df2['所属变电站'].value_counts()


        # 创建一个新的列来存储标记
        df2['变压器类型'] = ''

        with st.container(height=100):
            # 遍历站点名称和对应的次数
            for site, count in site_counts.items():
                if count > 2:
                    df2.loc[df2['所属变电站'] == site, '变压器类型'] = '三绕组'
                elif count == 2:
                    df2.loc[df2['所属变电站'] == site, '变压器类型'] = '两绕组'
                else:
                    st.write(site)

            # 定义一个函数来删除后三个字符
        def remove_last_three_chars(text):
            if isinstance(text, str) and len(text) > 3:
                return text[:-3]
            return text

        df2['变压器名称'] = df2['变压器名称'].apply(remove_last_three_chars)

        # 显示最终的 DataFrame
        st.write("最终的变压器参数导入文件内容：")
        st.write(df2)

        # 保存修改后的文件
        output_file_path = file2.name
        df2.to_excel(output_file_path, index=False)
        st.success("完成数据导入")
