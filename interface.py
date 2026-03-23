import os, random, time
from rich.console import Console
from rich.text import Text
from rich.live import Live

def logo(v):
    """Restores the Matrix-style animation and Magenta pulse."""
    os.system("cls" if os.name == "nt" else "clear")
    console = Console()
    
    final_logo = rf"""
_____________            ________            _____     ________              
___  __ \__(_)___  __    __  ___/______________  /_    ___  __ \____________ 
__  /_/ /_  /__  |/_/    _____ \_  __ \_  ___/  __/    __  /_/ /_  ___/  __ \
_  ____/_  / __>  <      ____/ // /_/ /  /   / /_      _  ____/_  /   / /_/ /
/_/     /_/  /_/|_|      /____/ \____//_/    \__/      /_/     /_/    \____/ 
                                                                             
        PIXSORT ENGINE v{v} | HIGH INTEGRITY
    """
    
    lines = final_logo.strip("\n").split("\n")
    
    with Live(console=console, refresh_per_second=15, transient=True) as live:
        all_coords = []
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char != " ":
                    all_coords.append((r, c))
        
        random.shuffle(all_coords)
        batch_size = max(1, len(all_coords) // 28) 
        
        for i in range(0, len(all_coords), batch_size):
            current_batch = all_coords[:i+batch_size]
            output = []
            for r, line in enumerate(lines):
                row_str = ""
                for c, char in enumerate(line):
                    if (r, c) in current_batch:
                        row_str += char
                    elif char != " ":
                        row_str += random.choice("01$&#@%*")
                    else:
                        row_str += " "
                output.append(row_str)
            live.update(Text("\n" + "\n".join(output), style="bold green"))
            time.sleep(0.045)

        # Pulse effect
        for color in ["bold white", "bold bright_magenta", "bold magenta"]:
            live.update(Text("\n" + "\n".join(lines), style=color))
            time.sleep(0.2)
            
    # Final Static Print
    console.print(Text(final_logo, style="bold magenta"))
