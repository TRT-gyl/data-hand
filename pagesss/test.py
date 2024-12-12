import streamlit as st
import pandas as pd
import tempfile
import os

# 设置页面布局为 wide 模式
st.set_page_config(layout="wide")

# 定义 Streamlit 应用程序
def main():
    st.title("台账数据工具")

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
        st.write("请选择要复制的列：")
        col1, col2 = st.columns([1, 1])
        with col1:
            old_columns = st.multiselect("选择原始数据表中的列", old_df.columns)
        with col2:
            new_columns = st.multiselect("选择新模板表中的列", new_df.columns)

        # 添加“开始复制”按钮
        if st.button("开始复制"):
            if old_columns and new_columns:
                if len(old_columns) == len(new_columns):
                    # 将旧表的选定列数据复制到新表的选定列
                    for old_col, new_col in zip(old_columns, new_columns):
                        new_df[new_col] = old_df[old_col].copy()

                    # 使用临时文件存储
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                        output_file = tmp_file.name

                    # 将更新后的新表写入临时文件
                    new_df.to_excel(output_file, index=False)

                    st.success(f"更新后的新表已保存到临时文件 {output_file}")

                    # 读取临时文件中的数据
                    df3 = pd.read_excel(output_file)

                    # 显示最终的 DataFrame
                    st.write("处理完成的文件内容：")
                    st.dataframe(df3)

                    # 提供下载按钮
                    with open(output_file, "rb") as f:
                        btn = st.download_button(
                            label="下载更新后的新表",
                            data=f,
                            file_name="updated_new_table.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    # 删除临时文件
                    os.remove(output_file)
                else:
                    st.error("旧表和新表选择的列数必须相同。")
            else:
                st.error("请选择要复制的列。")

if __name__ == "__main__":
    main()