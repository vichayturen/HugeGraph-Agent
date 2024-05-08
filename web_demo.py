import gradio as gr
from pyhugegraph.client import PyHugeClient
from stack.hugegraph_agent import HugeGraphAgent
from model.ollama import OllamaLLM


model = OllamaLLM("qwen:1.8b-chat-fp16", host="127.0.0.1", port=11434)
client = PyHugeClient(
    ip="127.0.0.1",
    port=18080,
    graph="hugegraph",
    user="admin",
    pwd="admin",
    timeout=10
)


with gr.Blocks() as demo:
    hugegraph_agent = gr.State(HugeGraphAgent(
        model=model.call,
        client=client
    ))
    gr.Markdown("# HugeGraph Agent\n")
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    with gr.Row():
        clear = gr.ClearButton([msg, chatbot])
        submit = gr.Button("Submit")
    def respond(message, chat_history):
        # response = hugegraph_agent.step(message)
        response = "hugegraph_agent.step(message)"
        chat_history.append((message, response))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
demo.launch()


# if __name__ == "__main__":
#     port = 7860
#     print(f"Experience demo on http://127.0.0.1:{port}")
#     demo().launch(server_name="0.0.0.0", server_port=port)
