# type: ignore
import gradio as gr

from goat.frontend.precision import Precision

from ..utils.database_helper import DatabaseHelper

TITLE = "Goat leaderboard"
INTRODUCTION_TEXT = "This is really nice introduction text!!!"
EVALUATION_QUEUE_TEXT = "there is evaluation queue"


db_helper = DatabaseHelper()

leaderboard_df = db_helper.get_leaderboard_df()


demo = gr.Blocks(css="src_display.css")
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
                    validate_big_tasks = gr.Checkbox(
                        label="Validate on big text tasks",
                        info="Do you need to validate your model on tasks that require large text answer?",
                    )
            submit_button = gr.Button("Submit Eval")
            submission_result = gr.Markdown()
            submit_button.click(
                db_helper.add_eval_request,
                [model_name, model_precision, validate_big_tasks],
                submission_result,
            )

demo.queue(default_concurrency_limit=40).launch()
