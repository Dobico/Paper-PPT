import streamlit as st
from modules.TextExtractor import extract_text_from_pdf
from modules.GPTSummarizer import summarize_with_gpt
from modules.PPTBuilder import create_summary_from_template
import datetime
import csv
import os

st.set_page_config(page_title="Paper2Slides", layout="centered")
st.title("📄 Paper2Slides")
st.markdown("논문 PDF를 업로드하면 GPT가 요약하고 슬라이드를 자동 생성해드립니다.")

pdf_file = st.file_uploader("1. 논문 PDF 업로드", type=["pdf"])
template_file = st.file_uploader("2. (선택) 템플릿 PPTX 업로드", type=["pptx"])
style_option = st.selectbox("3. 슬라이드 스타일 선택", ["default", "title_only", "section_header", "blank"])
summary_mode = st.radio("4. 요약 방식 선택", ["전체 요약", "목적과 결과 중심", "한 문단 요약"], index=0)

if "summary" not in st.session_state:
    st.session_state.summary = None
if "ppt_generated" not in st.session_state:
    st.session_state.ppt_generated = False
if "feedback_logged" not in st.session_state:
    st.session_state.feedback_logged = False

# 요약
if st.button("5. GPT로 요약하기"):
    if not pdf_file:
        st.warning("⚠️ PDF 파일을 업로드해주세요.")
    else:
        with st.spinner("📄 텍스트 추출 중..."):
            pdf_bytes = pdf_file.read()
            with open("temp_uploaded.pdf", "wb") as f:
                f.write(pdf_bytes)
            text = extract_text_from_pdf("temp_uploaded.pdf")

        if summary_mode == "전체 요약":
            prompt = f"""
다음 논문을 아래 항목별로 1~2문장씩 요약해줘:

1. 연구 목적
2. 사용된 방법
3. 주요 결과
4. 결론

논문 본문:
{text[:3500]}
"""
        elif summary_mode == "목적과 결과 중심":
            prompt = f"""
다음 논문에서 연구의 목적과 주요 결과를 각각 2문장 이내로 요약해줘.

논문 본문:
{text[:3500]}
"""
        else:
            prompt = f"""
다음 논문 내용을 전체적으로 한 문단(5문장 이내)으로 요약해줘.

논문 본문:
{text[:3500]}
"""

        try:
            with st.spinner("🤖 GPT가 요약 중입니다..."):
                summary = summarize_with_gpt(text, prompt=prompt)
                st.session_state.summary = summary
                st.session_state.ppt_generated = False
        except Exception as e:
            st.error("❌ 요약 중 문제가 발생했습니다.")
            print("DEBUG:", e)

# 요약 결과
if st.session_state.summary:
    st.subheader("📋 GPT 요약 결과")
    st.text_area("요약 내용", st.session_state.summary, height=300)

    if st.button("6. 슬라이드 생성"):
        try:
            with st.spinner("🎞 슬라이드 생성 중..."):
                pptx_path = "generated_slides.pptx"
                template_path = None
                if template_file:
                    template_bytes = template_file.read()
                    with open("temp_template.pptx", "wb") as f:
                        f.write(template_bytes)
                    template_path = "temp_template.pptx"

                create_summary_from_template(st.session_state.summary, template_path, style_option, pptx_path)
                st.session_state.ppt_generated = True
            st.success("✅ 슬라이드 생성 완료! 아래에서 다운로드하세요.")
        except Exception as e:
            st.error("❌ 슬라이드 생성 중 문제가 발생했습니다.")
            print("DEBUG:", e)

# 다운로드 및 피드백
if st.session_state.ppt_generated:
    st.markdown("### 📊 생성된 슬라이드에 대한 만족도를 알려주세요:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 만족해요"):
            feedback = "positive"
    with col2:
        if st.button("👎 아쉬워요"):
            feedback = "negative"

    if "feedback" in locals() and not st.session_state.feedback_logged:
        os.makedirs("feedback_logs", exist_ok=True)
        with open("feedback_logs/slide_feedback.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().isoformat(),
                summary_mode,
                style_option,
                feedback
            ])
        st.session_state.feedback_logged = True
        st.success("피드백 감사합니다!")

    with open("generated_slides.pptx", "rb") as f:
        pptx_data = f.read()

    st.download_button(
        label="📥 슬라이드 다운로드",
        data=pptx_data,
        file_name="summary_slides.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )