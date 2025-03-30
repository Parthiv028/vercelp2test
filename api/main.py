

from fastapi import FastAPI, Form, UploadFile
from difflib import SequenceMatcher
import re


app=FastAPI()
nothardcoded = []
QUESTIONS = {
    1: "Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below. What is the output of code -s?"
}

ANSWERS = {
    1: """Version:          Code 1.96.2 (fabdb6a30b49f79a7aba0f2ad9df9b399473380f, 2024-12-19T10:22:47.216Z)
OS Version:       Darwin arm64 22.6.0
CPUs:             Apple M2 (8 x 2400)
Memory (System):  8.00GB (0.07GB free)
Load (avg):       3, 3, 3
VM:               0%
Screen Reader:    no
Process Argv:     --crash-reporter-id 92550e3a-19fb-4a01-b9a3-bb0fe8885f25
GPU Status:       2d_canvas:                              enabled
                  canvas_oop_rasterization:               enabled_on
                  direct_rendering_display_compositor:    disabled_off_ok
                  gpu_compositing:                        enabled
                  multiple_raster_threads:                enabled_on
                  opengl:                                 enabled_on
                  rasterization:                          enabled
                  raw_draw:                               disabled_off_ok
                  skia_graphite:                          disabled_off
                  video_decode:                           enabled
                  video_encode:                           enabled
                  webgl:                                  enabled
                  webgl2:                                 enabled
                  webgpu:                                 enabled
                  webnn:                                  disabled_off

CPU %   Mem MB     PID  Process
    0       98   16573  code main
   13       41   16578     gpu-process
    0       16   16579     utility-network-service
    4      147   16582  window [1] (Extension: Cody: AI Coding Assistant with Autocomplete & Chat — Untitled (Workspace))
    0       33   16591  shared-process
    0       25   16592  fileWatcher [1]
    1       41   16604  ptyHost
    0        0   16618       /bin/zsh -il
    0        0   16780       /bin/zsh -il
    0        0   16841       /bin/zsh -il
    0        0   18972         bash /usr/local/bin/code -s
    7       41   18981           electron-nodejs (cli.js )
    0        0   18867       /bin/zsh -i
    0        8   18989       (ps)
    1      123   16744  extensionHost [1]
    0       25   16747       /Users/ok/Desktop/Visual Studio Code.app/Contents/Frameworks/Code Helper (Plugin).app/Contents/MacOS/Code Helper (Plugin) /Users/ok/Desktop/Visual Studio Code.app/Contents/Resources/app/extensions/json-language-features/server/dist/node/jsonServerMain --node-ipc --clientProcessId=16744
    0        0   16752       /Users/ok/.vscode/extensions/ms-vscode.cpptools-1.22.11-darwin-arm64/bin/cpptools
    0        0   18866       /Users/ok/.vscode/extensions/ms-python.python-2024.22.2-darwin-arm64/python-env-tools/bin/pet server
    0       33   18887       electron-nodejs (bundle.js )
    1       49   18545     window
    0       82   18924     window

Workspace Stats: 
|  Window (Extension: Cody: AI Coding Assistant with Autocomplete & Chat — Untitled (Workspace))
|    Folder (TDS): 0 files
|      File types:
|      Conf files:
"""
}



def check_question_similarity(input_question: str):
    best_match = None
    highest_score = 0.0
    
    for q_number, stored_question in QUESTIONS.items():
        score = SequenceMatcher(None, input_question.lower(), stored_question.lower()).ratio() * 100
        if score > highest_score:
            highest_score = score
            best_match = q_number
    
    return best_match, highest_score

def get_answer(q_number: int, question: str = None):
        
       
    return ANSWERS.get(q_number, "Answer not found")


@app.post("/")
async def process_question(question: str = Form(...)):
    q_number, similarity_score = check_question_similarity(question)

    if similarity_score >= 50.0:
        answer = get_answer(q_number, question)
        if not isinstance(answer, str):
            answer = str(answer)
        return {"answer": answer, "similarity_score": similarity_score}
    else:
        return {"error": "Question not recognized", "similarity_score": similarity_score}

