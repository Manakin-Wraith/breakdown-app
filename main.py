import tkinter as tk
from tkinter import filedialog, messagebox
from script_breakdown import breakdown_script
import json
from fuzzywuzzy import process

def save_to_file(parsed_scenes):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(parsed_scenes, file, indent=4)
        messagebox.showinfo("Save", f"Data saved to {file_path}")

def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        global parsed_scenes
        parsed_scenes = breakdown_script(file_path)
        display_scenes(parsed_scenes)
        save_button.config(state=tk.NORMAL)

def advanced_search(search_term, scenes):
    # Fuzzy matching for scenes, actors, and dialogues
    results = []
    for i, scene_info in enumerate(scenes):
        scene_matches = process.extract(search_term, [scene_info['scene']], limit=1)
        dialogue_matches = process.extract(search_term, [dialogue for actor, dialogue in scene_info['lines']], limit=3)
        actor_matches = process.extract(search_term, [actor for actor, dialogue in scene_info['lines']], limit=3)

        if scene_matches[0][1] > 80 or any(match[1] > 80 for match in dialogue_matches) or any(match[1] > 80 for match in actor_matches):
            results.append({
                'scene_number': i + 1,
                'scene': scene_info['scene'],
                'lines': scene_info['lines']
            })
    return results        

def search_scenes():
    search_term = search_entry.get().strip()
    if not search_term:
        messagebox.showwarning("Search", "Please enter a search term.")
        return

    results = advanced_search(search_term, parsed_scenes)

    if results:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        for result in results:
            text_area.insert(tk.END, f"Scene {result['scene_number']}:\n")
            text_area.insert(tk.END, f"{result['scene']}\n\n")
            for actor, dialogue in result['lines']:
                text_area.insert(tk.END, f"{actor}:\n{dialogue}\n\n")
            text_area.insert(tk.END, "-" * 40 + "\n\n")
        text_area.config(state=tk.DISABLED)
    else:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "No matches found.\n")
        text_area.config(state=tk.DISABLED)

def display_scenes(parsed_scenes):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    for i, scene_info in enumerate(parsed_scenes, start=1):
        text_area.insert(tk.END, f"Scene {i}:\n")
        text_area.insert(tk.END, f"{scene_info['scene']}\n\n")
        for actor, dialogue in scene_info['lines']:
            text_area.insert(tk.END, f"{actor}:\n{dialogue}\n\n")
        text_area.insert(tk.END, "-" * 40 + "\n\n")
    text_area.config(state=tk.DISABLED)

def display_analytics(parsed_scenes):
    try:
        total_scenes = len(parsed_scenes)
        total_int_scenes = sum(1 for scene in parsed_scenes if "INT." in scene['scene'])
        total_ext_scenes = sum(1 for scene in parsed_scenes if "EXT." in scene['scene'])
        total_lines = sum(len(scene_info['lines']) for scene_info in parsed_scenes)
        total_actors = len(set(actor for scene_info in parsed_scenes for actor, _ in scene_info['lines']))

        analytics_text = (
            f"Total Scenes: {total_scenes}\n"
            f"Total INT Scenes: {total_int_scenes}\n"
            f"Total EXT Scenes: {total_ext_scenes}\n"
            f"Total Lines: {total_lines}\n"
            f"Total Actors: {total_actors}\n"
        )
        
        # Display analytics in a pop-up window
        messagebox.showinfo("Analytics", analytics_text)
    except Exception as e:
        print(f"Error displaying analytics: {e}")

def view_scene(scene_number):
    if 'parsed_scenes' not in globals():
        messagebox.showwarning("Error", "No scenes available. Please upload a PDF first.")
        return

    try:
        scene_number = int(scene_number)
    except ValueError:
        messagebox.showwarning("Error", "Please enter a valid integer for the scene number.")
        return

    if scene_number < 1 or scene_number > len(parsed_scenes):
        messagebox.showwarning("Error", "Scene number out of range.")
        return

    scene_info = parsed_scenes[scene_number - 1]
    scene_text = f"Scene {scene_number}:\n"
    scene_text += f"{scene_info['scene']}\n\n"
    for actor, dialogue in scene_info['lines']:
        scene_text += f"{actor}:\n{dialogue}\n\n"
    
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, scene_text)
    text_area.config(state=tk.DISABLED)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Script Breakdown")
root.geometry("800x600")

upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=10)

save_button = tk.Button(root, text="Save Data", command=lambda: save_to_file(parsed_scenes), state=tk.DISABLED)
save_button.pack(pady=10)

search_label = tk.Label(root, text="Search:")
search_label.pack(pady=5)

search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_scenes)
search_button.pack(pady=5)

scene_number_label = tk.Label(root, text="Enter Scene Number:")
scene_number_label.pack(pady=5)

scene_number_entry = tk.Entry(root, width=20)
scene_number_entry.pack(pady=5)

view_scene_button = tk.Button(root, text="View Scene", command=lambda: view_scene(scene_number_entry.get()))
view_scene_button.pack(pady=10)

text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

analytics_button = tk.Button(root, text="Show Analytics", command=lambda: display_analytics(parsed_scenes))
analytics_button.pack(pady=10)

root.mainloop()
