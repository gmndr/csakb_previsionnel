import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import storage

def generate_exports(section_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename_base = f"{section_name.replace(' ', '_')}_{timestamp}"

    xlsx_path = os.path.join('exports', f"{filename_base}.xlsx")
    pdf_path = os.path.join('exports', f"{filename_base}.pdf")

    # --- XLSX Generation ---
    with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
        for theme_id in range(1, 5):
            response = storage.get_response(section_name, theme_id)

            sheet_name = f"Theme {theme_id}"
            if theme_id == 1: sheet_name = "Budget"
            elif theme_id == 2: sheet_name = "Bureau"
            elif theme_id == 3: sheet_name = "Formation"
            elif theme_id == 4: sheet_name = "Salaries"

            if response:
                data = response['data']
                # On récupère le template correspondant à la version sauvegardée
                template = storage.get_template(theme_id, version=response['template_version'])

                rows = []
                if template['structure']['type'] == 'budget':
                    for group in template['structure']['groups']:
                        rows.append([group['title'], ""])
                        for field in group['fields']:
                            rows.append([field['label'], data.get(field['id'], '')])
                        rows.append(["", ""])

                elif template['structure']['type'] == 'fixed_table':
                    header = ["Poste"] + template['structure']['cols']
                    rows.append(header)
                    for r_def in template['structure']['rows']:
                        row = [r_def['label']]
                        for col in template['structure']['cols']:
                            key = f"{r_def['id']}_{col.lower()}"
                            row.append(data.get(key, ''))
                        rows.append(row)

                elif template['structure']['type'] == 'dynamic_table':
                    header = [col['label'] for col in template['structure']['cols']]
                    rows.append(header)
                    for r_data in data.get('rows', []):
                        row = [r_data.get(col['id'], '') for col in template['structure']['cols']]
                        rows.append(row)

                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
            else:
                pd.DataFrame([["Aucune donnée saisie"]]).to_excel(writer, sheet_name=sheet_name, index=False, header=False)

    # --- PDF Generation ---
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for theme_id in range(1, 5):
        pdf.add_page()
        pdf.set_font("helvetica", 'B', 16)
        pdf.set_text_color(0, 35, 102) # Royal Blue

        title = f"Theme {theme_id}"
        if theme_id == 1: title = "Budget prévisionnel"
        elif theme_id == 2: title = "Bureau directeur"
        elif theme_id == 3: title = "Diplômes et plan de formation"
        elif theme_id == 4: title = "Salariés"

        pdf.cell(0, 10, f"{section_name} - {title}", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)

        pdf.set_font("helvetica", '', 12)
        pdf.set_text_color(0, 0, 0)

        response = storage.get_response(section_name, theme_id)

        if response:
            data = response['data']
            template = storage.get_template(theme_id, version=response['template_version'])

            if template['structure']['type'] == 'budget':
                for group in template['structure']['groups']:
                    pdf.set_font("helvetica", 'B', 13)
                    pdf.cell(0, 10, group['title'], new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font("helvetica", '', 11)
                    for field in group['fields']:
                        val = str(data.get(field['id'], ''))
                        pdf.multi_cell(0, 8, f"{field['label']} : {val}")
                    pdf.ln(5)

            else:
                if template['structure']['type'] == 'fixed_table':
                    for r_def in template['structure']['rows']:
                        pdf.set_font("helvetica", 'B', 11)
                        pdf.cell(0, 8, r_def['label'], new_x="LMARGIN", new_y="NEXT")
                        pdf.set_font("helvetica", '', 11)
                        for col in template['structure']['cols']:
                            key = f"{r_def['id']}_{col.lower()}"
                            pdf.cell(50, 8, f"  {col}:", border=0)
                            pdf.cell(0, 8, str(data.get(key, '')), new_x="LMARGIN", new_y="NEXT")

                elif template['structure']['type'] == 'dynamic_table':
                    for i, r_data in enumerate(data.get('rows', [])):
                        pdf.set_font("helvetica", 'B', 11)
                        pdf.cell(0, 8, f"Ligne {i+1}", new_x="LMARGIN", new_y="NEXT")
                        pdf.set_font("helvetica", '', 11)
                        for col in template['structure']['cols']:
                            val = str(r_data.get(col['id'], ''))
                            pdf.cell(60, 8, f"  {col['label']}:", border=0)
                            pdf.cell(0, 8, val, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.cell(0, 10, "Aucune donnée saisie pour ce formulaire.", new_x="LMARGIN", new_y="NEXT")

    pdf.output(pdf_path)

    return xlsx_path, pdf_path
