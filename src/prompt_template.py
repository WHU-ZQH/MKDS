get_llm_knowledge = "详细介绍医学术语：{}"

# check_consistency = """任务：对比并检查以下两段关于同一医学主题的文本内容是否一致。

# 源1：{graph_know}
# 源2：{retrival_know}

# 指令：
# 1. 请仔细阅读并理解上述两段文本的核心信息。
# 2. 判断两段文本在核心信息上是否存在矛盾或冲突。
# 3. 请明确给出结论：一致、冲突 或 部分冲突。
# 4. 如果判定为 冲突 或 部分冲突，请简要说明具体冲突或不一致的关键点在哪里，侧重事实性描述的差异。

# 输出格式：
# 判定结论： [填写：一致 / 冲突 / 部分冲突]
# 冲突说明： [如果是冲突或部分冲突，在此处简述冲突点；如果一致，可写“无明显冲突”]"""

# check_consistency = """以下是两段有关**{name}**的医学文本。

# 医学文本1：{graph_know}

# 医学文本2：{retrival_know}

# 请仔细阅读并理解上述两段医学文本，综合两段文本信息进行交叉验证，过滤掉两段文本中不一致的信息，只保留两段文本中描述一致的信息。
# 不要包含任何解释，直接输出最终综合后有关`{name}`的医学文本，你的医学文本中应该包含`{name}`并放在开头，以普通文本格式输出。"""

check_consistency = """你是一位专业的医学知识校验专家，负责对以下多源医学知识进行一致性校验和整合。请按照以下步骤完成任务：
1. 对比多源数据：从提供的不同来源的医学知识中，提取与目标医学术语相关的所有信息，包括疾病定义、症状、病因、治疗方法、预后等。
2. 识别矛盾或错误：检查不同来源的信息是否存在矛盾或错误，例如：
    - 是否有来源提供的信息与权威医学标准冲突？
    - 是否有来源提供的信息明显过时或不完整？
    - 是否有来源提供的信息缺乏科学依据或者在误导性？
3. 补充缺失信息：如果某些来源的信息不完整，请结合权威医学知识补充缺失的部分。
4. 生成权威整合结果：基于对比和校验的结果，生成一份权威、一致且完整的医学知识描述。

请以清晰的逻辑和结构化的方式呈现结果，包括：

- 矛盾点：列出不同来源之间的矛盾信息。
- 错误点：指出明显错误或不科学的信息。
- 整合结果：提供经过校验和补充的权威知识描述。

提供的多源知识：
源1: {graph_know}

源2: {retrival_know}

返回格式：
### 矛盾点
...
### 错误点
...
### 整合结果
..."""

# ner_prompt = """**Task**:
# Please generate high-quality Named Entity Recognition (NER) instruction-tuning data based on the provided medical knowledge.

# **Medical Knowledge**:
# ```{entity_knowledge}```

# **Please adhere to the following guidelines**:
# - The instruction should clearly describe the task objective, including the types of entities to be identified (e.g., diseases, medications, symptoms).
# - The input text should contain sufficient context to accurately recognize entities.
# - The output should list all identified entities along with their categories, formatted as: Entity Name|Category.
# - If applicable, provide any potential aliases or abbreviations.
# - Ensure that both instructions and outputs comply with industry standards and terminology in the medical field.

# **Return Format**:
# {
#     "instruction": "A specific NER instruction, e.g., Identify and label all disease names from the given text.",
#     "input": "The medical text for analysis, e.g., The patient reported symptoms of headache and fever and has been diagnosed with influenza.",
#     "output": "The correct output corresponding to the input, e.g., headache|symptom, fever|symptom, influenza|disease"
# }"""

ner_prompt = """**Task**:
Please generate high-quality Named Entity Recognition (NER) instruction-tuning data based on the provided medical knowledge.

**Medical Knowledge**:
```{entity_knowledge}```

**Please adhere to the following guidelines**:
- The instruction should clearly describe the task objective, including the types of entities to be identified (e.g., diseases, medications, symptoms).
- The input text should contain sufficient context to accurately recognize entities.
- The output should list all identified entities along with their categories, formatted as: Entity Name|Category.
- If applicable, provide any potential aliases or abbreviations.
- Ensure that both instructions and outputs comply with industry standards and terminology in the medical field.

**Return Format**:
[
    {
        "instruction": "A specific NER instruction, e.g., Identify and label all disease names from the given text.",
        "input": "The medical text for analysis, e.g., The patient reported symptoms of headache and fever and has been diagnosed with influenza.",
        "output": "The correct output corresponding to the input, e.g., headache|symptom, fever|symptom, influenza|disease"
    },
    ...
]"""

# text_classification_prompt = """**Task**:
# Please generate high-quality medical text classification instruction-tuning data based on the provided medical knowledge.

# **Medical Knowledge**:
# ```{entity_knowledge}```

# **Please adhere to the following guidelines**:
# - The instruction should clearly describe the task objective, including the types of texts to be classified (e.g., diagnostic reports, treatment plans, medical records).
# - The input text should contain sufficient context for accurate classification.
# - The output should provide the correct classification labels for each input text.
# - Classification labels should be clear and adhere to standard medical terminology.
# - If applicable, explain any subtle differences or special cases between categories.

# **Return Format**:
# {
#     "instruction": "A specific medical text classification instruction, e.g., Classify the given diagnostic report into the appropriate disease category.",
#     "input": "The medical text for analysis, e.g., The patient complains of headache, accompanied by nausea and blurred vision...",
#     "output": "The correct classification corresponding to the input, e.g., Migraine"
# }"""

text_classification_prompt = """**Task**:
Please generate high-quality medical text classification instruction-tuning data based on the provided medical knowledge.

**Medical Knowledge**:
```{entity_knowledge}```

**Please adhere to the following guidelines**:
- The instruction should clearly describe the task objective, including the types of texts to be classified (e.g., diagnostic reports, treatment plans, medical records).
- The input text should contain sufficient context for accurate classification.
- The output should provide the correct classification labels for each input text.
- Classification labels should be clear and adhere to standard medical terminology.
- If applicable, explain any subtle differences or special cases between categories.

**Return Format**:
[
    {
        "instruction": "A specific medical text classification instruction, e.g., Classify the given diagnostic report into the appropriate disease category.",
        "input": "The medical text for analysis, e.g., The patient complains of headache, accompanied by nausea and blurred vision...",
        "output": "The correct classification corresponding to the input, e.g., Migraine"
    },
    ...
]"""

# relation_extract_prompt = """**Task**:
# Please construct a high-quality Instruction fine-tuning sample for relation extraction based on the provided medical knowledge, intended for the analysis and understanding of medical text information.

# **Medical Knowledge**:
# ```{entity_knowledge}```

# **Please follow these guidelines to create the dataset**:
# 1. Ensure each question focuses on extracting specific types of information from the given medical knowledge.
# 2. Design questions to be specific enough to avoid ambiguity or multiple interpretations.
# 3. Answers should accurately reflect the facts presented in the medical knowledge and include as much detail as possible.
# 4. Where applicable, include relationships between entities such as drugs and diseases, symptoms and diagnoses.
# 5. Use professional terminology while ensuring that the text remains clear and comprehensible for medical professionals.

# **Return Format**:
# {
#     "question": "A specific, focused task for extracting information from medical text",
#     "answer": "A precise answer to the question, including all necessary details"
# }"""

relation_extract_prompt = """**Task**:
Please construct a high-quality Instruction fine-tuning sample for relation extraction based on the provided medical knowledge, intended for the analysis and understanding of medical text information.

**Medical Knowledge**:
```{entity_knowledge}```

**Please follow these guidelines to create the dataset**:
1. Ensure each question focuses on extracting specific types of information from the given medical knowledge.
2. Design questions to be specific enough to avoid ambiguity or multiple interpretations.
3. Answers should accurately reflect the facts presented in the medical knowledge and include as much detail as possible.
4. Where applicable, include relationships between entities such as drugs and diseases, symptoms and diagnoses.
5. Use professional terminology while ensuring that the text remains clear and comprehensible for medical professionals.

**Return Format**:
[
    {
        "question": "A specific, focused task for extracting information from medical text",
        "answer": "A precise answer to the question, including all necessary details"
    },
    ...
]"""

# qa_prompt = """**Task**:
# Please construct a set of high-quality, practically applicable medical Q&A data based on the provided medical knowledge. Ensure that each question is clear, specific, and that the answers accurately reflect the latest medical insights and practices.

# **Medical Knowledge**:
# ```{entity_knowledge}```

# **Please follow these guidelines to create the dataset**:
# 1. Questions should be directly based on the provided medical knowledge, avoiding overly broad or unrelated questions.
# 2. Answers should include sufficient explanatory information to ensure understanding by non-specialists.
# 3. Where applicable, include key points such as preventive measures, symptom recognition, treatment options, and expected outcomes.
# 4. For potentially confusing concepts or terms, provide concise definitions or clarifications.
# 5. If the medical knowledge mentions statistics or research findings, cite this information in your answers to enhance authority.

# **Return Format**:
# {
#     "question": "Specific high-quality medical question",
#     "answer": "Correct response to the question, including all necessary explanations and background information"
# }"""

qa_prompt = """**Task**:
Please construct a set of high-quality, practically applicable medical Q&A data based on the provided medical knowledge. Ensure that each question is clear, specific, and that the answers accurately reflect the latest medical insights and practices.

**Medical Knowledge**:
```{entity_knowledge}```

**Please follow these guidelines to create the dataset**:
1. Questions should be directly based on the provided medical knowledge, avoiding overly broad or unrelated questions.
2. Answers should include sufficient explanatory information to ensure understanding by non-specialists.
3. Where applicable, include key points such as preventive measures, symptom recognition, treatment options, and expected outcomes.
4. For potentially confusing concepts or terms, provide concise definitions or clarifications.
5. If the medical knowledge mentions statistics or research findings, cite this information in your answers to enhance authority.

**Return Format**:
[
    {
        "question": "Specific high-quality medical question",
        "answer": "Correct response to the question, including all necessary explanations and background information"
    },
    ...
]"""

# multi_choice_prompt = """**Task**:
# Please construct a set of high-quality, practically applicable multiple-choice questions (MCQs) based on the provided medical knowledge. Ensure that each question is clear and specific, and that the options are well-designed, including one correct answer and several plausible distractors (incorrect but seemingly reasonable options). Additionally, the answer section should clearly indicate the correct option and may optionally provide an explanation to aid learners in understanding.

# **Medical Knowledge**:
# ```{entity_knowledge}```

# **The created MCQs should meet the following criteria**:
# 1. Questions should be directly based on the provided medical knowledge, avoiding overly broad or unrelated questions.
# 2. Each question should have four options: one correct answer and three distractors. The distractors should be plausible incorrect options that appear reasonable to non-experts.
# 3. Answers should clearly specify which option is correct and may optionally include a brief explanation or additional information to clarify why this option is correct.
# 4. Where applicable, include key points such as preventive measures, symptom recognition, treatment options, and expected outcomes.
# 5. For potentially confusing concepts or terms, provide concise definitions or clarifications within the question.
# 6. If the medical knowledge mentions statistics or research findings, reference this information in the question or explanation to enhance credibility.

# **Return Format**:
# {
#     "question": "Specific high-quality medical multiple-choice question",
#     "options": [
#         "Option A",
#         "Option B",
#         "Option C",
#         "Option D"
#     ],
#     "correct_answer": "Correct answer letter (e.g., A, B, C, or D)",
#     "explanation": "Explanation of why this option is correct, along with any other relevant information"
# }"""

multi_choice_prompt = """**Task**:
Please construct a set of high-quality, practically applicable multiple-choice questions (MCQs) based on the provided medical knowledge. Ensure that each question is clear and specific, and that the options are well-designed, including one correct answer and several plausible distractors (incorrect but seemingly reasonable options). Additionally, the answer section should clearly indicate the correct option and may optionally provide an explanation to aid learners in understanding.

**Medical Knowledge**:
```{entity_knowledge}```

**The created MCQs should meet the following criteria**:
1. Questions should be directly based on the provided medical knowledge, avoiding overly broad or unrelated questions.
2. Each question should have four options: one correct answer and three distractors. The distractors should be plausible incorrect options that appear reasonable to non-experts.
3. Answers should clearly specify which option is correct and may optionally include a brief explanation or additional information to clarify why this option is correct.
4. Where applicable, include key points such as preventive measures, symptom recognition, treatment options, and expected outcomes.
5. For potentially confusing concepts or terms, provide concise definitions or clarifications within the question.
6. If the medical knowledge mentions statistics or research findings, reference this information in the question or explanation to enhance credibility.

**Return Format**:
[
    {
        "question": "Specific high-quality medical multiple-choice question",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": "Correct answer letter (e.g., A, B, C, or D)",
        "explanation": "Explanation of why this option is correct, along with any other relevant information"
    },
    ...
]"""

dialog_prompt = """**Task**: 
Extract key medical knowledge with educational and clinical application value from the provided professional medical text, and design a dialogue scenario that includes at least six rounds of interaction. This dialogue should guide users to gain a deeper understanding of medical knowledge step by step while ensuring that information is communicated clearly, accurately, and in an accessible manner.

**Medical Text**:
```{entity_knowledge}```

**Please adhere to the following guidelines**:
1. The dialogue should flow naturally, simulating authentic doctor-patient communication.
2. Each round of dialogue must include a user's question or statement, followed by the AI assistant's response.
3. The assistant's responses should be based on the provided medical text but explain complex concepts in an easy-to-understand way.
4. The assistant should pose questions or offer suggestions at appropriate times to encourage user engagement and reflection.
5. Ensure all critical medical knowledge points are covered within the dialogue.
6. By the end of the dialogue, the user should have a comprehensive understanding of the discussed topic.

**Return Format**:
[
    {
        "human": "User's question or statement",
        "assistant": "AI assistant's response or advice"
    },
    {
        "human": "Possible further questions or reactions from the user",
        "assistant": "Further explanation or guidance from the AI assistant"
    },
    ...
]"""

# score = """你是一个评估医学领域指令微调数据质量的专家，请对给定医学领域指令微调数据的###{dimension}###进行严格的评估，并给出1到5的评分，分数越高表示###{dimension}###越高。返回的结果中应包括具体的评分和详细的评分依据。

# ### 医学领域指令微调数据
# - **指令**：{question}
# - **输出**：{answer}

# ### 返回格式要求：
# 具体的评分：[填写1到5的评分]
# 评分依据：[详细描述评分依据]"""

# score = """你是一位医学领域的专家，负责对医学领域大语言模型（LLM）的监督微调数据进行质量评估，你的任务是评估一组“指令-输出”对的质量，并给出多维度评估分数。

# ### 医学领域指令微调数据
# - **指令**：```{question}```
# - **输出**：```{answer}```

# ### 评估维度（1-5分）

# 1. 准确性 (accuracy)：输出内容是否正确回答了问题？是否事实准确？是否存在幻觉或错误信息？是否与医学知识强相关？
# 2. 清晰度 (clarity)：指令和输出表达是否清晰完整？

# ### 返回格式要求：
# {
#     "reason": "简要说明打分理由",
#     "scores": {
#         "accuracy": 0,
#         "clarity": 0
#     },
#     "average_score": 0
# }"""

score = """你是一位医学领域的专家，负责对医学领域大语言模型（LLM）的监督微调数据进行质量评估，你的任务是评估一组“指令-输出”对的质量，并给出多维度评估分数。

### 医学领域指令微调数据
- **指令**：```{question}```
- **输出**：```{answer}```

### 评估维度（1-5分）

1. 准确性 (accuracy)：输出的内容越准确，错误信息越少，分数越高；
2. 医学相关性 (relevance)：包含的医学知识越丰富，与日常医学相关性越高，分数越高。

### 返回格式要求：
{
    "reason": "简要说明打分理由",
    "scores": {
        "accuracy": 0,
        "relevance": 0
    },
    "average_score": 0
}"""

# score = """你是一位医学领域的专家，负责对医学领域大语言模型（LLM）的监督微调数据进行质量评估，你的任务是评估一组“指令-输出”对的质量，并给出多维度评估分数。

# ### 医学领域指令微调数据
# - **指令**：```{question}```
# - **输出**：```{answer}```

# ### 评估维度（1-5分）

# 1. 准确性 (accuracy)：输出内容是否正确回答了问题？事实准确？是否存在幻觉或错误信息？
# 2. 医学相关性 (relevance)：微调数据是否包含医学知识？
# 2. 清晰度 (clarity)：指令和输出表达是否清晰完整？

# ### 评分规则

# - 1-2分：劣质数据。存在严重逻辑错误、格式混乱或指令完全不匹配。应被剔除。
# - 3分：普通数据。基本可用，但较为平庸或存在轻微瑕疵。
# - 4-5分：优质数据。回答准确，表达清晰完整，是微调模型的理想样本。

# ### 返回格式要求：
# {
#     "reason": "简要说明打分理由",
#     "scores": {
#         "accuracy": 0,
#         "relevance": 0,
#         "clarity": 0
#     },
#     "average_score": 0
# }"""

# score = """你是一位医学领域的专家，负责对医学领域大语言模型（LLM）的监督微调数据进行质量评估，你的任务是评估一条医学监督微调数据的质量，并给出多维度评估分数。

# ### 医学领域指令微调数据

# - **指令**：```{question}```
# - **输出**：```{answer}```

# ### 评估维度（1-5分）

# 1. 准确性 (accuracy)：输出内容是否正确回答了问题？回答是否准确？是否存在幻觉或错误信息？
# 2. 医学相关性 (relevance)：微调数据是否与医学强相关？是否适合作为医学
# 3. 清晰度 (clarity)：指令和输出表达是否清晰完整？是否存在歧义？
# 4. 数据质量（quality）：数据质量是否满足作为高质量监督微调数据？

# ### 返回格式要求：
# {
#     "reason": "简要说明打分理由",
#     "scores": {
#         "accuracy": 0,
#         "relevance": 0,
#         "clarity": 0,
#         "quality": 0
#     },
#     "average_score": 0
# }"""
