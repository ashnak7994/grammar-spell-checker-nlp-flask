# app.py

from flask import Flask, render_template, request
from textblob import TextBlob
import language_tool_python

app = Flask(__name__)

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')

@app.route('/', methods=['GET', 'POST'])
def index():
    corrected_text = ""
    spelling_correction = ""
    grammar_suggestions = []
    
    if request.method == 'POST':
        user_input = request.form['text']
        
        # Step 1: Spelling Correction using TextBlob
        blob = TextBlob(user_input)
        spelling_correction = str(blob.correct())
        
        # Step 2: Grammar Checking using LanguageTool
        matches = tool.check(spelling_correction)
        corrected_text = language_tool_python.utils.correct(spelling_correction, matches)
        
        # For displaying errors and suggestions
        grammar_suggestions = [{"error": m.ruleId, "message": m.message, "context": m.context} for m in matches]
        
    return render_template('index.html', 
                           corrected_text=corrected_text, 
                           spelling_correction=spelling_correction, 
                           grammar_suggestions=grammar_suggestions)

if __name__ == '__main__':
    app.run(debug=True)
