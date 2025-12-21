import os
import warnings
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI

# 过滤 BeautifulSoup 解析器警告（来自 wikipedia 库）
warnings.filterwarnings("ignore", message=".*GuessedAtParserWarning.*")
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

def generate_script(subject, video_length, creativity, api_key=None):
    # 获取 API 密钥：优先使用传入的参数，其次使用环境变量
    api_key = api_key or os.getenv('ARK_API_KEY')
    if not api_key:
        raise ValueError("请提供 API 密钥：可以通过参数传入或设置环境变量 ARK_API_KEY")
    
    title_template =  ChatPromptTemplate.from_messages(
        [
            ('human', '请给出视频的主题：{subject}')
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ('human', '''你是一位视频创作专家。擅长制作关于{title}的视频，我希望内容经过充分研究和整理。这个视频的时长是{duration}，目的是创造吸引观众，表达方式轻松有趣且符合潮流的视频内容。你能帮助我研究这个细分领域的话题，并制作一份全面的视频大纲吗？可以参考维基百科搜索到的信息并作为参考信息给出"""{wiki_search}"""。''')
        ]
    )

    model = ChatOpenAI(
        model_name="doubao-seed-1-8-251215",
        temperature=creativity,
        openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
        openai_api_key=api_key
    )

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({'subject': subject}).content

    # 尝试搜索维基百科，如果失败则使用空字符串
    search_result = ""
    print(f'🔍 开始搜索维基百科: {subject}')
    
    # 优先使用 wikipedia 库直接搜索（更可靠）
    try:
        import wikipedia
        wikipedia.set_lang("zh")
        # 先搜索页面标题
        print(f'📚 使用 wikipedia 库搜索...')
        search_pages = wikipedia.search(subject, results=3)
        
        if search_pages and len(search_pages) > 0:
            # 尝试获取第一个匹配页面的内容
            try:
                page = wikipedia.page(search_pages[0], auto_suggest=False)
                search_result = page.content
                print(f'✅ 维基百科搜索成功，找到页面: {page.title}')
                
                # 限制搜索结果长度，避免过长
                if len(search_result) > 2000:
                    search_result = search_result[:2000] + "..."
                    print(f'📝 搜索结果已截断至 2000 字符')
            except wikipedia.exceptions.DisambiguationError as e:
                # 如果是消歧义页面，使用第一个选项
                print(f'⚠️ 发现消歧义页面，使用第一个选项: {e.options[0] if e.options else search_pages[0]}')
                try:
                    page = wikipedia.page(e.options[0] if e.options else search_pages[0], auto_suggest=False)
                    search_result = page.content
                    if len(search_result) > 2000:
                        search_result = search_result[:2000] + "..."
                except Exception:
                    search_result = f"找到关于'{subject}'的维基百科页面，但无法获取内容"
            except wikipedia.exceptions.PageError:
                print(f'⚠️ 页面不存在，尝试使用 LangChain 搜索...')
                search_result = ""
            except Exception as page_error:
                print(f'⚠️ 获取页面内容失败: {page_error}')
                search_result = ""
        else:
            print(f'⚠️ 未找到匹配的维基百科页面')
            search_result = ""
    except Exception as wiki_error:
        print(f'⚠️ wikipedia 库搜索失败: {type(wiki_error).__name__}: {wiki_error}')
        search_result = ""
    
    # 如果 wikipedia 库搜索失败，尝试使用 LangChain 的 WikipediaAPIWrapper
    if not search_result or len(search_result.strip()) == 0:
        try:
            print(f'🔄 尝试使用 LangChain WikipediaAPIWrapper 搜索...')
            search = WikipediaAPIWrapper(lang='zh')
            search_result = search.run(subject)
            
            # 检查搜索结果是否为空
            if not search_result or len(search_result.strip()) == 0:
                print(f'⚠️ LangChain 搜索返回空结果')
                search_result = f"未找到关于'{subject}'的维基百科信息"
            else:
                print(f'✅ LangChain 维基百科搜索成功，结果长度: {len(search_result)} 字符')
                # 限制搜索结果长度，避免过长
                if len(search_result) > 2000:
                    search_result = search_result[:2000] + "..."
        except Exception as langchain_error:
            print(f'⚠️ LangChain 维基百科搜索失败: {type(langchain_error).__name__}: {langchain_error}')
            if not search_result or len(search_result.strip()) == 0:
                search_result = f"未找到关于'{subject}'的维基百科信息"
    
    # 最终检查
    if not search_result or len(search_result.strip()) == 0:
        search_result = f"未找到关于'{subject}'的维基百科信息"
        print(f'⚠️ 所有维基百科搜索方法都失败，使用默认消息')

    script = script_chain.invoke({'title':title,'duration':video_length,'wiki_search':search_result}).content
    return search_result,title,script
