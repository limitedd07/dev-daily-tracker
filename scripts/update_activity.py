"""
Activity Tracker
Tracks daily automation activity with better formatting and statistics
"""

from datetime import datetime
from pathlib import Path

def main():
    """Update activity log with current timestamp"""
    
    # Get current timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    day_name = now.strftime("%A")
    
    print(f"📝 Recording activity for {date_str} ({day_name})")
    
    # Setup path
    activity_log = Path("activity_log.md")
    
    # Initialize if needed
    if not activity_log.exists():
        header = "# 📈 Activity Log\n\n"
        header += "Tracking daily automation runs and system activity.\n\n"
        activity_log.write_text(header, encoding="utf-8")
    
    # Check if we already logged today
    content = activity_log.read_text(encoding="utf-8")
    if f"- **{date_str}**" in content:
        print(f"✅ Activity for {date_str} already logged")
        return
    
    # Append new activity
    entry = f"- **{date_str}** ({day_name}) - Activity logged at {timestamp}\n"
    
    with activity_log.open("a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"✅ Activity logged successfully")

if __name__ == "__main__":
    main()
