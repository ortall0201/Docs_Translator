import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors
frontend_color = '#61DAFB'  # React blue
backend_color = '#FF6B6B'   # FastAPI red
crewai_color = '#4ECDC4'    # Teal
storage_color = '#FFE66D'   # Yellow

# Title
ax.text(5, 11.5, 'Document Translator Flow', fontsize=20, fontweight='bold', ha='center')

# Frontend Section
frontend_box = FancyBboxPatch((0.5, 8.5), 3, 2.5, boxstyle="round,pad=0.1", 
                              facecolor=frontend_color, edgecolor='black', linewidth=2)
ax.add_patch(frontend_box)
ax.text(2, 10.5, 'FRONTEND', fontsize=14, fontweight='bold', ha='center')
ax.text(2, 10, 'React App', fontsize=10, ha='center')
ax.text(2, 9.7, '• UploadForm.js', fontsize=9, ha='center')
ax.text(2, 9.4, '• TranslateForm.js', fontsize=9, ha='center')
ax.text(2, 9.1, '• App.js', fontsize=9, ha='center')

# Backend Section
backend_box = FancyBboxPatch((6, 8.5), 3, 2.5, boxstyle="round,pad=0.1", 
                             facecolor=backend_color, edgecolor='black', linewidth=2)
ax.add_patch(backend_box)
ax.text(7.5, 10.5, 'BACKEND', fontsize=14, fontweight='bold', ha='center')
ax.text(7.5, 10, 'FastAPI Server', fontsize=10, ha='center')
ax.text(7.5, 9.7, '• /upload endpoint', fontsize=9, ha='center')
ax.text(7.5, 9.4, '• /translate endpoint', fontsize=9, ha='center')
ax.text(7.5, 9.1, '• /download endpoint', fontsize=9, ha='center')

# CrewAI Section
crewai_box = FancyBboxPatch((3.5, 5.5), 3, 2, boxstyle="round,pad=0.1", 
                            facecolor=crewai_color, edgecolor='black', linewidth=2)
ax.add_patch(crewai_box)
ax.text(5, 7.2, 'CrewAI Agents', fontsize=14, fontweight='bold', ha='center')
ax.text(5, 6.8, 'FormTranslatorAgent', fontsize=10, ha='center')
ax.text(5, 6.5, 'ResponseBackTranslatorAgent', fontsize=10, ha='center')
ax.text(5, 6.2, 'GPT-4 Integration', fontsize=9, ha='center', style='italic')

# Storage Section
storage_box = FancyBboxPatch((6, 2.5), 3, 2, boxstyle="round,pad=0.1", 
                             facecolor=storage_color, edgecolor='black', linewidth=2)
ax.add_patch(storage_box)
ax.text(7.5, 3.8, 'FILE STORAGE', fontsize=14, fontweight='bold', ha='center')
ax.text(7.5, 3.4, 'uploads/', fontsize=10, ha='center')
ax.text(7.5, 3.1, 'outputs/', fontsize=10, ha='center')

# Tools Section
tools_box = FancyBboxPatch((0.5, 5.5), 2.5, 2, boxstyle="round,pad=0.1", 
                           facecolor='#DDA0DD', edgecolor='black', linewidth=2)
ax.add_patch(tools_box)
ax.text(1.75, 7, 'AI Tools', fontsize=12, fontweight='bold', ha='center')
ax.text(1.75, 6.6, 'TranslationTool', fontsize=9, ha='center')
ax.text(1.75, 6.3, 'AnnotationTool', fontsize=9, ha='center')

# Flow arrows and labels
# 1. Upload flow
arrow1 = ConnectionPatch((3.5, 9.8), (6, 9.8), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="blue")
ax.add_artist(arrow1)
ax.text(4.75, 10, '1. POST /upload', fontsize=9, ha='center', bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 2. File storage
arrow2 = ConnectionPatch((7.5, 8.5), (7.5, 4.5), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="red")
ax.add_artist(arrow2)
ax.text(8.2, 6.5, '2. Save file\nto uploads/', fontsize=9, ha='left', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 3. Translation request
arrow3 = ConnectionPatch((3.5, 9.2), (6, 9.2), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="green")
ax.add_artist(arrow3)
ax.text(4.75, 9.4, '3. POST /translate', fontsize=9, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 4. CrewAI processing
arrow4 = ConnectionPatch((7.2, 8.5), (5.8, 7.5), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="purple")
ax.add_artist(arrow4)
ax.text(6.8, 8, '4. run_crew()', fontsize=9, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 5. Tools usage
arrow5 = ConnectionPatch((3, 6.5), (3.5, 6.5), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="orange")
ax.add_artist(arrow5)
ax.text(3.25, 6.8, '5. Use\ntools', fontsize=8, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 6. Save translated file
arrow6 = ConnectionPatch((6.2, 6.2), (7.2, 4.5), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="brown")
ax.add_artist(arrow6)
ax.text(6.2, 5.2, '6. Save to\noutputs/', fontsize=9, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 7. Download link
arrow7 = ConnectionPatch((6, 8.8), (3.5, 8.8), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="darkgreen")
ax.add_artist(arrow7)
ax.text(4.75, 8.6, '7. Return filename', fontsize=9, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# 8. Download request
arrow8 = ConnectionPatch((3.5, 8.6), (6, 8.6), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc="navy")
ax.add_artist(arrow8)
ax.text(4.75, 8.4, '8. GET /download', fontsize=9, ha='center', 
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))

# Process steps text
ax.text(0.5, 1.5, 'Process Flow:', fontsize=14, fontweight='bold')
steps = [
    '1. User uploads PDF file via React frontend',
    '2. FastAPI saves file to uploads/ directory', 
    '3. User selects language and requests translation',
    '4. Backend extracts PDF text and calls CrewAI',
    '5. AI agents use translation/annotation tools',
    '6. Translated content saved to outputs/',
    '7. Frontend receives translated filename',
    '8. User downloads via /download endpoint'
]

for i, step in enumerate(steps):
    ax.text(0.5, 1.2 - i*0.15, step, fontsize=9, ha='left')

# Legend
ax.text(8.5, 1.5, 'Components:', fontsize=12, fontweight='bold')
legend_items = [
    ('React Frontend', frontend_color),
    ('FastAPI Backend', backend_color),
    ('CrewAI Agents', crewai_color),
    ('File Storage', storage_color)
]

for i, (label, color) in enumerate(legend_items):
    rect = patches.Rectangle((8.5, 1.1 - i*0.2), 0.2, 0.15, facecolor=color, edgecolor='black')
    ax.add_patch(rect)
    ax.text(8.8, 1.17 - i*0.2, label, fontsize=10, va='center')

plt.tight_layout()
plt.savefig('C:\\Users\\user\\Desktop\\Docs_Translator\\flow_diagram.png', dpi=300, bbox_inches='tight')
plt.show()