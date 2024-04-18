import re
import streamlit as st
from jiwer import wer, cer

# 设置Streamlit页面
st.title('字符准确率与句子准确率统计工具')

# 使用columns创建并排的文本输入框
col1, col2 = st.columns(2)

with col1:
    ref_text = st.text_area("参考文本", "这是一个参考文本的例子。\n请按行输入。", height=300)

with col2:
    hyp_text = st.text_area("预期文本", "这是一个预期文本的例子。\n请按行输入。", height=300)

# 数字转中文映射
num_map = str.maketrans('0123456789', '零一二三四五六七八九')

# 文本预处理
import string

# 文本预处理
def preprocess(text):
    # 数字转中文
    text = text.translate(num_map)
    # 英文转小写
    text = text.lower()
    # 剔除空格
    text = re.sub(r'\s', '', text)
    # 剔除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# 计算逐行的句子准确率和字符准确率
def calculate_accuracies(ref_texts, hyp_texts):
    character_accuracies = []
    sentence_accuracies = []
    for ref, hyp in zip(ref_texts, hyp_texts):
        if ref.strip() == "":  # 忽略空行
            continue
        ref, hyp = preprocess(ref), preprocess(hyp)
        ser = wer(ref, hyp)
        cer_value = cer(ref, hyp)

        cer_value = 1 if cer_value > 1 else cer_value
        sentence_accuracies.append(1 - ser)
        character_accuracies.append(1 - cer_value)
    return character_accuracies, sentence_accuracies

# 当用户点击按钮时，计算并显示字准和句准，并在表格中展示每一对的字准和句准
if st.button('计算'):
    # 按行分割文本
    ref_lines = ref_text.split("\n")
    hyp_lines = hyp_text.split("\n")

    # 预处理后的文本
    preprocessed_ref_text = preprocess(ref_text)
    preprocessed_hyp_text = preprocess(hyp_text)

    # 校正行数使得两者匹配
    min_lines = min(len(ref_lines), len(hyp_lines))
    ref_lines = ref_lines[:min_lines]
    hyp_lines = hyp_lines[:min_lines]

    # 计算字准和句准
    total_character_accuracy = 1 - cer(preprocessed_ref_text, preprocessed_hyp_text)
    character_accuracies, sentence_accuracies = calculate_accuracies(ref_lines, hyp_lines)
    average_sentence_accuracy = sum(sentence_accuracies) / len(sentence_accuracies)

    st.write(f"总字符准确率: {total_character_accuracy:.2%}")
    st.write(f"平均句子准确率: {average_sentence_accuracy:.2%}")

    # 展示表格
    data = {
        "参考文本": [preprocess(line) for line in ref_lines],
        "假设文本": [preprocess(line) for line in hyp_lines],
        "字符准确率": [f"{acc:.2%}" for acc in character_accuracies],
        "句子准确率": [f"{acc:.2%}" for acc in sentence_accuracies]
    }
    st.table(data)
