import streamlit as st
import pandas as pd


def show():

    # Streamlit界面
    st.title("运行方式参数导入数据处理工具")
    col1, col2 = st.columns([1, 1])
    with col1:
        # 上传第一个 Excel 文件
        file1 = st.file_uploader("上传报送数据文件", type=["xlsm"])

    with col2:
        # 上传第二个 Excel 文件
        file2 = st.file_uploader("上传运行方式模板参数导入文件", type=["xlsx"])

    if file1 is not None and file2 is not None:
        # 读取第一个 Excel 文件
        sheet_name1 = '拓扑数据'  # 替换为第一个Excel表的Sheet名称
        df1 = pd.read_excel(file1, sheet_name=sheet_name1)
        st.write("报送数据参数文件内容：")
        st.write(df1)

        # 读取第二个 Excel 文件
        df2 = pd.read_excel(file2)

        # 复制列内容上级节点
        df2['节点名称'] = df1['母线线路设备名称']
        df2['上级节点'] = df1['上级']

        # # 显示最终的 DataFrame
        # st.write("最终的运行方式导入模板文件内容：")
        # st.write(df2)

        # 保存修改后的文件
        output_file_path = file2.name

        # 使用 ExcelWriter 追加数据
        with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df2.to_excel(writer, sheet_name='Sheet1', index=False, startrow=writer.sheets['Sheet1'].max_row,header=False)

        st.success("完成数据导入")
        st.divider()
        # 读取第二个 Excel 文件
        file_path = '运行方式参数导入模板.xlsx'
        df3 = pd.read_excel(file_path)
        # 显示最终的 DataFrame
        st.write("运行方式参数导入模板文件内容：")
        st.write(df3)

