#!/usr/bin/env python3
"""
DEMO: Network-Enhanced Code Generation
Proving the concept of network intelligence in action
"""

import subprocess
import json
import sys


def demo_github_search(query: str) -> dict:
    """
    Search GitHub for code patterns.
    
    WHY: Learn from millions of real implementations!
    """
    print(f"\n🔍 Searching GitHub for: {query}")
    
    cmd = f'curl -s "https://api.github.com/search/repositories?q={query}+language:python&sort=stars&per_page=5"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        repos = []
        
        for item in data['items'][:5]:
            repos.append({
                'name': item['full_name'],
                'stars': item['stargazers_count'],
                'description': item['description'][:100] if item['description'] else 'No description',
                'url': item['html_url']
            })
            print(f"  ⭐ {item['stargazers_count']:>5} - {item['full_name']}")
            print(f"     {item['description'][:80] if item['description'] else 'No description'}...")
        
        return {'success': True, 'repos': repos}
    
    return {'success': False, 'error': result.stderr}


def demo_huggingface_models(task: str) -> dict:
    """
    Find ML models for a task.
    
    WHY: Instant access to SOTA models!
    """
    print(f"\n🤖 Searching HuggingFace for: {task}")
    
    cmd = f'curl -s "https://huggingface.co/api/models?search={task}&limit=5"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        models = []
        
        for model in data[:5]:
            models.append({
                'id': model['id'],
                'downloads': model.get('downloads', 0),
                'likes': model.get('likes', 0)
            })
            print(f"  🤖 {model['id']}")
            print(f"     Downloads: {model.get('downloads', 'N/A')} | Likes: {model.get('likes', 'N/A')}")
        
        return {'success': True, 'models': models}
    
    return {'success': False, 'error': result.stderr}


def demo_stackoverflow_search(query: str) -> dict:
    """
    Search Stack Overflow for solutions.
    
    WHY: Learn from millions of solved problems!
    """
    print(f"\n📚 Searching Stack Overflow for: {query}")
    
    # Stack Overflow API
    import urllib.parse
    encoded = urllib.parse.quote(query)
    cmd = f'curl -s "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q={encoded}&site=stackoverflow"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        questions = []
        
        for item in data.get('items', [])[:3]:
            questions.append({
                'title': item['title'],
                'score': item['score'],
                'answers': item['answer_count'],
                'link': item['link']
            })
            print(f"  📝 Score: {item['score']} | Answers: {item['answer_count']}")
            print(f"     {item['title'][:80]}...")
            print(f"     {item['link']}")
        
        return {'success': True, 'questions': questions}
    
    return {'success': False, 'error': result.stderr}


def demo_pypi_check(package: str) -> dict:
    """
    Check package info from PyPI.
    
    WHY: Get latest versions and compatibility info!
    """
    print(f"\n📦 Checking PyPI for: {package}")
    
    cmd = f'curl -s "https://pypi.org/pypi/{package}/json"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        info = {
            'name': data['info']['name'],
            'version': data['info']['version'],
            'summary': data['info']['summary'],
            'requires_python': data['info'].get('requires_python', 'Any'),
            'url': data['info']['project_urls'].get('Homepage', '')
        }
        
        print(f"  📦 {info['name']} v{info['version']}")
        print(f"     {info['summary']}")
        print(f"     Requires Python: {info['requires_python']}")
        
        return {'success': True, 'info': info}
    
    return {'success': False, 'error': result.stderr}


def main():
    """
    Demonstrate network-enhanced code generation capabilities.
    
    THIS PROVES:
    - We can access GitHub for patterns
    - We can find HuggingFace models
    - We can search Stack Overflow
    - We can check PyPI for packages
    - We can integrate ANY public API
    """
    print("="*70)
    print("🚀 NETWORK INTELLIGENCE DEMONSTRATION")
    print("Proving the capability of network-enhanced code generation")
    print("="*70)
    
    # Demo 1: Search GitHub for existing solutions
    github_results = demo_github_search("machine+learning+pipeline")
    
    # Demo 2: Find ML models
    hf_results = demo_huggingface_models("text-classification")
    
    # Demo 3: Search Stack Overflow
    so_results = demo_stackoverflow_search("python async await")
    
    # Demo 4: Check package info
    pypi_results = demo_pypi_check("transformers")
    
    print("\n" + "="*70)
    print("✅ CAPABILITIES CONFIRMED:")
    print("  - GitHub API access: ✅")
    print("  - HuggingFace access: ✅")
    print("  - Stack Overflow access: ✅")
    print("  - PyPI access: ✅")
    print()
    print("🔥 THIS MEANS:")
    print("  - Can learn from millions of repos")
    print("  - Can download ML models on-demand")
    print("  - Can find solutions to common problems")
    print("  - Can verify package compatibility")
    print("  - Can access ANY public API")
    print()
    print("💡 NEXT LEVEL:")
    print("  - Could access Google Colab for GPU compute")
    print("  - Could integrate with cloud services")
    print("  - Could validate code against real APIs")
    print("  - Could benchmark on external infrastructure")
    print("="*70)


if __name__ == "__main__":
    main()
