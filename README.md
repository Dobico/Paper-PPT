
# Paper2Slides

Paper2Slides는 논문 PDF 파일을 요약하고, 해당 내용을 PowerPoint 슬라이드로 자동 생성하는 Python 기반 툴입니다.

## 기능
- 📄 논문 PDF → 텍스트 자동 추출
- 🤖 GPT-3.5/4 API를 통한 요약
- 🎞 요약 결과 → 슬라이드(PPTX) 자동 생성
- 🎨 사용자 템플릿 `.pptx` 업로드 또는 스타일 선택 지원

## 실행 방법

```bash
pip install -r requirements.txt
python main.py
```

## 폴더 구조

```
Paper2Slides/
├── main.py
├── requirements.txt
├── README.md
└── modules/
    ├── TextExtractor.py
    ├── GPTSummarizer.py
    └── PPTBuilder.py
```

## 설정
`.env` 파일에 아래 내용을 추가해 주세요:

```
OPENAI_API_KEY=your_openai_api_key
```

## 라이선스
MIT
