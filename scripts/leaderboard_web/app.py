# type: ignore
import gradio as gr
from database_helper import DatabaseHelper
from src_display_css_html_js import custom_css
from utils import Precision

TITLE = "Goat leaderboard"
INTRODUCTION_TEXT = "This is really nice introduction text!!!"
EVALUATION_QUEUE_TEXT = "there is evaluation queue"

db_helper = DatabaseHelper()

leaderboard_df = db_helper.get_leaderboard_df()


demo = gr.Blocks(css=custom_css)
with demo:
    gr.HTML(TITLE)
    gr.Markdown(INTRODUCTION_TEXT, elem_classes="markdown-text")

    with gr.Tabs(elem_classes="tab-buttons") as tabs:
        with gr.TabItem("🏅 LLM Benchmark", elem_id="llm-benchmark-tab-table", id=1):
            leaderboard_table = gr.components.Dataframe(
                value=leaderboard_df,
                headers=["Model", "GOAT"],
                interactive=False,
            )
        with gr.TabItem("🚀 Submit ", elem_id="llm-benchmark-tab-table", id=5):
            with gr.Column():
                with gr.Row():
                    gr.Markdown(EVALUATION_QUEUE_TEXT, elem_classes="markdown-text")

            with gr.Row():
                gr.Markdown("# ✉️✨ Submit your model here!", elem_classes="markdown-text")

            with gr.Row():
                with gr.Column():
                    model_name = gr.Textbox(label="Model name on HF")
                    model_precision = gr.Dropdown(
                        choices=[i.value for i in Precision if i != Precision.Unknown],
                        label="Precision",
                        multiselect=False,
                        value="float16",
                        interactive=True,
                    )
                    num_fewshot = gr.Number(
                        label="Fewshot number",
                        minimum=0,
                        maximum=5,
                        step=1,
                        value=5,
                        interactive=True,
                    )

            submit_button = gr.Button("Submit Eval")
            submission_result = gr.Markdown()
            submit_button.click(
                db_helper.add_eval_request,
                [model_name, model_precision, num_fewshot],
                submission_result,
            )

demo.queue(default_concurrency_limit=40).launch()
