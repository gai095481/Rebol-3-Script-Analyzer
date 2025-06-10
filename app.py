#!/usr/bin/env python3
"""
Rebol 3 Script Analysis Tool
A comprehensive tool for analyzing and reviewing Rebol 3 scripts with detailed feedback.
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import re
from analyzer import RebolScriptAnalyzer

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'rebol-analyzer-secret-key-2025')

@app.route('/')
def index():
    """Main page for uploading and analyzing Rebol scripts."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_script():
    """Analyze the uploaded Rebol script and provide comprehensive feedback."""
    try:
        # Check if script content was provided
        script_content = request.form.get('script_content', '').strip()
        
        if not script_content:
            flash('Please provide Rebol script content to analyze.', 'error')
            return redirect(url_for('index'))
        
        # Initialize the analyzer
        analyzer = RebolScriptAnalyzer()
        
        # Perform comprehensive analysis
        analysis_results = analyzer.analyze_script(script_content)
        
        return render_template('analysis.html', 
                             analysis=analysis_results,
                             script_content=script_content)
        
    except Exception as e:
        flash(f'Error analyzing script: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for script analysis."""
    try:
        data = request.get_json()
        if not data or 'script_content' not in data:
            return jsonify({'error': 'No script content provided'}), 400
        
        analyzer = RebolScriptAnalyzer()
        results = analyzer.analyze_script(data['script_content'])
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
