import json

def get_td_class_and_value(raw_excel_value, section_type):
    display_text = str(raw_excel_value) if raw_excel_value is not None else ""
    
    if not display_text.strip():
        return "", "" # Empty display text, no class

    style_text = display_text.replace("=", "")
    num_val = -1000  # Default if not parsable

    try:
        num_val = int(style_text)
    except ValueError:
        try:
            num_val = float(style_text) # Try float if int fails
        except ValueError:
            pass # Keep num_val as -1000 if not a number

    css_class = ""
    if section_type == 'training':
        css_class = "bg-primary-subtle"
    elif section_type == 'inference_quant':
        css_class = "bg-light-subtle"
    elif section_type == 'architecture':
        if num_val == 1:
            css_class = "bg-danger-subtle"
        elif num_val == 2 or num_val == 3:
            css_class = "bg-warning-subtle"
        elif num_val >= 4: # Handles 4 and potentially other higher scores if they were green
            css_class = "bg-success-subtle"
    
    return display_text, css_class

def generate_row_html(excel_row_data, section_type):
    method_name = str(excel_row_data[0]) if excel_row_data[0] is not None else ""
    cells_html = [f"  <td>{method_name}</td>"]
    # Data columns are from index 1 to 9 in excel_row_data
    for i in range(1, 10): 
        raw_val = excel_row_data[i] if i < len(excel_row_data) else None
        val_str, css_cl = get_td_class_and_value(raw_val, section_type)
        cells_html.append(f'  <td class="{css_cl}">{val_str}</td>')
    return "\n".join(cells_html)

# Load the raw data from JSON
with open('excel_data_raw.json', 'r') as f:
    all_excel_data = json.load(f)

# Filter out completely empty rows (all elements are None)
cleaned_excel_rows = [row for row in all_excel_data if any(cell is not None for cell in row)]
excel_data_iter = iter(cleaned_excel_rows)

tbody_html = ["<tbody>"]

# Helper to consume next data row
def get_next_data_row():
    try:
        return next(excel_data_iter)
    except StopIteration:
        # Return a row of Nones if data runs out, to prevent crashes and show missing data
        return [None] * 10


# --- Architecture Section ---
# 1. Attention Mechanism (4 rows)
current_data_category = "architecture"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="attention">')
tbody_html.append('  <td rowspan="4" class="align-middle">Attention Mechanism</td>')
tbody_html.append('  <td></td>') # Sub-category placeholder
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(3): # Next 3 rows for Attention Mechanism
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="attention">')
    tbody_html.append('  <td></td>') # Sub-category placeholder
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# 2. Efficient Positional Encoding (4 rows)
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="posenc">') # Main subcat is posenc for first
tbody_html.append('  <td rowspan="4" class="align-middle">Efficient Positional Encoding</td>')
tbody_html.append('  <td></td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(3): # Next 3 rows, subcat changes to 'poe'
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="poe">')
    tbody_html.append('  <td></td>')
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# 3. MoE Mechanism (4 rows)
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="moe">')
tbody_html.append('  <td rowspan="4" class="align-middle">MoE Mechanism</td>')
tbody_html.append('  <td></td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(3):
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="moe">')
    tbody_html.append('  <td></td>')
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# 4. Attention-free Mechanism (4 rows)
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="attfree">')
tbody_html.append('  <td rowspan="4" class="align-middle">Attention-free Mechanism</td>')
tbody_html.append('  <td></td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(3):
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="attfree">')
    tbody_html.append('  <td></td>')
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# --- Training and Tuning Section ---
current_data_category = "training"
# Overall category cell
training_tuning_main_category_cell = '  <td rowspan="21" class="align-middle">Training and Tuning</td>'

# Sub-category: 1B-3B (7 rows)
sub_cat_name = "1B-3B"
sub_cat_slug = "1-3b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
tbody_html.append(training_tuning_main_category_cell) # Add main category cell only for the very first row of this large group
tbody_html.append(f'  <td rowspan="7" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(6): # Next 6 rows for 1B-3B
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    # No main cat cell, no sub cat cell due to rowspans
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# Sub-category: 7B-8B (7 rows)
sub_cat_name = "7B-8B"
sub_cat_slug = "7-8b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
# No main cat cell
tbody_html.append(f'  <td rowspan="7" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(6): 
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# Sub-category: 14B-24B (7 rows)
sub_cat_name = "14B-24B"
sub_cat_slug = "14-24b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
# No main cat cell
tbody_html.append(f'  <td rowspan="7" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
tbody_html.append("</tr>")
for _ in range(6):
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    tbody_html.append(generate_row_html(get_next_data_row(), current_data_category))
    tbody_html.append("</tr>")

# --- Inference Section (Quantification) ---
current_data_category = "inference"
section_type_hint = "inference_quant" # Special styling for quantification
# Overall category cell
quantification_main_category_cell = '  <td rowspan="9" class="align-middle">Quantification</td>'

# Sub-category: 1.5B-3.8B (3 rows)
sub_cat_name = "1.5B-3.8B"
sub_cat_slug = "1.5-3.8b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
tbody_html.append(quantification_main_category_cell) # Add main category cell
tbody_html.append(f'  <td rowspan="3" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
tbody_html.append("</tr>")
for _ in range(2): # Next 2 rows
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
    tbody_html.append("</tr>")

# Sub-category: 7B-8B (3 rows)
sub_cat_name = "7B-8B"
sub_cat_slug = "7-8b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
tbody_html.append(f'  <td rowspan="3" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
tbody_html.append("</tr>")
for _ in range(2):
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
    tbody_html.append("</tr>")

# Sub-category: 14B-34B (3 rows)
sub_cat_name = "14B-34B"
sub_cat_slug = "14-34b"
tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
tbody_html.append(f'  <td rowspan="3" class="align-middle">{sub_cat_name}</td>')
tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
tbody_html.append("</tr>")
for _ in range(2):
    tbody_html.append(f'<tr data-category="{current_data_category}" data-subcategory="{sub_cat_slug}">')
    tbody_html.append(generate_row_html(get_next_data_row(), section_type_hint))
    tbody_html.append("</tr>")

tbody_html.append("</tbody>")

# Print the final HTML to be captured
final_html_output = "\n".join(tbody_html)
print(final_html_output) 