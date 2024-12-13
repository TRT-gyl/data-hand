import streamlit as st
from streamlit_option_menu import option_menu
import pagesss.母线数据处理 as page1
import pagesss.变电站参数导入 as page2
import pagesss.变压器设备参数导入 as page3
import pagesss.线路参数导入 as page4
import pagesss.变压器参数导入 as page5
import pagesss.运行方式导入 as page6
import pagesss.运行数据 as page7
import pagesss.分布式电站 as page8
from datetime import datetime, timedelta
 
 
st.set_page_config(page_title="Data Hand", page_icon="dolphin", layout="wide")

with st.sidebar:
    selected = option_menu("数据处理", ["主页", 'Settings', '承载力老模板', '承载力新模板',"分布式台账处理"],
                           icons=['house', 'gear'], menu_icon="cast", default_index=0)

if selected == '主页':
    st.write("# 台账数据处理!")
    

    # 初始化会话状态
    if 'data' not in st.session_state:
        st.session_state.data = []

    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = datetime.now()

    # 检查是否超过一天
    if datetime.now() - st.session_state.last_update_time > timedelta(days=1):
        st.session_state.data = []  # 清空数据
        st.session_state.last_update_time = datetime.now()  # 重置时间戳

    # 用户操作
    if st.button("Add Data"):
        st.session_state.data.append("New Data")
        st.session_state.last_update_time = datetime.now()  # 更新时间戳

    # 显示当前数据
    st.write("Current Data:", st.session_state.data)
elif selected == 'Settings':
    st.success('test')
elif selected == '承载力老模板':
    sub_menu_items = ["母线数据处理", "变电站参数处理", "变压器设备参数",'线路参数','变压器参数','运行方式','运行方式数据转置']
    selected_sub_menu = st.sidebar.selectbox("选择处理文档种类", sub_menu_items)
    if selected_sub_menu == '母线数据处理':
        page1.show()
    elif selected_sub_menu == '变电站参数处理':
        page2.show()
    elif selected_sub_menu == '变压器设备参数':
        page3.show()
    elif selected_sub_menu == '线路参数':
        page4.show()
    elif selected_sub_menu == '变压器参数':
        page5.show()
    elif selected_sub_menu == '运行方式':
        page6.show()
    elif selected_sub_menu == '运行方式数据转置':
        page7.show()
elif selected == '承载力新模板':
    st.write("# 承载力新模板台账数据处理!")
elif selected == '分布式台账处理':
    sub_menu_items = ["分布式电站", "区域模板处理"]
    selected_sub_menu = st.sidebar.selectbox("选择处理文档种类", sub_menu_items)
    if selected_sub_menu == '分布式电站':
        page8.main()
    elif selected_sub_menu == '区域模板处理':
        page2.show()

