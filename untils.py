import os
import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI

# 过滤 BeautifulSoup 解析器警告
warnings.filterwarnings("ignore", message=".*GuessedAtParserWarning.*")
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

def generate_script(subject, video_length, creativity, api_key=None):
    # 获取 API 密钥
    api_key = api_key or os.getenv('ARK_API_KEY')
    if not api_key:
        raise ValueError("请提供 API 密钥：可以通过参数传入或设置环境变量 ARK_API_KEY")
    
    # 创建提示模板
    title_template = ChatPromptTemplate.from_messages([
        ('human', '请给出视频的主题：{subject}')
    ])
    
    script_template = ChatPromptTemplate.from_messages([
        ('human', '''你是一位视频创作专家。擅长制作关于{title}的视频，我希望内容经过充分研究和整理。这个视频的时长是{duration}，目的是创造吸引观众，表达方式轻松有趣且符合潮流的视频内容。你能帮助我研究这个细分领域的话题，并制作一份全面的视频大纲吗？可以参考维基百科搜索到的信息并作为参考信息给出"""{wiki_search}"""。''')
    ])

    # 创建模型
    model = ChatOpenAI(
        model_name="doubao-seed-1-6-251015",
        temperature=creativity,
        openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
        openai_api_key=api_key
    )

    # 创建链
    title_chain = title_template | model
    script_chain = script_template | model

    # 生成标题
    title = title_chain.invoke({'subject': subject}).content

    # 搜索维基百科
    try:
        search = WikipediaAPIWrapper(lang='zh')
        search_result = search.run(subject)
        if not search_result or not search_result.strip() or search_result.strip() == "No good Wikipedia Search Result was found":
            search_result = f"未找到关于'{subject}'的维基百科信息"
    except Exception as e:
        search_result = f"未找到关于'{subject}'的维基百科信息（搜索失败）"

    # 生成脚本
    script = script_chain.invoke({'title': title, 'duration': video_length, 'wiki_search': search_result}).content
    
    return search_result, title, script