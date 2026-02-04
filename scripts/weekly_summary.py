"""
Weekly Summary Generator
Analyzes learning log and generates weekly reflection summaries
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

def main():
    """Generate weekly learning summary"""
    
    print("📊 Generating weekly learning summary...")
    
    # Get current date
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())  # Monday of current week
    week_start_str = week_start.strftime("%Y-%m-%d")
    
    print(f"   Week starting: {week_start_str}")
    
    # Setup paths
    learning_log = Path("learning_log.md")
    weekly_summary = Path("weekly_summary.md")
    
    # Check if learning log exists
    if not learning_log.exists():
        print("⚠️  No learning log found, creating placeholder summary")
        create_placeholder_summary(weekly_summary, week_start_str)
        return
    
    # Parse learning log
    print("📖 Parsing learning log...")
    entries = parse_learning_log(learning_log, week_start)
    
    if not entries:
        print("ℹ️  No entries found for this week")
        create_placeholder_summary(weekly_summary, week_start_str)
        return
    
    # Analyze entries
    stats = analyze_entries(entries)
    
    # Initialize weekly summary file if needed
    if not weekly_summary.exists():
        weekly_summary.write_text("# 📊 Weekly Learning Summaries\n\n", encoding="utf-8")
    
    # Check if this week's summary already exists
    content = weekly_summary.read_text(encoding="utf-8")
    if f"## Week of {week_start_str}" in content:
        print(f"✅ Summary for week of {week_start_str} already exists")
        return
    
    # Generate summary
    summary = generate_summary(week_start_str, entries, stats)
    
    # Append to file
    with weekly_summary.open("a", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✅ Weekly summary generated successfully!")
    print(f"   Total entries: {stats['total']}")
    print(f"   Domains: {', '.join(stats['domains'].keys())}")

def parse_learning_log(log_path, week_start):
    """Parse learning log and extract entries from this week"""
    
    content = log_path.read_text(encoding="utf-8")
    entries = []
    
    # Regex to match entries: ## YYYY-MM-DD — [Domain] Topic
    pattern = r'## (\d{4}-\d{2}-\d{2}) — \[([^\]]+)\] (.+)'
    
    for match in re.finditer(pattern, content):
        date_str, domain, topic = match.groups()
        entry_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Only include entries from this week
        if entry_date >= week_start:
            entries.append({
                'date': date_str,
                'domain': domain,
                'topic': topic
            })
    
    return entries

def analyze_entries(entries):
    """Analyze entries to generate statistics"""
    
    stats = {
        'total': len(entries),
        'domains': defaultdict(int),
        'topics': []
    }
    
    for entry in entries:
        stats['domains'][entry['domain']] += 1
        stats['topics'].append(entry['topic'])
    
    return stats

def generate_summary(week_start_str, entries, stats):
    """Generate formatted weekly summary"""
    
    summary = f"\n## Week of {week_start_str}\n\n"
    summary += f"**Total Learning Entries:** {stats['total']}\n\n"
    
    # Domain breakdown
    summary += "**Domain Breakdown:**\n"
    for domain, count in stats['domains'].items():
        summary += f"- {domain}: {count} entries\n"
    summary += "\n"
    
    # Topics covered
    summary += "**Topics Covered:**\n"
    for entry in entries:
        summary += f"- [{entry['domain']}] {entry['topic']}\n"
    summary += "\n"
    
    # Reflection prompts
    summary += "**Weekly Reflection:**\n"
    summary += "- [ ] What was the most valuable learning this week?\n"
    summary += "- [ ] Which topic do I want to explore deeper?\n"
    summary += "- [ ] What connections did I make between topics?\n"
    summary += "- [ ] What should I focus on next week?\n"
    summary += "\n---\n"
    
    return summary

def create_placeholder_summary(weekly_summary, week_start_str):
    """Create placeholder summary when no entries exist"""
    
    if not weekly_summary.exists():
        weekly_summary.write_text("# 📊 Weekly Learning Summaries\n\n", encoding="utf-8")
    
    # Check if already exists
    content = weekly_summary.read_text(encoding="utf-8")
    if f"## Week of {week_start_str}" in content:
        print(f"✅ Placeholder for week of {week_start_str} already exists")
        return
    
    summary = f"\n## Week of {week_start_str}\n\n"
    summary += "**Status:** Planning week - no entries yet\n\n"
    summary += "**Weekly Planning:**\n"
    summary += "- [ ] Review learning goals\n"
    summary += "- [ ] Identify focus areas (AI/DSA/System Design)\n"
    summary += "- [ ] Set learning targets\n"
    summary += "\n---\n"
    
    with weekly_summary.open("a", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✅ Created weekly planning placeholder")

if __name__ == "__main__":
    main()
