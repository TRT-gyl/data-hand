import os

import streamlit as st
import pandas as pd

# 设置页面布局为 wide 模式
st.set_page_config(layout="wide")

# 定义 Streamlit 应用程序
def main():
    st.title("分布式电站台账数据处理")

    # 检查是否需要重置会话状态
    if 'reset' not in st.session_state:
        st.session_state.reset = False

    # 重置按钮
    if st.button("重置会话状态"):
        st.session_state.reset = True

    # 如果需要重置，清除所有会话状态
    if st.session_state.reset:
        for key in list(st.session_state.keys()):
            if key != 'reset':  # 保留 reset 标志
                del st.session_state[key]
        st.session_state.reset = False
        st.write("会话状态已重置")

    # 上传旧表和新表
    st.write("请上传原始数据表和新模板表：")
    col1, col2 = st.columns([1, 1])
    with col1:
        old_file = st.file_uploader("上传原始数据表", type=["xlsx", "xls"])

    with col2:
        new_file = st.file_uploader("上传新模板表", type=["xlsx", "xls"])

    if old_file is not None and new_file is not None:
        # 读取 Excel 文件
        old_df = pd.read_excel(old_file)
        new_df = pd.read_excel(new_file)

        col1, col2 = st.columns([1, 1])
        with col1:
            # 显示旧表和新表
            st.write("原始数据表：")
            st.write(old_df)
        with col2:
            st.write("新模板表：")
            st.write(new_df)

        # 让用户选择要复制的列
        col1, col2 = st.columns([1, 1])
        with col1:
            # 默认选中一些列名
            default_old_columns = ["电压等级", "发电户号"]  # 这里替换为你希望默认选中的列名
            old_columns = st.multiselect("选择原始数据表中的列", old_df.columns, default=default_old_columns)
        with col2:
            # 默认选中一些列名
            default_new_columns = ["电压等级", "户号"]  # 这里替换为你希望默认选中的列名
            new_columns = st.multiselect("选择新模板表中的列", new_df.columns, default=default_new_columns)

        # 添加“开始复制”按钮
        if old_columns and new_columns:
            if len(old_columns) == len(new_columns):
                # 用户输入填充的值
                fill_value = st.text_input("请输入要填充的分布式电站名称", "河南主站驻马店城区分布式光伏电站")

                if st.button("开始数据处理"):

                    # 将旧表的选定列数据复制到新表的选定列
                    for old_col, new_col in zip(old_columns, new_columns):
                        new_df[new_col] = old_df[old_col].copy()
                        # 假设你要处理的列名为 '电压等级'

                    column_name = '电压等级'
                    column_name1 = '公共连接点电压等级'
                    # 定义要替换的旧值和新值的映射字典
                    replacement_dict = {
                        '交流380V': '380V',
                        '交流220V': '220V',
                        '交流10kV': '10kV',
                        '交流35kV': '35kV',
                        'AC03802': '380V',
                        'AC02202': '220V',
                    }
                    replacement_dict1 = {
                        '交流380V': '380V',
                        '交流220V': '220V',
                        '交流6kV': '6kV',
                        '交流10kV': '10kV',
                        '交流20kV': '20kV',
                        '交流35kV': '35kV',
                        '交流66kV': '66kV'
                    }

                    # 替换特定值
                    new_df[column_name] = new_df[column_name].replace(replacement_dict)
                    new_df[column_name1] = new_df[column_name1].replace(replacement_dict1)

                    # 检查条件并修改数据
                    new_df.loc[(new_df['电压等级'].notnull()) & (
                        new_df['分布式电站名称'].isnull()), '分布式电站名称'] = fill_value

                    # 将更新后的新表写入新的 Excel 文件
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

if __name__ == "__main__":
    main()