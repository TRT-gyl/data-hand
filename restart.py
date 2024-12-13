import os
import time

def restart():
    # 停止 Streamlit 服务
    os.system("pkill -f 'streamlit run'")
    time.sleep(2)  # 等待服务停止
    # 重新启动 Streamlit 服务
    os.system("streamlit run streamlit_app.py &")

if __name__ == "__main__":
    restart()