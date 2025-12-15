#!/usr/bin/env python3
"""
Generate HTML catalog page from index.json
"""

import json
from datetime import datetime
from pathlib import Path

def read_catalog_data(json_path):
    """Read and parse the catalog index.json file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Filter out placeholder entries
    return [item for item in data if item.get('year') != 0]

def format_date(iso_date):
    """Format ISO date to readable format"""
    if not iso_date:
        return "Unknown date"
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %H:%M UTC")
    except:
        return iso_date
    
def each_word_upper(s):
    """Capitalize each word in a string"""
    return ' '.join(word.capitalize() for word in s.split())

def generate_html(catalog_data):
    """Generate HTML page from catalog data"""
    
    # Group by year
    grouped_by_year = {}
    for item in catalog_data:
        year = item.get('year', 'Unknown')
        if year not in grouped_by_year:
            grouped_by_year[year] = []
        grouped_by_year[year].append(item)
    
    # Sort years descending
    sorted_years = sorted(grouped_by_year.keys(), reverse=True)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phishing Catalog - Captured Pages</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        :root {{
            --primary-color: #00a8e8;
            --secondary-color: #003459;
            --dark-bg: #0a0e27;
            --card-bg: #1a1e3e;
        }}
        
        body {{
            background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1e3e 100%);
            min-height: 100vh;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .header {{
            background: rgba(0, 52, 89, 0.5);
            backdrop-filter: blur(10px);
            border-bottom: 2px solid var(--primary-color);
            padding: 2rem 0;
            margin-bottom: 3rem;
        }}
        
        .header h1 {{
            color: var(--primary-color);
            font-weight: 700;
            text-shadow: 0 0 20px rgba(0, 168, 232, 0.5);
        }}
        
        .header .subtitle {{
            color: #adb5bd;
            font-size: 1.1rem;
        }}
        
        .year-section {{
            margin-bottom: 3rem;
        }}
        
        .year-header {{
            background: linear-gradient(90deg, var(--primary-color), transparent);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--primary-color);
        }}
        
        .year-header h2 {{
            margin: 0;
            font-size: 1.8rem;
            font-weight: 600;
        }}
        
        .phishing-card {{
            background: var(--card-bg);
            border: 1px solid rgba(0, 168, 232, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: block;
        }}
        
        .phishing-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(0, 168, 232, 0.05), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .phishing-card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-color);
            box-shadow: 0 10px 30px rgba(0, 168, 232, 0.3);
        }}
        
        .phishing-card:hover::before {{
            opacity: 1;
        }}
        
        .card-title {{
            color: var(--primary-color);
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .card-domain {{
            color: #adb5bd;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        
        .card-description {{
            color: #dee2e6;
            margin-bottom: 1rem;
        }}
        
        .card-meta {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #adb5bd;
        }}
        
        .meta-item i {{
            color: var(--primary-color);
        }}
        
        .btn-view {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .btn-view:hover {{
            background: #0096d1;
            color: white;
            box-shadow: 0 5px 15px rgba(0, 168, 232, 0.4);
            transform: translateX(5px);
        }}
        
        .stats-card {{
            background: var(--card-bg);
            border: 1px solid rgba(0, 168, 232, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .stats-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}
        
        .stats-label {{
            color: #adb5bd;
            font-size: 1rem;
        }}
        
        .footer {{
            background: rgba(0, 52, 89, 0.3);
            border-top: 1px solid rgba(0, 168, 232, 0.2);
            padding: 2rem 0;
            margin-top: 4rem;
            text-align: center;
            color: #adb5bd;
        }}
        
        .warning-badge {{
            background: #dc3545;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
        }}
        
        .no-data {{
            text-align: center;
            padding: 3rem;
            color: #adb5bd;
        }}
        
        @media (max-width: 768px) {{
            .card-meta {{
                flex-direction: column;
                gap: 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1><i class="bi bi-shield-exclamation"></i> Phishing Catalog</h1>
            <p class="subtitle">Archived phishing pages for research and awareness</p>
        </div>
    </div>

    <div class="container">
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="stats-card">
                    <div class="stats-number">{len(catalog_data)}</div>
                    <div class="stats-label">Total Captures</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card">
                    <div class="stats-number">{len(grouped_by_year)}</div>
                    <div class="stats-label">Years</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card">
                    <div class="stats-number">{len(set(item.get('domain', '') for item in catalog_data))}</div>
                    <div class="stats-label">Unique Domains</div>
                </div>
            </div>
        </div>
"""

    if not catalog_data:
        html += """
        <div class="no-data">
            <i class="bi bi-inbox" style="font-size: 4rem; margin-bottom: 1rem; display: block;"></i>
            <h3>No phishing pages captured yet</h3>
            <p>Captured pages will appear here once added to the catalog.</p>
        </div>
"""
    else:
        for year in sorted_years:
            items = grouped_by_year[year]
            html += f"""
        <div class="year-section">
            <div class="year-header">
                <h2><i class="bi bi-calendar3"></i> {year}</h2>
            </div>
            <div class="row">
"""
            for item in items:
                domain = item.get('domain', 'Unknown domain')
                filename = item.get('filename', 'unknown')
                description = item.get('description', 'No description available')
                captured_at = format_date(item.get('capturedAt', ''))
                url = item.get('url', '#')
                path = item.get('path', f"{year}/{filename}/index.html")
                
                html += f"""
                <div class="col-lg-6">
                    <a class="phishing-card" href="{path}" target="_blank" rel="noopener noreferrer">
                        <div class="warning-badge">
                            <i class="bi bi-exclamation-triangle-fill"></i> PHISHING SITE
                        </div>
                        <h3 class="card-title">{each_word_upper(filename.replace('-', ' '))}</h3>
                        <div class="card-domain">
                            <i class="bi bi-globe"></i>Domain: {domain}
                        </div>
                        <p class="card-description">{description}</p>
                        <div class="card-meta">
                            <div class="meta-item">
                                <i class="bi bi-clock"></i>
                                <span>{captured_at}</span>
                            </div>
                            <div class="meta-item">
                                <i class="bi bi-link-45deg"></i>
                                <span title="{url}">{url[:50]}{'...' if len(url) > 50 else ''}</span>
                            </div>
                        </div>
                        <div href="{path}" class="btn-view" target="_blank" rel="noopener noreferrer">
                            <i class="bi bi-eye"></i> View Captured Page
                        </div>
                    </a>
                </div>
"""
            html += """
            </div>
        </div>
"""

    html += f"""
    </div>

    <div class="footer">
        <div class="container">
            <p><i class="bi bi-info-circle"></i> This catalog contains archived phishing pages for educational and research purposes only.</p>
            <p>⚠️ <strong>Warning:</strong> These are real phishing pages. Do not enter any personal information.</p>
            <p class="mt-3">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    return html

def main():
    """Main function"""
    # Paths
    script_dir = Path(__file__).parent.parent
    json_path = script_dir / 'catalog' / 'index.json'
    output_path = script_dir / 'catalog' / 'index.html'
    
    print(f"Reading catalog data from: {json_path}")
    catalog_data = read_catalog_data(json_path)
    print(f"Found {len(catalog_data)} catalog entries")
    
    print("Generating HTML page...")
    html_content = generate_html(catalog_data)
    
    print(f"Writing HTML to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Catalog page generated successfully!")
    print(f"   Open: {output_path}")

if __name__ == '__main__':
    main()
