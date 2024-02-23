import gradio as gr
from search.scholar import search_authors, search_pubs
from load.scihub import download_paper
from search.arxiv import general_search
import json

def search_and_display(input_text, search_type, top_n):
    if search_type == "author":
        results = search_authors(input_text, top_n)
        urls = [result.get('homepage', 'No URL available') for result in results]
    else:  # Assuming search_type is "publication"
        results = search_pubs(input_text, top_n)
        urls = [result.get('eprint_url', 'No URL available') for result in results]
    
    markdown_content = ""
    for i in range(max(len(urls), top_n)):
        url = urls[i] if i < len(urls) else 'No URL available'
        result = json.dumps(results[i], indent=2) if i < len(results) else '{}'
        link_text = f'[Link {i+1}]({url})' if url != 'No URL available' else "No URL available"
        markdown_content += f"**Result {i+1}:**\n{link_text}\n```json\n{result}\n```\n\n"
    
    return markdown_content

def search_arxiv_and_display(query, top_n):
    results = general_search(query, top_n)
    markdown_content = ""
    for i, result in enumerate(results):
        paper_info = {
            "title": result.title,
            "summary": result.summary.replace('\n', ' '),
            "url": result.entry_id.replace("/abs/", "/pdf/") + '.pdf'
        }
        json_str = json.dumps(paper_info, indent=2)
        markdown_content += f"**Result {i+1}:**\n[Link {i+1}]({paper_info['url']})\n```json\n{json_str}\n```\n\n"
    
    return markdown_content

results_markdown = gr.Markdown()

with gr.Blocks() as app:
    gr.Markdown("##### Search for Authors, Publications, or arXiv Papers")
    input_text = gr.Textbox(label="Enter Author Name, Publication Title, or arXiv Query")
    top_n_slider = gr.Slider(minimum=3, maximum=10, step=1, label="Number of Results")
        
    with gr.Row():
        search_arxiv_btn = gr.Button("Search on arXiv")        
        search_author_btn = gr.Button("Search Author on Scholar")
        search_pub_btn = gr.Button("Search Publication on Scholar")
    
    
    search_author_btn.click(search_and_display, inputs=[input_text, gr.Textbox(value="author", visible=False), top_n_slider], outputs=results_markdown)
    search_pub_btn.click(search_and_display, inputs=[input_text, gr.Textbox(value="publication", visible=False), top_n_slider], outputs=results_markdown)
    search_arxiv_btn.click(search_arxiv_and_display, inputs=[input_text, top_n_slider], outputs=results_markdown)
    
    # Define a single Markdown component for displaying results
    results_markdown
    
app.launch()