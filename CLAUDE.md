# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **PDF Quiz Translator** project that converts English statistics quiz PDFs into interactive Chinese HTML quiz pages. The project uses:
- **PyMuPDF** for PDF text extraction
- **DeepSeek Chat API** for translation and HTML generation

## Project Structure

```
quiz-questions/
├── main.py              # Main script - PDF processing pipeline
├── requirements.txt     # Python dependencies
├── topic_files/         # Source PDF files (100+ English statistics quizzes)
├── htmls/               # Generated interactive HTML quiz pages (Chinese)
└── .venv/               # Python virtual environment
```

## Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Run the PDF translator
```bash
python main.py
```

The script will:
1. Display all PDF files found in `topic_files/`
2. Prompt for file range to process (or press Enter for all)
3. Process each PDF: extract text -> translate -> generate HTML
4. Save output to `htmls/`

## Architecture

### Processing Pipeline (main.py)

1. **`extract_text_from_pdf()`** - Uses PyMuPDF (fitz) to extract text from each PDF page
2. **`translate_filename()`** - Calls DeepSeek API to translate English filenames to Chinese
3. **`translate_pdf_content()`** - Translates PDF content to Chinese while preserving math formulas (x̄, σ, μ, α, β, χ², H₀, H₁)
4. **`generate_html_quiz()`** - Generates interactive HTML with:
   - Multiple choice options with visual feedback
   - Submit/Reset buttons
   - Score tracking
   - Hidden answer explanations (revealed on button click)
5. **`clean_html_code()`** - Removes markdown code block markers from API response
6. **`sanitize_chinese_filename()`** - Sanitizes Chinese filenames for valid filesystem paths

### Generated HTML Structure

Each HTML file is self-contained with:
- Embedded CSS (responsive design, blue color theme)
- Embedded JavaScript (answer selection, score tracking, show/hide explanations)
- Chinese quiz content with mathematical notation preserved
- Topics include: probability, hypothesis testing, ANOVA, regression, chi-square, etc.

## Configuration (main.py)

- `API_KEY` - DeepSeek API key (configure before running)
- `DEEPSEEK_API_URL` - API endpoint (default: https://api.deepseek.com)
- `DEEPSEEK_CHAT_MODEL` - Model to use (default: deepseek-chat)
- `PDF_FOLDER` - Input folder name (default: topic_files)
- `API_DELAY` - Delay between API calls in seconds (default: 5)

## Statistics Topics Covered

The `topic_files/` directory contains 100+ PDFs covering:
- Descriptive statistics (mean, median, mode, standard deviation)
- Probability distributions (normal, binomial, chi-square, t, F)
- Hypothesis testing (Z-test, t-test, chi-square test)
- Confidence intervals
- ANOVA (one-way, two-way, repeated measures)
- Regression analysis
- Contingency tables and independence tests
- Bayes' theorem and conditional probability

## HTML Testing & Quality Assurance

### Testing Checklist

When testing HTML quiz files, check for the following issues:

#### Fill-in-the-Blank Files (Input Fields)
- [ ] Input field exists and is visible
- [ ] Input field has correct placeholder (if any)
- [ ] Tolerance value is appropriate (0.01 or 0.001)
- [ ] Correct answer validation works
- [ ] Feedback shows on correct/incorrect answers
- [ ] Correct answer is displayed when wrong
- [ ] CSS styling for correct/incorrect states works
- [ ] JavaScript handles edge cases (empty input, non-numbers)

#### Multiple-Choice Files
- [ ] All options are clickable
- [ ] Selected option is highlighted
- [ ] Only one option can be selected
- [ ] Correct answer validation works
- [ ] Feedback shows on selection
- [ ] Score tracking works

#### General Issues
- [ ] No JavaScript console errors
- [ ] No CSS styling conflicts
- [ ] Responsive design works
- [ ] Chinese characters display correctly
- [ ] Math symbols display correctly (x̄, σ, μ, α, β, χ², H₀, H₁)
- [ ] Submit/Reset buttons work
- [ ] Show explanation button works

### File Categories

Based on analysis, files are categorized as:

| Category | Count | Description |
|----------|-------|-------------|
| NUMERICAL | 8 | Pure numerical calculation questions |
| HAS_INPUT | 21 | Already have input fields (may need tolerance fix) |
| CONCEPTUAL | 27 | Conceptual questions (keep as multiple-choice) |
| OTHER | 52+ | Mixed or need analysis |

### Testing Log

#### 2026-02-26 Testing Session

**Testing approach**: Parallel agents testing different file categories

### Issues Found and Fixed

#### 1. Tolerance Comparison Bug (`<` vs `<=`)
**Files affected:**
- 均值中位数众数计算.html
- 基于直方图的数据集均值近似.html
- 解读相对频率直方图.html

**Issue:** Tolerance comparison used strict inequality (`<`) instead of `<=`, meaning answers exactly at tolerance boundary would be marked wrong.

**Fix:** Changed all instances of `Math.abs(...) < tolerance` to `Math.abs(...) <= tolerance`

#### 2. Mixed Input/Multiple-Choice Implementation
**File affected:** 百分位数.html

**Issue:** Questions 1-3 had input fields in HTML but no JavaScript validation handlers. The code only handled multiple-choice options.

**Fix:** Converted questions 1-3 back to multiple-choice format for consistent UI/UX. Also removed 4 duplicate JavaScript code blocks.

#### 3. Variable Declaration Order
**File affected:** 正态分布求基本概率.html

**Issue:** Variable `currentParams` was declared globally and then redeclared inside DOMContentLoaded, causing potential confusion.

**Fix:** Removed global declaration, kept variables inside DOMContentLoaded scope.

### Files Tested (Summary)

| Category | Files Tested | Issues Found | Status |
|----------|--------------|--------------|--------|
| NUMERICAL | 8 | 1 (百分位数.html) | Fixed |
| HAS_INPUT | 8 | 3 (tolerance bugs) | Fixed |
| CONCEPTUAL | 8 | 4 (refresh handlers + error msg + HTML) | Fixed |
| OTHER | 8 | 1 (variable scope) | Fixed |

| **Total** | **32** | **9 issues** | **All Fixed** |

### All Issues Resolved

All identified issues have been fixed. No outstanding issues remain.
