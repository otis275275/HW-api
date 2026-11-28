import os
import subprocess
from markdown_it import MarkdownIt

md_parser = MarkdownIt().enable('table').enable('strikethrough')

def render_md_file(md_path, html_path, title):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    rendered_body = md_parser.render(md_text)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; padding: 40px; max-width: 1000px; margin: 0 auto; color: #24292e; }}
  table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
  th, td {{ border: 1px solid #dfe2e5; padding: 8px 12px; text-align: left; }}
  th {{ background-color: #f6f8fa; font-weight: bold; }}
  tr:nth-child(2n) {{ background-color: #f8f8f8; }}
  code {{ background-color: #f6f8fa; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; font-size: 85%; }}
  pre code {{ background-color: transparent; padding: 0; }}
  pre {{ background-color: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; border: 1px solid #e1e4e8; }}
  blockquote {{ border-left: 4px solid #dfe2e5; color: #6a737d; padding: 0 1em; margin: 0; }}
  img {{ max-width: 100%; height: auto; display: block; margin: 15px 0; border: 1px solid #e1e4e8; border-radius: 4px; }}
  h1, h2, h3, h4 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
  @media print {{
    body {{ padding: 0; }}
    @page {{ margin: 1.5cm; }}
  }}
</style>
</head>
<body>
{rendered_body}
</body>
</html>"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

def print_pdf(html_path, pdf_path):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    abs_html = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    abs_pdf = os.path.abspath(pdf_path)
    tmp_user_dir = os.path.abspath(".tmp_chrome")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={tmp_user_dir}",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={abs_pdf}",
        abs_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(abs_pdf):
        print(f"Generated PDF: {abs_pdf} ({os.path.getsize(abs_pdf)} bytes)")

def convert_all():
    tasks = [
        ("report/main_report.md", "report/main_report.html", "report/main_report.pdf", "EShop API Main Report - 23120228"),
        ("report/ai_audit.md", "report/ai_audit.html", "report/ai_audit.pdf", "AI Audit Report - 23120228"),
        ("report/ai_critique.md", "report/ai_critique.html", "report/ai_critique.pdf", "AI Critique - 23120228"),
    ]

    for md_path, html_path, pdf_path, title in tasks:
        render_md_file(md_path, html_path, title)
        print_pdf(html_path, pdf_path)

if __name__ == '__main__':
    convert_all()
