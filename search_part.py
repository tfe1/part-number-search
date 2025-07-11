import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

SOURCES = {
    "Digi-Key": "https://www.digikey.com/en/products/result?keywords={}",
    "Mouser": "https://www.mouser.com/Search/Refine.aspx?Keyword={}",
    "Arrow": "https://www.arrow.com/en/products/search?q={}",
    "Rochester Electronics": "https://www.rocelec.com/search?text={}",
    "ISO Group": "https://www.iso-group.com/search?search={}",
    "FindChips": "https://www.findchips.com/search/{}",
    "Octopart": "https://octopart.com/search?q={}",
    "NSN Parts Now": "https://www.nsnpartsnow.com/search?q={}",
    "Alibaba": "https://www.alibaba.com/trade/search?SearchText={}",
    "PartsBase": "https://www.partsbase.com/search?q={}",
    "eBay": "https://www.ebay.com/sch/i.html?_nkw={}",
    "AVNET": "https://www.avnet.com/shop/us/search/?term={}",
    "Newark": "https://www.newark.com/search?st={}",
    "Electronics Surplus": "https://www.electronicsurplus.com/catalogsearch/result/?q={}",
    "Allied Electronics": "https://www.alliedelec.com/search/?keyword={}",
    "Chip 1 Exchange": "https://www.chip1stop.com/search?keywords={}",
    "Win Source": "https://www.win-source.net/search?q={}",
    "Utmel": "https://www.utmel.com/components/{}/search",
    "NSN Center": "https://www.nsncenter.com/nsn/search?nsn={}",
    "Buy NSN": "https://www.buynsn.com/search?q={}",
    "Part Target": "https://www.parttarget.com/search.aspx?q={}"
}

def search_part():
    part_number = entry_part.get().strip()
    if not part_number:
        messagebox.showwarning("Input Error", "Please enter a part number.")
        return

    selected = [src for src, var in source_vars.items() if var.get()]
    if not selected:
        messagebox.showwarning("Selection Error", "Please select at least one source.")
        return

    for source in selected:
        url = SOURCES[source].format(part_number)
        webbrowser.open_new_tab(url)

root = tk.Tk()
root.title("Aerospace Part Finder")
root.geometry("500x500")
root.resizable(False, False)

title = ttk.Label(root, text="Aerospace Part Search Tool", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

frame_entry = ttk.Frame(root)
frame_entry.pack(pady=10)
ttk.Label(frame_entry, text="Enter Part Number:").pack(side="left", padx=5)
entry_part = ttk.Entry(frame_entry, width=40)
entry_part.pack(side="left")

frame_sources = ttk.LabelFrame(root, text="Search Sources")
frame_sources.pack(padx=20, pady=10, fill="both", expand=True)

source_vars = {}
for source in SOURCES:
    var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(frame_sources, text=source, variable=var)
    chk.pack(anchor="w", padx=10)
    source_vars[source] = var

btn_search = ttk.Button(root, text="Search Part", command=search_part)
btn_search.pack(pady=20)

root.mainloop()
