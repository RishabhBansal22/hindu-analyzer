from scripts.gemini import Gemini
from scripts.scrapper import Scrapper
import json
from datetime import datetime
import os


def main(num_articles: int = 1):
    """
    Scrape articles and analyze them with Gemini, returning structured data
    """
    gemini = Gemini()
    scraper = Scrapper(url="https://www.thehindu.com/opinion/editorial/")

    try:
        output = scraper.scrape_articles(num_articles=num_articles)
        
        
        if output:
            
            output_dict = json.loads(output)
            
            # Create structured analysis results
            analysis_results = {
                "session_info": {
                    "timestamp": datetime.now().isoformat(),
                    "total_articles": len(output_dict["articles"]),
                    "analysis_status": "completed"
                },
                "articles_analysis": []
            }
            
            for idx, article in enumerate(output_dict["articles"], 1):
                print(f"Analyzing article {idx}/{len(output_dict['articles'])}...")
                
                # Get Gemini analysis
                gemini_analysis = gemini.gemini_response(user_prompt=article["content"])
                
                # Structure the article data
                article_analysis = {
                    "article_info": {
                        "number": idx,
                        "title": article.get("title", "Untitled"),
                        "url": article.get("url", ""),
                        "status": article.get("status", "unknown")
                    },
                    "original_content": article["content"],
                    "gemini_analysis": gemini_analysis
                }
                
                analysis_results["articles_analysis"].append(article_analysis)
            
            return analysis_results
            
    except Exception as e:
        print(f"Error in main function: {e}")
        return None


def format_and_display_results(results):
    """
    Format and display the analysis results in a readable way
    """
    if not results:
        print("No results to display")
        return
    
    print("\n" + "="*80)
    print("THE HINDU EDITORIAL ANALYSIS REPORT")
    print("="*80)
    
    # Display session info
    session = results["session_info"]
    print(f"Analysis completed at: {session['timestamp']}")
    print(f"Total articles analyzed: {session['total_articles']}")
    print(f"Status: {session['analysis_status']}")
    
    # Display each article analysis
    for article_data in results["articles_analysis"]:
        article_info = article_data["article_info"]
        analysis = article_data["gemini_analysis"]
        
        print("\n" + "-"*80)
        print(f"ARTICLE {article_info['number']}: {article_info['title']}")
        print("-"*80)
        print(f"URL: {article_info['url']}")
        print(f"Status: {article_info['status']}")
        
        if analysis:
            print("\n📝 CENTRAL IDEA:")
            print(f"   {analysis.get('central_idea', 'Not available')}")
            
            print(f"\n🎭 AUTHOR'S TONE: {analysis.get('tone_of_author', 'Not available').upper()}")
            
            print("\n📚 PARAGRAPH-WISE SUMMARY:")
            for i, summary in enumerate(analysis.get('paragraph_wise_summary', []), 1):
                print(f"   {i}. {summary}")
            
            print("\n📖 VOCABULARY BUILDER:")
            for vocab in analysis.get('vocabulary_builder', []):
                print(f"   • {vocab.get('word', 'N/A')}: {vocab.get('meaning', 'N/A')}")
                print(f"     Example: {vocab.get('example_usage', 'N/A')}")
            
            print("\n🤔 CRITICAL THINKING QUESTIONS:")
            for i, question in enumerate(analysis.get('critical_thinking_questions', []), 1):
                print(f"   {i}. {question.get('question', 'N/A')} ({question.get('question_type', 'N/A')})")
            
            print("\n💡 KEY TAKEAWAY:")
            print(f"   {analysis.get('takeaway', 'Not available')}")
        else:
            print("\n❌ Gemini analysis failed for this article")
        
        print("\n" + "="*40 + " ORIGINAL CONTENT " + "="*40)
        content = article_data["original_content"]
        print(content)


def save_results_to_file(results, filename=None):
    """
    Save the analysis results to a JSON file
    """
    if not results:
        print("No results to save")
        return
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"editorial_analysis_{timestamp}.json"
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    filepath = os.path.join("logs", filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {filepath}")
    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    # Run analysis
    results = main(2)
    
    if results:
        # Display formatted results
        format_and_display_results(results)
        
        # Save to file
        save_results_to_file(results)
    else:
        print("Analysis failed or returned no results")
