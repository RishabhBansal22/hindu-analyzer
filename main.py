from scripts.gemini import Gemini
from scripts.scrapper import Scrapper
import json
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from textwrap import fill


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


def save_results_to_pdf(results, filename=None):
    """
    Save the analysis results to a well-formatted PDF file
    """
    if not results:
        print("No results to save")
        return
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"editorial_analysis_{timestamp}.pdf"
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    filepath = os.path.join("logs", filename)
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.darkred
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=8,
            textColor=colors.darkgreen
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10
        )
        
        # Build content
        content = []
        
        # Title page
        content.append(Paragraph("THE HINDU EDITORIAL ANALYSIS REPORT", title_style))
        content.append(Spacer(1, 20))
        
        # Session info
        session = results["session_info"]
        session_info = f"""
        <b>Analysis Date:</b> {datetime.fromisoformat(session['timestamp']).strftime('%B %d, %Y at %I:%M %p')}<br/>
        <b>Total Articles Analyzed:</b> {session['total_articles']}<br/>
        <b>Status:</b> {session['analysis_status'].title()}
        """
        content.append(Paragraph(session_info, body_style))
        content.append(Spacer(1, 30))
        
        # Table of contents
        content.append(Paragraph("TABLE OF CONTENTS", heading_style))
        toc_data = [["Article", "Title", "Page"]]
        
        for i, article_data in enumerate(results["articles_analysis"], 1):
            title = article_data["article_info"]["title"][:50] + ("..." if len(article_data["article_info"]["title"]) > 50 else "")
            toc_data.append([f"Article {i}", title, f"{i}"])
        
        toc_table = Table(toc_data, colWidths=[1*inch, 4*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(toc_table)
        content.append(PageBreak())
        
        # Process each article
        for idx, article_data in enumerate(results["articles_analysis"], 1):
            article_info = article_data["article_info"]
            analysis = article_data["gemini_analysis"]
            
            # Article header
            content.append(Paragraph(f"ARTICLE {idx}: {article_info['title']}", title_style))
            content.append(Spacer(1, 12))
            
            # Article metadata
            metadata = f"""
            <b>URL:</b> {article_info['url']}<br/>
            <b>Status:</b> {article_info['status'].title()}
            """
            content.append(Paragraph(metadata, body_style))
            content.append(Spacer(1, 20))
            
            # Original Content FIRST
            content.append(Paragraph("📰 ORIGINAL EDITORIAL CONTENT", heading_style))
            original_content = article_data["original_content"]
            
            # Split content into paragraphs for better formatting
            paragraphs = original_content.split('\n')
            for para in paragraphs:
                if para.strip():
                    content.append(Paragraph(para.strip(), body_style))
            
            content.append(Spacer(1, 30))
            content.append(Paragraph("─" * 80, body_style))
            content.append(Spacer(1, 20))
            
            # THEN Analysis
            if analysis:
                content.append(Paragraph("🔍 GEMINI ANALYSIS", heading_style))
                content.append(Spacer(1, 12))
                
                # Central Idea
                content.append(Paragraph("📝 CENTRAL IDEA", subheading_style))
                content.append(Paragraph(analysis.get('central_idea', 'Not available'), body_style))
                content.append(Spacer(1, 12))
                
                # Author's Tone
                content.append(Paragraph("🎭 AUTHOR'S TONE", subheading_style))
                content.append(Paragraph(f"<b>{analysis.get('tone_of_author', 'Not available').upper()}</b>", body_style))
                content.append(Spacer(1, 12))
                
                # Paragraph-wise Summary
                content.append(Paragraph("📚 PARAGRAPH-WISE SUMMARY", subheading_style))
                for i, summary in enumerate(analysis.get('paragraph_wise_summary', []), 1):
                    content.append(Paragraph(f"{i}. {summary}", bullet_style))
                content.append(Spacer(1, 12))
                
                # Vocabulary Builder with better text wrapping
                content.append(Paragraph("📖 VOCABULARY BUILDER", subheading_style))
                vocab_data = [["Word", "Meaning", "Example Usage"]]
                
                for vocab in analysis.get('vocabulary_builder', []):
                    word = vocab.get('word', 'N/A')
                    meaning = vocab.get('meaning', 'N/A')
                    example = vocab.get('example_usage', 'N/A')
                    
                    # Use Paragraph objects for better text wrapping in cells
                    word_para = Paragraph(f"<b>{word}</b>", ParagraphStyle('WordStyle', parent=body_style, fontSize=9))
                    meaning_para = Paragraph(meaning, ParagraphStyle('MeaningStyle', parent=body_style, fontSize=8))
                    example_para = Paragraph(example, ParagraphStyle('ExampleStyle', parent=body_style, fontSize=8))
                    
                    vocab_data.append([word_para, meaning_para, example_para])
                
                # Adjusted column widths to fit page better
                vocab_table = Table(vocab_data, colWidths=[1.2*inch, 2.8*inch, 2.8*inch])
                vocab_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                
                content.append(vocab_table)
                content.append(Spacer(1, 12))
                
                # Critical Thinking Questions
                content.append(Paragraph("🤔 CRITICAL THINKING QUESTIONS", subheading_style))
                for i, question in enumerate(analysis.get('critical_thinking_questions', []), 1):
                    q_text = question.get('question', 'N/A')
                    q_type = question.get('question_type', 'N/A')
                    content.append(Paragraph(f"{i}. {q_text} <i>({q_type})</i>", bullet_style))
                content.append(Spacer(1, 12))
                
                # Key Takeaway
                content.append(Paragraph("💡 KEY TAKEAWAY", subheading_style))
                content.append(Paragraph(analysis.get('takeaway', 'Not available'), body_style))
                content.append(Spacer(1, 20))
            else:
                content.append(Paragraph("❌ Gemini analysis failed for this article", body_style))
                content.append(Spacer(1, 20))
            
            # Add page break except for the last article
            if idx < len(results["articles_analysis"]):
                content.append(PageBreak())
        
        # Build PDF
        doc.build(content)
        print(f"\n📄 PDF report saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None


def save_simple_pdf(results, filename=None):
    """
    Create a simpler PDF as a fallback option
    """
    if not results:
        print("No results to save")
        return
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"editorial_analysis_simple_{timestamp}.pdf"
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    filepath = os.path.join("logs", filename)
    
    try:
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        content = []
        
        # Title
        content.append(Paragraph("THE HINDU EDITORIAL ANALYSIS REPORT", styles['Title']))
        content.append(Spacer(1, 20))
        
        # Session info
        session = results["session_info"]
        content.append(Paragraph(f"Analysis Date: {session['timestamp']}", styles['Normal']))
        content.append(Paragraph(f"Total Articles: {session['total_articles']}", styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Articles
        for idx, article_data in enumerate(results["articles_analysis"], 1):
            article_info = article_data["article_info"]
            analysis = article_data["gemini_analysis"]
            
            content.append(Paragraph(f"Article {idx}: {article_info['title']}", styles['Heading1']))
            content.append(Spacer(1, 12))
            
            if analysis:
                content.append(Paragraph("Central Idea:", styles['Heading2']))
                content.append(Paragraph(analysis.get('central_idea', 'Not available'), styles['Normal']))
                content.append(Spacer(1, 12))
                
                content.append(Paragraph(f"Author's Tone: {analysis.get('tone_of_author', 'Not available')}", styles['Normal']))
                content.append(Spacer(1, 12))
                
                content.append(Paragraph("Key Takeaway:", styles['Heading2']))
                content.append(Paragraph(analysis.get('takeaway', 'Not available'), styles['Normal']))
                content.append(Spacer(1, 20))
        
        doc.build(content)
        print(f"\n📄 Simple PDF report saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error creating simple PDF: {e}")
        return None


if __name__ == "__main__":
    # Run analysis
    results = main(1)
    
    if results:
        # Display formatted results
        format_and_display_results(results)
        
        # Try to save detailed PDF, fallback to simple PDF if needed
        pdf_path = save_results_to_pdf(results)
        if not pdf_path:
            print("Detailed PDF creation failed, trying simple PDF...")
            save_simple_pdf(results)
    else:
        print("Analysis failed or returned no results")
