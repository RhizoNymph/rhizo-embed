import gradio as gr
from search.scihub import search_authors, search_pubs
from load.scihub import download_paper
from search.arxiv import general_search
import json

def search_and_display(input_text, search_type):
    if search_type == "author":
        results = search_authors(input_text)
        urls = [result.get('homepage', 'No URL available') for result in results]
    else:  # Assuming search_type is "publication"
        results = search_pubs(input_text)
        urls = [result.get('eprint_url', 'No URL available') for result in results]
    
    # Ensure there are always 3 results for both URLs and JSON, filling with placeholders if necessary
    while len(urls) < 3:
        urls.append('No URL available')
    while len(results) < 3:
        results.append({})
    
    # Convert results to JSON strings
    json_results = [json.dumps(result, default=str) for result in results]
    
    # Assuming urls is your list of URLs
    markdown_urls = [f'<a href="{url}" style="color: white;font-size: 20px">Link</a>' if url != 'No URL available' else "No URL available" for url in urls]
    
    # Split markdown_urls and json_results into separate variables to match the expected six outputs
    markdown_url1, markdown_url2, markdown_url3 = markdown_urls[:3]
    json_result1, json_result2, json_result3 = json_results[:3]
    
    return markdown_url1, json_result1, markdown_url2, json_result2, markdown_url3, json_result3

def download_and_show_status(paper_title):
    try:
        download_paper(paper_title)
        return f"Successfully downloaded: {paper_title}"
    except Exception as e:
        return f"Failed to download {paper_title}: {str(e)}"

def search_arxiv_and_display(query):
    results = general_search(query)
    json_results = []
    markdown_urls = []
    for result in results:
        paper_info = {
            "title": result.title,
            "summary": result.summary.replace('\n', ' '),
            "url": result.entry_id
        }
        json_results.append(json.dumps(paper_info, default=str))  # Convert to JSON string here to match the output format
        
        # Create markdown link for each result
        markdown_url = f'<a href="{result.entry_id.replace("/abs/", "/pdf/") + '.pdf'}" style="color: white;font-size: 20px">Link</a>'
        markdown_urls.append(markdown_url)
    
    # Ensure there are always 3 results for both URLs and JSON, filling with placeholders if necessary
    while len(markdown_urls) < 3:
        markdown_urls.append('No URL available')
    while len(json_results) < 3:
        json_results.append('{}')
    
    # Split markdown_urls and json_results into separate variables to match the expected six outputs
    markdown_url1, markdown_url2, markdown_url3 = markdown_urls[:3]
    json_result1, json_result2, json_result3 = json_results[:3]
    
    return markdown_url1, json_result1, markdown_url2, json_result2, markdown_url3, json_result3

with gr.Blocks() as app:
    gr.Markdown("##### Search for Authors, Publications, or arXiv Papers")
    input_text = gr.Textbox(label="Enter Author Name, Publication Title, or arXiv Query")
    with gr.Row():
        gr.Markdown("### Google Scholar")
        search_author_btn = gr.Button("Search Author")
        search_pub_btn = gr.Button("Search Publication")
    with gr.Row():
        gr.Markdown("### Sci-Hub and Arxiv")
        download_paper_btn = gr.Button("Download Paper")
        search_arxiv_btn = gr.Button("Search arXiv")  # New button for arXiv search
    
    search_type_author = gr.Textbox(value="author", visible=False)
    search_type_publication = gr.Textbox(value="publication", visible=False)
    
    with gr.Accordion("Search Results"):  
        with gr.Accordion("Result 1"):      
            markdown_link1 = gr.Markdown()        
            output_json1 = gr.JSON()
        with gr.Accordion("Result 2"):
            markdown_link2 = gr.Markdown()
            output_json2 = gr.JSON()
        with gr.Accordion("Result 3"):
            markdown_link3 = gr.Markdown()
            output_json3 = gr.JSON()

    search_author_btn.click(search_and_display, inputs=[input_text, search_type_author], outputs=[markdown_link1, output_json1, markdown_link2, output_json2, markdown_link3, output_json3])
    search_pub_btn.click(search_and_display, inputs=[input_text, search_type_publication], outputs=[markdown_link1, output_json1, markdown_link2, output_json2, markdown_link3, output_json3])
    download_paper_btn.click(download_and_show_status, inputs=[input_text], outputs=[])
    search_arxiv_btn.click(search_arxiv_and_display, inputs=[input_text], outputs=[markdown_link1, output_json1, markdown_link2, output_json2, markdown_link3, output_json3])
    
app.launch()