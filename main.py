import yaml
from modules.TextExtractor import extract_text_from_pdf
from modules.GPTSummarizer import summarize_with_gpt
from modules.PPTBuilder import create_summary_from_template

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    pdf_path = config["input"]["pdf_path"]
    template_path = config["slides"]["template_path"]
    style_option = config["slides"]["style"]
    output_path = config["slides"]["output_path"]

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Summarize with GPT
    summary = summarize_with_gpt(
        text,
        model=config["openai"]["model"],
        temperature=config["openai"]["temperature"],
        api_key_env=config["openai"]["api_key_env"]
    )

    # Step 3: Create presentation
    create_summary_from_template(summary, template_path, style_option, output_path)

if __name__ == "__main__":
    main()