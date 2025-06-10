"""
Rebol Script Analyzer - Comprehensive analysis tool for Rebol 3 scripts
"""

import re
from typing import Dict, List, Any, Tuple
from collections import defaultdict

class RebolScriptAnalyzer:
    """Comprehensive analyzer for Rebol 3 scripts with focus on code quality and best practices."""
    
    def __init__(self):
        """Initialize the analyzer with pattern definitions and quality metrics."""
        self.function_pattern = re.compile(r'(\w+):\s*function\s*\[', re.MULTILINE)
        self.example_pattern = re.compile(r'example-(\d+):\s*function', re.MULTILINE)
        self.comment_pattern = re.compile(r';;.*$|;.*$', re.MULTILINE)
        self.string_pattern = re.compile(r'"[^"]*"|\{[^}]*\}', re.DOTALL)
        self.check_usage_pattern = re.compile(r'\bcheck\s+', re.MULTILINE)
        self.error_handling_pattern = re.compile(r'\btry\s*\[|\berror\?', re.MULTILINE)
        
    def analyze_script(self, script_content: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of the Rebol script.
        
        Args:
            script_content: The complete Rebol script content
            
        Returns:
            Dictionary containing detailed analysis results
        """
        analysis = {
            'overview': self._analyze_overview(script_content),
            'structure': self._analyze_structure(script_content),
            'functions': self._analyze_functions(script_content),
            'examples': self._analyze_examples(script_content),
            'documentation': self._analyze_documentation(script_content),
            'code_quality': self._analyze_code_quality(script_content),
            'best_practices': self._analyze_best_practices(script_content),
            'recommendations': self._generate_recommendations(script_content),
            'performance': self._analyze_performance(script_content),
            'educational_value': self._assess_educational_value(script_content)
        }
        
        return analysis
    
    def _analyze_overview(self, content: str) -> Dict[str, Any]:
        """Analyze script overview and metadata."""
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith(';')])
        comment_lines = len([line for line in lines if line.strip().startswith(';')])
        blank_lines = total_lines - code_lines - comment_lines
        
        # Extract header information
        header_match = re.search(r'REBOL\s*\[(.*?)\]', content, re.DOTALL)
        header_info = {}
        if header_match:
            header_content = header_match.group(1)
            for line in header_content.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    header_info[key.strip()] = value.strip().strip('"')
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'comment_ratio': round(comment_lines / total_lines * 100, 1) if total_lines > 0 else 0,
            'header_info': header_info,
            'script_sections': self._identify_sections(content)
        }
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze script structure and organization."""
        sections = []
        current_section = None
        
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line.startswith(';;='):
                if 'UNDERSTANDING' in line:
                    current_section = 'theory'
                elif 'HELPER' in line:
                    current_section = 'helpers'
                elif 'EXAMPLE' in line:
                    current_section = 'examples'
                sections.append({
                    'type': current_section,
                    'line': line_num,
                    'title': line
                })
        
        functions = self.function_pattern.findall(content)
        examples = self.example_pattern.findall(content)
        
        return {
            'sections': sections,
            'total_functions': len(functions),
            'example_functions': len(examples),
            'helper_functions': len([f for f in functions if not f.startswith('example-')]),
            'structure_quality': self._assess_structure_quality(content),
            'organization_score': self._calculate_organization_score(content)
        }
    
    def _analyze_functions(self, content: str) -> Dict[str, Any]:
        """Analyze all functions in the script."""
        functions = []
        function_blocks = re.finditer(r'(\w+):\s*function\s*\[(.*?)\]\s*\[(.*?)\n\]', content, re.DOTALL)
        
        for match in function_blocks:
            func_name = match.group(1)
            func_params = match.group(2).strip()
            func_body_start = match.end()
            
            # Find function body (simplified - would need more complex parsing for real Rebol)
            func_info = {
                'name': func_name,
                'parameters': func_params,
                'is_example': func_name.startswith('example-'),
                'has_documentation': bool(re.search(rf'{func_name}.*?".*?"', content)),
                'uses_check': 'check' in match.group(0),
                'has_error_handling': bool(re.search(r'try\s*\[|error\?', match.group(0))),
                'complexity': self._calculate_function_complexity(match.group(0))
            }
            functions.append(func_info)
        
        return {
            'functions': functions,
            'average_complexity': sum(f['complexity'] for f in functions) / len(functions) if functions else 0,
            'documented_functions': len([f for f in functions if f['has_documentation']]),
            'functions_with_error_handling': len([f for f in functions if f['has_error_handling']])
        }
    
    def _analyze_examples(self, content: str) -> Dict[str, Any]:
        """Analyze the example functions in detail."""
        examples = []
        example_matches = list(self.example_pattern.finditer(content))
        
        for i, match in enumerate(example_matches):
            example_num = match.group(1)
            start_pos = match.start()
            
            # Find the end of this example (start of next example or end of file)
            if i < len(example_matches) - 1:
                end_pos = example_matches[i + 1].start()
            else:
                end_pos = len(content)
            
            example_content = content[start_pos:end_pos]
            
            example_info = {
                'number': example_num,
                'title': self._extract_example_title(example_content),
                'description': self._extract_example_description(example_content),
                'uses_check': 'check' in example_content,
                'uses_validate_series': 'validate-series' in example_content,
                'has_error_handling': bool(re.search(r'try\s*\[|error\?', example_content)),
                'complexity': self._calculate_function_complexity(example_content),
                'educational_elements': self._identify_educational_elements(example_content),
                'code_quality': self._assess_example_quality(example_content)
            }
            examples.append(example_info)
        
        return {
            'examples': examples,
            'total_examples': len(examples),
            'examples_with_error_handling': len([e for e in examples if e['has_error_handling']]),
            'average_complexity': sum(e['complexity'] for e in examples) / len(examples) if examples else 0,
            'coverage_analysis': self._analyze_example_coverage(examples)
        }
    
    def _analyze_documentation(self, content: str) -> Dict[str, Any]:
        """Analyze documentation quality and completeness."""
        # Count different types of comments
        doc_strings = re.findall(r'\{[^}]*\}', content, re.DOTALL)
        inline_comments = re.findall(r';[^;].*$', content, re.MULTILINE)
        section_headers = re.findall(r';;=.*$', content, re.MULTILINE)
        
        # Analyze documentation completeness
        functions = self.function_pattern.findall(content)
        documented_functions = 0
        
        for func in functions:
            # Check if function has documentation string
            func_pattern = rf'{func}:\s*function.*?\{{.*?\}}'
            if re.search(func_pattern, content, re.DOTALL):
                documented_functions += 1
        
        return {
            'doc_strings': len(doc_strings),
            'inline_comments': len(inline_comments),
            'section_headers': len(section_headers),
            'documentation_ratio': round(documented_functions / len(functions) * 100, 1) if functions else 0,
            'has_comprehensive_guide': 'COMPREHENSIVE GUIDE' in content,
            'has_best_practices': 'BEST PRACTICES' in content,
            'has_examples_explanation': 'WHAT IS THE' in content,
            'documentation_quality': self._assess_documentation_quality(content)
        }
    
    def _analyze_code_quality(self, content: str) -> Dict[str, Any]:
        """Analyze overall code quality metrics."""
        issues = []
        warnings = []
        strengths = []
        
        # Check for consistent naming
        function_names = self.function_pattern.findall(content)
        if all('-' in name or name.startswith('example') for name in function_names):
            strengths.append("Consistent kebab-case naming convention")
        else:
            issues.append("Inconsistent function naming convention")
        
        # Check error handling
        check_usages = len(self.check_usage_pattern.findall(content))
        error_handlers = len(self.error_handling_pattern.findall(content))
        
        if error_handlers >= check_usages * 0.8:
            strengths.append("Good error handling coverage")
        else:
            warnings.append("Some check operations lack proper error handling")
        
        # Check for magic numbers or strings
        if re.search(r'\b\d{3,}\b', content):
            warnings.append("Consider defining constants for large numbers")
        
        # Check function length
        long_functions = []
        for match in re.finditer(r'(\w+):\s*function.*?(?=\w+:\s*function|\Z)', content, re.DOTALL):
            func_name = match.group(1)
            func_content = match.group(0)
            line_count = len(func_content.split('\n'))
            if line_count > 50:
                long_functions.append(func_name)
        
        if long_functions:
            warnings.append(f"Long functions detected: {', '.join(long_functions)}")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'strengths': strengths,
            'quality_score': self._calculate_quality_score(issues, warnings, strengths),
            'maintainability': self._assess_maintainability(content)
        }
    
    def _analyze_best_practices(self, content: str) -> Dict[str, Any]:
        """Analyze adherence to Rebol and general programming best practices."""
        practices = {
            'good_practices': [],
            'violations': [],
            'suggestions': []
        }
        
        # Check for comprehensive error handling
        if 'try [' in content and 'error?' in content:
            practices['good_practices'].append("Proper error handling with try/error pattern")
        
        # Check for helper function usage
        if 'validate-series' in content:
            practices['good_practices'].append("Good use of helper functions to reduce code duplication")
        
        # Check for performance considerations
        if 'performance' in content.lower() or 'timing' in content.lower():
            practices['good_practices'].append("Performance awareness demonstrated")
        
        # Check for educational structure
        if re.search(r'print.*"---.*Example \d+:', content):
            practices['good_practices'].append("Clear example organization and labeling")
        
        # Check for documentation strings
        doc_string_count = len(re.findall(r'\{[^}]*Parameters:.*?\}', content, re.DOTALL | re.IGNORECASE))
        if doc_string_count > 5:
            practices['good_practices'].append("Comprehensive function documentation with parameters")
        
        # Check for potential improvements
        if 'print reform' in content:
            practices['suggestions'].append("Consider using more modern string formatting approaches")
        
        return practices
    
    def _analyze_performance(self, content: str) -> Dict[str, Any]:
        """Analyze performance considerations and implications."""
        performance_issues = []
        optimizations = []
        considerations = []
        
        # Check for performance-critical patterns
        if 'repeat i 1000' in content:
            considerations.append("Large loop operations present - check function impact measured")
        
        # Check for string concatenation in loops
        if re.search(r'repeat.*append.*string', content, re.DOTALL):
            performance_issues.append("String concatenation in loops - consider using join or collect")
        
        # Check for timing measurements
        if 'now/precise' in content:
            optimizations.append("Performance timing measurements implemented")
        
        # Check for large data handling
        if 'large-string' in content or 'large' in content:
            considerations.append("Large data set handling demonstrated")
        
        return {
            'performance_issues': performance_issues,
            'optimizations': optimizations,
            'considerations': considerations,
            'performance_awareness': len(optimizations) > 0
        }
    
    def _assess_educational_value(self, content: str) -> Dict[str, Any]:
        """Assess the educational value and learning potential of the script."""
        educational_elements = []
        learning_progression = []
        gaps = []
        
        # Check for progressive complexity
        examples = self.example_pattern.findall(content)
        if len(examples) >= 20:
            educational_elements.append("Comprehensive set of examples (25+ examples)")
        
        # Check for explanatory content
        if 'WHAT IS THE' in content and 'WHY USE' in content:
            educational_elements.append("Clear conceptual explanations")
        
        # Check for best practices section
        if 'BEST PRACTICES' in content:
            educational_elements.append("Best practices guidance included")
        
        # Check for common mistakes section
        if 'COMMON MISTAKES' in content:
            educational_elements.append("Common pitfalls and mistakes addressed")
        
        # Analyze example progression
        basic_examples = ['string', 'block', 'binary']
        advanced_examples = ['nested', 'large', 'performance']
        
        has_basic = any(example in content.lower() for example in basic_examples)
        has_advanced = any(example in content.lower() for example in advanced_examples)
        
        if has_basic and has_advanced:
            learning_progression.append("Good progression from basic to advanced concepts")
        elif has_basic:
            gaps.append("Could benefit from more advanced examples")
        
        return {
            'educational_elements': educational_elements,
            'learning_progression': learning_progression,
            'gaps': gaps,
            'teaching_quality': len(educational_elements) + len(learning_progression),
            'beginner_friendly': 'novice' in content.lower() or 'beginner' in content.lower()
        }
    
    def _generate_recommendations(self, content: str) -> List[Dict[str, str]]:
        """Generate specific recommendations for improvement."""
        recommendations = []
        
        # Code structure recommendations
        if content.count('validate-series') < 10:
            recommendations.append({
                'category': 'Code Structure',
                'priority': 'Medium',
                'recommendation': 'Consider creating additional helper functions to reduce code duplication in example functions'
            })
        
        # Documentation recommendations
        doc_strings = len(re.findall(r'\{[^}]*\}', content, re.DOTALL))
        functions = len(self.function_pattern.findall(content))
        if doc_strings < functions * 0.8:
            recommendations.append({
                'category': 'Documentation',
                'priority': 'High',
                'recommendation': 'Add comprehensive documentation strings to all functions, including parameters and return values'
            })
        
        # Error handling recommendations
        check_usages = len(self.check_usage_pattern.findall(content))
        try_blocks = len(re.findall(r'try\s*\[', content))
        if try_blocks < check_usages * 0.9:
            recommendations.append({
                'category': 'Error Handling',
                'priority': 'High',
                'recommendation': 'Ensure all check function calls are wrapped in proper error handling'
            })
        
        # Performance recommendations
        if 'performance' in content.lower():
            recommendations.append({
                'category': 'Performance',
                'priority': 'Low',
                'recommendation': 'Consider adding more performance benchmarks and optimization examples'
            })
        
        # Educational recommendations
        if 'production' in content:
            recommendations.append({
                'category': 'Educational',
                'priority': 'Medium',
                'recommendation': 'Add examples showing when NOT to use check function in production code'
            })
        
        return recommendations
    
    # Helper methods for analysis
    def _identify_sections(self, content: str) -> List[str]:
        """Identify major sections in the script."""
        sections = []
        for line in content.split('\n'):
            if line.strip().startswith(';;='):
                sections.append(line.strip())
        return sections
    
    def _assess_structure_quality(self, content: str) -> str:
        """Assess the overall structure quality."""
        sections = self._identify_sections(content)
        if len(sections) >= 3:
            return "Excellent - Well organized with clear sections"
        elif len(sections) >= 2:
            return "Good - Has some organization"
        else:
            return "Poor - Lacks clear organization"
    
    def _calculate_organization_score(self, content: str) -> int:
        """Calculate organization score out of 100."""
        score = 0
        
        # Section headers (+30)
        if ';;=' in content:
            score += 30
        
        # Helper functions (+20)
        if 'validate-series' in content:
            score += 20
        
        # Consistent naming (+20)
        functions = self.function_pattern.findall(content)
        if functions and all('-' in f or f.startswith('example') for f in functions):
            score += 20
        
        # Documentation (+30)
        if '{' in content and 'Parameters:' in content:
            score += 30
        
        return min(score, 100)
    
    def _calculate_function_complexity(self, func_content: str) -> int:
        """Calculate function complexity based on various metrics."""
        complexity = 1  # Base complexity
        
        # Add complexity for control structures
        complexity += len(re.findall(r'\b(if|either|repeat|foreach|while)\b', func_content))
        complexity += len(re.findall(r'\btry\s*\[', func_content))
        complexity += len(re.findall(r'\berror\?', func_content))
        
        return complexity
    
    def _extract_example_title(self, example_content: str) -> str:
        """Extract the title from an example function."""
        match = re.search(r'"([^"]*)"', example_content)
        return match.group(1) if match else "No title found"
    
    def _extract_example_description(self, example_content: str) -> str:
        """Extract the description from an example function."""
        match = re.search(r'\{([^}]*)\}', example_content, re.DOTALL)
        if match:
            desc = match.group(1).strip()
            return desc[:200] + '...' if len(desc) > 200 else desc
        return "No description found"
    
    def _identify_educational_elements(self, example_content: str) -> List[str]:
        """Identify educational elements in an example."""
        elements = []
        
        if 'print' in example_content:
            elements.append("Interactive output")
        if 'try [' in example_content:
            elements.append("Error handling demonstration")
        if 'validate-series' in example_content:
            elements.append("Helper function usage")
        if re.search(r'print.*"---', example_content):
            elements.append("Clear section labeling")
        
        return elements
    
    def _assess_example_quality(self, example_content: str) -> str:
        """Assess the quality of an individual example."""
        score = 0
        
        if 'try [' in example_content:
            score += 2
        if 'validate-series' in example_content:
            score += 2
        if re.search(r'\{[^}]*Parameters:.*?\}', example_content, re.DOTALL):
            score += 2
        if 'print' in example_content:
            score += 1
        
        if score >= 6:
            return "Excellent"
        elif score >= 4:
            return "Good"
        elif score >= 2:
            return "Fair"
        else:
            return "Needs improvement"
    
    def _analyze_example_coverage(self, examples: List[Dict]) -> Dict[str, Any]:
        """Analyze what concepts the examples cover."""
        coverage = {
            'basic_types': 0,
            'advanced_operations': 0,
            'error_handling': 0,
            'performance': 0,
            'edge_cases': 0
        }
        
        for example in examples:
            title = example.get('title', '').lower()
            
            if any(t in title for t in ['string', 'block', 'binary']):
                coverage['basic_types'] += 1
            if any(t in title for t in ['nested', 'modification', 'insertion']):
                coverage['advanced_operations'] += 1
            if example.get('has_error_handling'):
                coverage['error_handling'] += 1
            if 'performance' in title or 'large' in title:
                coverage['performance'] += 1
            if 'empty' in title or 'edge' in title:
                coverage['edge_cases'] += 1
        
        return coverage
    
    def _assess_documentation_quality(self, content: str) -> str:
        """Assess overall documentation quality."""
        score = 0
        
        # Header documentation
        if 'REBOL [' in content and 'Purpose:' in content:
            score += 2
        
        # Section organization
        if content.count(';;=') >= 3:
            score += 2
        
        # Function documentation
        doc_strings = len(re.findall(r'\{[^}]*Parameters:.*?\}', content, re.DOTALL))
        if doc_strings > 10:
            score += 3
        elif doc_strings > 5:
            score += 2
        elif doc_strings > 0:
            score += 1
        
        # Educational content
        if 'WHAT IS THE' in content and 'WHY USE' in content:
            score += 2
        
        if score >= 8:
            return "Excellent - Comprehensive documentation"
        elif score >= 6:
            return "Good - Well documented"
        elif score >= 4:
            return "Fair - Basic documentation"
        else:
            return "Poor - Lacks adequate documentation"
    
    def _calculate_quality_score(self, issues: List, warnings: List, strengths: List) -> int:
        """Calculate overall quality score."""
        base_score = 70
        base_score -= len(issues) * 10
        base_score -= len(warnings) * 5
        base_score += len(strengths) * 5
        
        return max(0, min(100, base_score))
    
    def _assess_maintainability(self, content: str) -> str:
        """Assess code maintainability."""
        factors = []
        
        # Consistent naming
        functions = self.function_pattern.findall(content)
        if functions and all('-' in f or f.startswith('example') for f in functions):
            factors.append("Consistent naming")
        
        # Helper functions
        if 'validate-series' in content:
            factors.append("Good use of helper functions")
        
        # Documentation
        if '{' in content and 'Parameters:' in content:
            factors.append("Well documented")
        
        # Error handling
        if 'try [' in content and 'error?' in content:
            factors.append("Robust error handling")
        
        score = len(factors)
        if score >= 3:
            return "High maintainability"
        elif score >= 2:
            return "Moderate maintainability"
        else:
            return "Low maintainability"
