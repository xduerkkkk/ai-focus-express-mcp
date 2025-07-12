import gradio as gr
from core_functions import get_ai_focus_express

# 更新下拉菜单的选项，与 core_functions.py 中的映射保持一致
time_options = ["过去24小时", "过去一周", "过去一月"]

demo = gr.Interface(
    fn=get_ai_focus_express,
    inputs=[
        gr.Textbox(label="关键词", placeholder="例如: Mixture of Experts, LLM Agent..."),
        gr.Dropdown(label="时间范围", choices=time_options, value="过去一周")
    ],
    outputs=gr.Markdown(label="情报报告", sanitize_html=False), # sanitize_html=False 允许渲染Markdown的全部格式
    title="AI焦点速递",
    description="输入AI领域的关键词，从顶尖信源获取最新动态。由MCP驱动。",
    allow_flagging="never" # 禁用Gradio的标记功能
)

if __name__ == "__main__":
    # 为了让其作为MCP被调用，启动时需要启用mcp_server
    demo.launch(mcp_server=True)