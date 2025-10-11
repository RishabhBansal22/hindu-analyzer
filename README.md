# The Hindu Editorial Analyzer

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent tool that scrapes editorial articles from The Hindu newspaper and provides comprehensive analysis using Google's Gemini AI. Designed specifically for CAT VARC (Verbal Ability and Reading Comprehension) exam preparation.

## 🎯 Purpose

This project helps CAT aspirants improve their reading comprehension skills by automatically analyzing newspaper editorials and providing structured insights including central ideas, tone analysis, vocabulary building, and critical thinking questions.

## ✨ Features

- **Automated Scraping**: Extracts editorial articles from The Hindu's opinion section
- **AI-Powered Analysis**: Uses Google Gemini to provide detailed article analysis
- **CAT VARC Focused**: Structured output designed for exam preparation
- **Multiple Articles**: Process multiple editorials in a single run
- **Clean Content Extraction**: Filters out metadata and related content for focused analysis

## 📋 Analysis Components

For each article, the tool provides:

1. **Central Idea** (2-3 lines): Main argument summary
2. **Tone Analysis**: Author's tone (critical, analytical, persuasive, etc.)
3. **Paragraph-wise Summary**: Breakdown of each paragraph
4. **Vocabulary Builder**: 5-7 advanced words with meanings and examples
5. **Critical Thinking Questions**: 2-3 inference and comprehension questions
6. **Reading Skill Tips**: Advice for improving reading techniques

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/RishabhBansal22/hindu-analyzer.git
cd hindu-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### Usage

Run the analyzer with default settings (1 article):
```bash
python main.py
```

To analyze multiple articles, modify the `main()` function call in `main.py`:
```python
output = main(num_articles=3)  # Analyze 3 articles
```

## 📁 Project Structure

```
thehindu_exct/
├── main.py                 # Main execution script
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── scripts/
│   ├── scrapper.py        # Web scraping functionality
│   └── gemini.py          # Gemini AI integration
└── utils/
    └── prompt.py          # System prompts for AI analysis
```

## 🔧 Configuration

### Scraper Settings

The scraper targets The Hindu's editorial section by default:
- URL: `https://www.thehindu.com/opinion/editorial/`
- Respects server load with 0.5-second delays between requests
- Filters out metadata and related content for clean extraction

### AI Analysis

The Gemini AI is configured with:
- Model: `gemini-2.5-flash`
- Structured JSON output using Pydantic models
- CAT VARC-focused system prompts

## 📊 Output Format

The analysis is returned as structured JSON containing:

```json
{
  "Central_Idea": "Summary of main argument",
  "Tone_of_author": "analytical/critical/persuasive etc.",
  "Paragraph_wise_summary": ["Para 1 summary", "Para 2 summary"],
  "Vocabulary_builder": ["word1: meaning", "word2: meaning"],
  "critical_thinking": "Inference questions",
  "takeaway": "Reading skill tip"
}
```

## 🛠️ Dependencies

- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing and content extraction
- `google-genai`: Google Gemini AI integration
- `python-dotenv`: Environment variable management
- `pydantic`: Data validation and serialization

## 🔮 Future Enhancements

- [ ] Support for multiple newspaper sources
- [ ] PDF export functionality
- [ ] Progress tracking for CAT preparation
- [ ] Custom prompt templates
- [ ] Batch processing with scheduling
- [ ] Web interface for easier use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for educational purposes. Please respect The Hindu's terms of service and use responsibly. The scraped content is analyzed for educational enhancement and should not be redistributed without proper attribution.

## 🙏 Acknowledgments

- The Hindu for quality editorial content
- Google Gemini for AI analysis capabilities
- CAT preparation community for inspiration

---

**Happy Reading and CAT Preparation! 🎯**