#!/usr/bin/env python3
"""
Script to convert multiple-choice HTML quiz files to fill-in-the-blank format.
This script identifies numerical answer options and replaces them with input fields.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Files that should keep multiple-choice format (conceptual questions)
KEEP_MULTIPLE_CHOICE = [
    '变量分类与测量水平.html',
    't检验与方差分析检验选择.html',
    '离散变量与连续变量.html',
    '无需计算的标准差比较.html',
    '无需计算的均值比较.html',
    '确定原假设与备择假设.html',
    '总体均值推断的分布选择.html',
    '第一类错误与第二类错误.html',
]

# Files that already have input fields (may need minor fixes)
ALREADY_INPUT_FILES = [
    '均值中位数众数计算.html',
    '总体均值的置信区间-t分布的应用.html',
    '选择合适样本量.html',
    '总体均值差异的置信区间标准正态分布应用.html',
    '基于直方图的数据集均值近似.html',
    '解读相对频率直方图.html',
    '卡方独立性检验.html',
    '切比雪夫定理与经验法则.html',
    '总体均值置信区间标准正态分布应用.html',
    '总体均值差异的置信区间t分布应用.html',
    '列联表期望频数.html',
    '解读双条形图.html',
    '方差分析均方与总体方差2.html',
    '第一类错误与第二类错误及统计功效.html',
    '相关系数与最小二乘回归线斜率的假设检验2.html',
    '简单线性回归的置信区间与预测区间.html',
    '离散概率分布基础.html',
    '总体方差比置信区间.html',
    '总体均值假设检验-t检验.html',
]

# CSS for input field
INPUT_CSS = '''
        .answer-input-container {
            margin: 25px 0;
            text-align: center;
        }
        .answer-label {
            display: block;
            font-size: 1.1rem;
            color: #0052cc;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .answer-input {
            width: 200px;
            padding: 15px 20px;
            font-size: 1.3rem;
            border: 3px solid #cce0ff;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
            outline: none;
        }
        .answer-input:focus {
            border-color: #0052cc;
            box-shadow: 0 0 0 4px rgba(0, 82, 204, 0.1);
        }
        .answer-input.correct {
            border-color: #00cc66;
            background-color: #e6ffe6;
        }
        .answer-input.incorrect {
            border-color: #ff6666;
            background-color: #ffe6e6;
        }
'''

def is_numerical_option(text):
    """Check if option text is a numerical value."""
    text = text.strip()
    # Match numbers like: 6.43, -2.789, 0.7977, 92378, 1/2, etc.
    patterns = [
        r'^-?\d+\.?\d*$',  # Simple numbers
        r'^-?\d+,\s*-?\d+$',  # Comma-separated numbers like "-1.645, 1.645"
    ]
    for pattern in patterns:
        if re.match(pattern, text):
            return True
    return False

def has_numerical_options(soup):
    """Check if the HTML has numerical multiple-choice options."""
    options = soup.find_all(['div'], class_=re.compile(r'option|answer-option'))
    numerical_count = 0
    total_count = 0

    for option in options:
        text_elem = option.find(['div'], class_=re.compile(r'option-text|option-content'))
        if text_elem:
            text = text_elem.get_text(strip=True)
            if text:
                total_count += 1
                if is_numerical_option(text):
                    numerical_count += 1

    # If most options are numerical, return True
    return total_count > 0 and numerical_count >= total_count * 0.75

def extract_correct_answer(soup, content):
    """Try to extract the correct answer from the HTML/JS."""
    # Look for correctAnswer in JavaScript
    match = re.search(r"const\s+correctAnswer\s*=\s*['\"]([^'\"]+)['\"]", content)
    if match:
        return match.group(1)

    match = re.search(r"correctAnswer\s*=\s*['\"]([^'\"]+)['\"]", content)
    if match:
        return match.group(1)

    # Look for data-correct="true"
    correct_option = soup.find(attrs={'data-correct': 'true'})
    if correct_option:
        text_elem = correct_option.find(['div'], class_=re.compile(r'option-text|option-content'))
        if text_elem:
            return text_elem.get_text(strip=True)

    return None

def convert_file(filepath):
    """Convert a single HTML file to fill-in-the-blank format."""
    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Check if this file should be skipped
    if filepath.name in KEEP_MULTIPLE_CHOICE:
        print(f"  Skipping (conceptual): {filepath.name}")
        return False

    if filepath.name in ALREADY_INPUT_FILES:
        print(f"  Skipping (already has input): {filepath.name}")
        return False

    # Check if file has numerical options
    if not has_numerical_options(soup):
        print(f"  Skipping (no numerical options): {filepath.name}")
        return False

    print(f"  Converting: {filepath.name}")
    return True

def main():
    html_dir = Path(__file__).parent
    html_files = list(html_dir.glob('*.html'))

    converted = 0
    skipped = 0

    for filepath in html_files:
        if filepath.name == 'convert_to_fill_blank.py':
            continue
        if convert_file(filepath):
            converted += 1
        else:
            skipped += 1

    print(f"\nSummary: {converted} files to convert, {skipped} files skipped")

if __name__ == '__main__':
    main()
