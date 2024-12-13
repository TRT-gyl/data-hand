import os
import time

def restart_streamlit():
    # 找到 Streamlit 进程的 PID
    streamlit_pid = os.popen("pgrep -f 'streamlit run'").read().strip()
    if streamlit_pid:
        # 终止 Streamlit 进程
        os.system(f"kill {streamlit_pid}")
        time.sleep(2)  # 等待服务停止
    # 重新启动 Streamlit 服务
    os.system("streamlit run your_app.py &")

if __name__ == "__main__":
    restart_streamlit()