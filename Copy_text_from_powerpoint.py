import os
import sys
from pptx import Presentation
# pip install python-pptx


def extract_text_from_pptx_file(file_path):
    prs = Presentation(file_path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return '\n'.join(text)

def extract_text_from_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.pptx'):
                file_path = os.path.join(root, file_name)
                text = extract_text_from_pptx_file(file_path)
                # Create a text file with the same name as the PowerPoint file
                text_file_path = os.path.splitext(file_path)[0] + '.txt'
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)

# folder_path = r'C:\Users\Lenovo\OneDrive - Solent University\Documents\724 AI in Business (Friday)\Lesson 1\'
folder_path = r'C:\Users\Lenovo\OneDrive - Solent University\Documents\725 Analytics Visualisation (Tue)'
extract_text_from_folder(folder_path)

