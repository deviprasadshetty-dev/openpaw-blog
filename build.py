import os
import markdown
import re

POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

def process_md():
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    if not md_files:
        return

    for md_file in md_files:
        filepath = os.path.join(POSTS_DIR, md_file)
        base_name = md_file[:-3]
        html_filepath = os.path.join(POSTS_DIR, f"{base_name}.html")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        title = "Untitled"
        date_str = "2026-03-20"
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                content = parts[2]
                for line in frontmatter.split('\n'):
                    if line.startswith('title:'): title = line.replace('title:', '').strip()
                    elif line.startswith('date:'): date_str = line.replace('date:', '').strip()

        html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
        text_only = re.sub('<[^<]+>', '', html_content)
        snippet = text_only[:150] + '...'

        template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | OpenPaw</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        gray: {{ 900: '#0f172a', 800: '#1e293b', 700: '#334155' }},
                        primary: {{ 500: '#3b82f6', 400: '#60a5fa' }}
                    }},
                    fontFamily: {{
                        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
                    }}
                }}
            }}
        }}
    </script>
    <style>
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #0f172a; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}
        .prose a {{ color: #60a5fa; text-decoration: none; }}
        .prose a:hover {{ color: #93c5fd; }}
        .prose h1 {{ font-size: 2rem; color: white; margin-top: 1.5em; margin-bottom: 0.5em; font-weight: bold; }}
        .prose h2 {{ font-size: 1.5rem; color: white; margin-top: 1.5em; margin-bottom: 0.5em; font-weight: bold; }}
        .prose h3 {{ font-size: 1.25rem; color: white; margin-top: 1.5em; margin-bottom: 0.5em; font-weight: bold; }}
        .prose p {{ margin-bottom: 1.5em; line-height: 1.7; }}
        .prose ul {{ list-style-type: disc; padding-left: 1.5em; margin-bottom: 1.5em; }}
        .prose li {{ margin-bottom: 0.5em; }}
        .prose strong {{ color: white; }}
    </style>
</head>
<body class="bg-gray-900 text-gray-300 font-mono min-h-screen flex flex-col antialiased">
    <div class="max-w-3xl w-full mx-auto px-6 py-12 flex-grow">
        <header class="mb-12 border-b border-gray-800 pb-8">
            <a href="../index.html" class="text-primary-400 hover:text-primary-300 text-sm mb-6 inline-block">← Back to System Logs</a>
            <time class="text-xs text-gray-500 mb-2 block">{date_str}</time>
            <h1 class="text-3xl font-bold text-white tracking-tight">{title}</h1>
        </header>
        <main class="prose prose-invert max-w-none">
            {html_content}
        </main>
    </div>
</body>
</html>"""
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(template)

        # Update index.html
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_html = f.read()

        article_block = f"""                <article class="group relative">
                    <div class="absolute -inset-y-4 -inset-x-4 z-0 scale-95 bg-gray-800/50 opacity-0 transition group-hover:scale-100 group-hover:opacity-100 rounded-lg"></div>
                    <div class="relative z-10">
                        <time class="text-xs text-gray-500 mb-2 block">{date_str}</time>
                        <h3 class="text-xl font-semibold text-white mb-3">
                            <a href="posts/{base_name}.html" class="hover:text-primary-400 transition-colors">
                                <span class="text-primary-500 mr-2">></span>{title}
                            </a>
                        </h3>
                        <p class="text-gray-400 text-sm leading-relaxed">
                            {snippet}
                        </p>
                        <a href="posts/{base_name}.html" class="text-primary-400 text-sm mt-4 inline-flex items-center hover:text-primary-300 transition-colors">
                            Read log <span class="ml-1 group-hover:translate-x-1 transition-transform">→</span>
                        </a>
                    </div>
                </article>

"""
        target = '<div class="space-y-12">\n'
        index_html = index_html.replace(target, target + article_block)

        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(index_html)

        # Delete the .md file so it doesn't get processed again
        os.remove(filepath)

if __name__ == '__main__':
    process_md()
