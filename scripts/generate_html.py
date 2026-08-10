import pandas as pd
import json
import re

def build_dashboard():
    # 1. Load Excel Data
    df = pd.read_excel('data/sales_data.xlsx')

    # 2. Group totals by State and District
    state_df = df.groupby('State')['Boards'].sum().sort_values(ascending=False).reset_index()
    district_df = df.groupby('District')['Boards'].sum().sort_values(ascending=False).head(10).reset_index()

    # 3. Format Data for JavaScript
    updated_sales_data = {
        "states": state_df['State'].tolist(),
        "stateVolumes": state_df['Boards'].tolist(),
        "districts": district_df['District'].tolist(),
        "districtVolumes": district_df['Boards'].tolist()
    }

    # 4. Generate JavaScript String
    js_code = f"<script>\nconst salesData = {json.dumps(updated_sales_data, indent=4)};\n</script>"

    # 5. Inject into index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    pattern = r'<!-- DATA_START -->.*?<!-- DATA_END -->'
    replacement = f'<!-- DATA_START -->\n{js_code}\n<!-- DATA_END -->'
    
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print("Successfully updated index.html!")

if __name__ == "__main__":
    build_dashboard()
