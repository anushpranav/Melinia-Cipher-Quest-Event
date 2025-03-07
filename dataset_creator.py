import pandas as pd
import tkinter as tk
from tkinter import messagebox, Checkbutton, IntVar, ttk
import os
from functools import partial

# Static input file path - replace with your actual dataset path
INPUT_FILE_PATH = "Shuffled Datasets\Crime Data Prototype-2 (shuffled).csv"  # Change this to your actual file path
OUTPUT_DIRECTORY = "Round-2 Datasets"    # Folder to store all team datasets

# Always selected features
REQUIRED_FEATURES = [
    "ID", "CNTYFIPS", "Ori", "OffCount", "ActionType", 
    "VicAge", "VicRace", "VicSex", "Solved", "VicEthnic", 
    "OffEthnic", "Weapon", "Circumstance", "Subcircum",
    "Incident", "Relationship", "VicCount", "MSA", "FileDate"
]

def select_features():
    # Create main window with modern styling
    root = tk.Tk()
    root.title("Crime Data Feature Selector")
    root.geometry("1000x900")  # Increased window size
    
    # Set theme colors
    bg_color = "#f5f5f5"
    header_color = "#2c3e50"
    accent_color = "#3498db"
    success_color = "#2ecc71"
    
    root.configure(bg=bg_color)
    
    # Apply modern style to ttk widgets
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme as base
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 11))
    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=header_color, background=bg_color)
    style.configure("Info.TLabel", font=("Segoe UI", 10), foreground="#555555", background=bg_color)
    style.configure("Success.TLabel", foreground=success_color, background=bg_color)
    style.configure("Category.TLabel", font=("Segoe UI", 12, "bold"), foreground="#1a5276", background=bg_color)
    
    # Variables
    feature_vars = {}
    features = []
    
    def update_feature_display():
        # Clear previous checkboxes
        for widget in selected_frame.winfo_children():
            widget.destroy()
        for widget in unselected_frame.winfo_children():
            widget.destroy()
            
        # Define number of columns
        NUM_COLUMNS = 5  # Changed from 3 to 5
            
        # Display required features first
        ttk.Label(selected_frame, text="Required Features:", style="Category.TLabel").grid(row=0, column=0, columnspan=NUM_COLUMNS, sticky="w", pady=(0, 10))
        
        row_selected_req = 1
        for i, feature in enumerate([f for f in features if f in REQUIRED_FEATURES]):
            var = feature_vars[feature]
            
            cb_frame = ttk.Frame(selected_frame)
            cb_frame.grid(row=row_selected_req + i//NUM_COLUMNS, column=i%NUM_COLUMNS, sticky="w", padx=10, pady=5)
            
            cb = Checkbutton(
                cb_frame, 
                text=feature,
                variable=var,
                bg=bg_color,
                fg="#1a5276",
                font=("Segoe UI", 10, "bold"),
                state=tk.DISABLED
            )
            cb.pack(side=tk.LEFT)
            ttk.Label(cb_frame, text="(required)", style="Info.TLabel").pack(side=tk.LEFT, padx=(5, 0))
        
        # Display optional selected features
        row_selected_req += (len([f for f in features if f in REQUIRED_FEATURES]) // NUM_COLUMNS) + 1
        
        optional_selected = [f for f in features if f not in REQUIRED_FEATURES and feature_vars[f].get() == 1]
        if optional_selected:
            ttk.Label(selected_frame, text="Optional Selected Features:", style="Category.TLabel").grid(row=row_selected_req, column=0, columnspan=NUM_COLUMNS, sticky="w", pady=(15, 10))
            
            for i, feature in enumerate(optional_selected):
                var = feature_vars[feature]
                
                cb_frame = ttk.Frame(selected_frame)
                cb_frame.grid(row=row_selected_req + 1 + i//NUM_COLUMNS, column=i%NUM_COLUMNS, sticky="w", padx=10, pady=5)
                
                cb = Checkbutton(
                    cb_frame, 
                    text=feature,
                    variable=var,
                    bg=bg_color,
                    fg="#2c3e50",
                    font=("Segoe UI", 10),
                    command=update_feature_display
                )
                cb.pack(side=tk.LEFT)
        
        # Display unselected optional features
        optional_unselected = [f for f in features if f not in REQUIRED_FEATURES and feature_vars[f].get() == 0]
        if optional_unselected:
            ttk.Label(unselected_frame, text="Unselected Optional Features:", style="Category.TLabel").grid(row=0, column=0, columnspan=NUM_COLUMNS, sticky="w", pady=(0, 10))
            
            for i, feature in enumerate(optional_unselected):
                var = feature_vars[feature]
                
                cb_frame = ttk.Frame(unselected_frame)
                cb_frame.grid(row=1 + i//NUM_COLUMNS, column=i%NUM_COLUMNS, sticky="w", padx=10, pady=5)
                
                cb = Checkbutton(
                    cb_frame, 
                    text=feature,
                    variable=var,
                    bg=bg_color,
                    fg="#555555",
                    font=("Segoe UI", 10),
                    command=update_feature_display
                )
                cb.pack(side=tk.LEFT)
    
    def load_features():
        nonlocal features, feature_vars
        # Read the CSV headers
        try:
            df = pd.read_csv(INPUT_FILE_PATH, nrows=0)
            features = df.columns.tolist()
            
            # Create variables for each feature
            feature_vars = {}
            for feature in features:
                var = IntVar(value=1 if feature in REQUIRED_FEATURES else 0)
                feature_vars[feature] = var
            
            # Update display
            update_feature_display()
             
            # Enable buttons
            select_optional_btn.config(state=tk.NORMAL)
            deselect_optional_btn.config(state=tk.NORMAL)
            generate_btn.config(state=tk.NORMAL)
            
            # Update status
            status_label.config(text=f"Loaded {len(features)} features from dataset")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error reading CSV file: {str(e)}")
            status_label.config(text=f"Error: {str(e)}")
    
    def select_all_optional():
        for feature in features:
            if feature not in REQUIRED_FEATURES:
                feature_vars[feature].set(1)
        update_feature_display()
    
    def deselect_all_optional():
        for feature in features:
            if feature not in REQUIRED_FEATURES:
                feature_vars[feature].set(0)
        update_feature_display()
    
    def generate_dataset():
        # Get selected features
        selected_features = [feature for feature in features if feature_vars[feature].get() == 1]
        
        # Ensure required features are always included
        for feature in REQUIRED_FEATURES:
            if feature in features and feature not in selected_features:
                selected_features.append(feature)
        
        team_name = team_entry.get().strip()
        if not team_name:
            messagebox.showerror("Error", "Please enter a team name")
            return
        
        try:
            # Read the CSV
            df = pd.read_csv(INPUT_FILE_PATH)
            
            # Validate selected features exist in dataframe
            valid_features = [f for f in selected_features if f in df.columns]
            if len(valid_features) != len(selected_features):
                invalid_features = set(selected_features) - set(valid_features)
                messagebox.showwarning("Warning", f"Some features not found in dataset: {', '.join(invalid_features)}\nProceeding with valid features only.")
                selected_features = valid_features
            
            # Select only the chosen features
            df_selected = df[selected_features]
            
            # Create output directory if it doesn't exist
            if not os.path.exists(OUTPUT_DIRECTORY):
                os.makedirs(OUTPUT_DIRECTORY)
            
            # Define output path
            output_file = f"{team_name}.csv"
            output_path = os.path.join(OUTPUT_DIRECTORY, output_file)
            
            # Save the new CSV
            df_selected.to_csv(output_path, index=False)
            
            messagebox.showinfo("Success", 
                               f"Dataset for {team_name} created successfully!\n"
                               f"Location: {output_path}\n"
                               f"Features: {len(selected_features)}")
            
            # Show selected features in the text widget
            features_text.config(state=tk.NORMAL)
            features_text.delete(1.0, tk.END)
            
            # Separate required and optional features for display
            req_features = [f for f in selected_features if f in REQUIRED_FEATURES]
            opt_features = [f for f in selected_features if f not in REQUIRED_FEATURES]
            
            features_text.insert(tk.END, f"Features selected for team '{team_name}':\n\n", "header")
            features_text.insert(tk.END, "Required Features:\n", "subheader")
            for feature in req_features:
                features_text.insert(tk.END, f"• {feature}\n", "required")
                
            features_text.insert(tk.END, "\nOptional Features:\n", "subheader")
            if opt_features:
                for feature in opt_features:
                    features_text.insert(tk.END, f"• {feature}\n", "optional")
            else:
                features_text.insert(tk.END, "None\n", "italic")
            
            features_text.config(state=tk.DISABLED)
                
            # Clear team name for next team
            team_entry.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error generating dataset: {str(e)}")
    
    # Create UI elements with improved styling
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    header_label = ttk.Label(main_frame, text="Crime Data Feature Selector", style="Header.TLabel")
    header_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
    
    # File info panel
    info_frame = ttk.Frame(main_frame, padding=10)
    info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    info_frame.configure(style="TFrame")
    
    ttk.Label(info_frame, text=f"Input File: ", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
    ttk.Label(info_frame, text=INPUT_FILE_PATH, foreground="#3498db").grid(row=0, column=1, sticky="w")
    
    ttk.Label(info_frame, text=f"Output Directory: ", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
    ttk.Label(info_frame, text=OUTPUT_DIRECTORY, foreground="#3498db").grid(row=1, column=1, sticky="w")
    
    # Status label
    status_label = ttk.Label(main_frame, text="Click 'Load Features' to begin", foreground="#777777")
    status_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 15))
    
    # Load button with better styling
    load_btn = tk.Button(
        main_frame, 
        text="Load Features", 
        command=load_features, 
        bg=accent_color, 
        fg="white", 
        padx=15, 
        pady=8,
        relief=tk.FLAT,
        font=("Segoe UI", 11)
    )
    load_btn.grid(row=3, column=0, sticky="w", pady=(0, 20))
    
    # Team name with better styling
    team_frame = ttk.Frame(main_frame)
    team_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 20))
    
    ttk.Label(team_frame, text="Team Name:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 10))
    team_entry = ttk.Entry(team_frame, width=30, font=("Segoe UI", 11))
    team_entry.pack(side=tk.LEFT)
    
    # Feature selection with better styling
    ttk.Label(main_frame, text="Select Features to Include:", font=("Segoe UI", 11, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 5))
    ttk.Label(main_frame, text="Note: Required features are automatically selected and cannot be deselected.", style="Info.TLabel").grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 10))
    
    # Buttons for select/deselect optional
    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 10))
    
    select_optional_btn = tk.Button(
        btn_frame, 
        text="Select All Optional", 
        command=select_all_optional, 
        state=tk.DISABLED,
        bg="#34495e", 
        fg="white", 
        padx=10, 
        pady=5,
        relief=tk.FLAT,
        font=("Segoe UI", 10)
    )
    select_optional_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    deselect_optional_btn = tk.Button(
        btn_frame, 
        text="Deselect All Optional", 
        command=deselect_all_optional, 
        state=tk.DISABLED,
        bg="#34495e", 
        fg="white", 
        padx=10, 
        pady=5,
        relief=tk.FLAT,
        font=("Segoe UI", 10)
    )
    deselect_optional_btn.pack(side=tk.LEFT)
    
    # Create a notebook for better organization
    notebook = ttk.Notebook(main_frame)
    # Increase the height by adding ipady
    notebook.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=(0, 15), ipady=150)
    
    # Create tabs for selected and unselected features
    features_container = ttk.Frame(notebook)
    notebook.add(features_container, text="Feature Selection")
    
    # Split the features container into two sections with explicit height
    features_paned = ttk.PanedWindow(features_container, orient=tk.VERTICAL, height=500)
    features_paned.pack(fill=tk.BOTH, expand=True)
    
    # Selected features frame (top section)
    selected_container = ttk.Frame(features_paned)
    features_paned.add(selected_container, weight=2)  # Increased weight to make it taller
    
    # Add scrollbar to the selected features section
    selected_canvas = tk.Canvas(selected_container, bg=bg_color, highlightthickness=0, height=300)
    selected_scrollbar = ttk.Scrollbar(selected_container, orient="vertical", command=selected_canvas.yview)
    selected_frame = ttk.Frame(selected_canvas)
    selected_frame.configure(style="TFrame")
    
    selected_canvas.configure(yscrollcommand=selected_scrollbar.set)
    
    selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    selected_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    selected_canvas_frame = selected_canvas.create_window((0, 0), window=selected_frame, anchor="nw")
    
    def on_selected_frame_configure(event):
        selected_canvas.configure(scrollregion=selected_canvas.bbox("all"))
        selected_canvas.itemconfig(selected_canvas_frame, width=selected_canvas.winfo_width())
    
    selected_frame.bind("<Configure>", on_selected_frame_configure)
    selected_canvas.bind("<Configure>", lambda e: selected_canvas.itemconfig(selected_canvas_frame, width=selected_canvas.winfo_width()))
    
    # Unselected features frame (bottom section)
    unselected_container = ttk.Frame(features_paned)
    features_paned.add(unselected_container, weight=2)  # Increased weight to make it taller
    
    # Add scrollbar to the unselected features section
    unselected_canvas = tk.Canvas(unselected_container, bg=bg_color, highlightthickness=0, height=300)
    unselected_scrollbar = ttk.Scrollbar(unselected_container, orient="vertical", command=unselected_canvas.yview)
    unselected_frame = ttk.Frame(unselected_canvas)
    unselected_frame.configure(style="TFrame")
    
    unselected_canvas.configure(yscrollcommand=unselected_scrollbar.set)
    
    unselected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    unselected_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    unselected_canvas_frame = unselected_canvas.create_window((0, 0), window=unselected_frame, anchor="nw")
    
    def on_unselected_frame_configure(event):
        unselected_canvas.configure(scrollregion=unselected_canvas.bbox("all"))
        unselected_canvas.itemconfig(unselected_canvas_frame, width=unselected_canvas.winfo_width())
    
    unselected_frame.bind("<Configure>", on_unselected_frame_configure)
    unselected_canvas.bind("<Configure>", lambda e: unselected_canvas.itemconfig(unselected_canvas_frame, width=unselected_canvas.winfo_width()))
    
    # Add mousewheel scrolling for both sections
    def _on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    selected_canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, selected_canvas) if selected_canvas.winfo_containing(e.x_root, e.y_root) == selected_canvas else None)
    unselected_canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, unselected_canvas) if unselected_canvas.winfo_containing(e.x_root, e.y_root) == unselected_canvas else None)
    
    # Generate button
    generate_btn = tk.Button(
        main_frame, 
        text="Generate Team Dataset", 
        command=generate_dataset, 
        state=tk.DISABLED, 
        bg=success_color, 
        fg="white", 
        padx=15, 
        pady=8,
        relief=tk.FLAT,
        font=("Segoe UI", 11, "bold")
    )
    generate_btn.grid(row=9, column=0, sticky="w", pady=(5, 20))
    
    # Selected features display with improved styling
    ttk.Label(main_frame, text="Selected Features Summary:", font=("Segoe UI", 11, "bold")).grid(row=10, column=0, columnspan=2, sticky="w")
    
    # Text widget with scrollbar and custom styling
    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=11, column=0, columnspan=2, sticky="nsew", pady=(5, 0))
    
    # Add scrollbar to text widget
    text_scrollbar = ttk.Scrollbar(text_frame)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    features_text = tk.Text(
        text_frame, 
        height=5,  # Reduced height from 8 to 5
        width=60, 
        font=("Segoe UI", 10),
        bg="white",
        relief=tk.FLAT,
        padx=10,
        pady=10,
        wrap=tk.WORD,
        yscrollcommand=text_scrollbar.set
    )
    
    # Add text tags for styling
    features_text.tag_configure("header", font=("Segoe UI", 12, "bold"))
    features_text.tag_configure("subheader", font=("Segoe UI", 11, "bold"), foreground="#2c3e50")
    features_text.tag_configure("required", foreground="#1a5276")
    features_text.tag_configure("optional", foreground="#2c3e50")
    features_text.tag_configure("italic", font=("Segoe UI", 10, "italic"), foreground="#555555")
    
    features_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_scrollbar.config(command=features_text.yview)
    
    # Initial text
    features_text.insert(tk.END, "Feature selection summary will appear here after dataset generation.", "italic")
    features_text.config(state=tk.DISABLED)
    
    # Configure grid to expand
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(8, weight=5)  # Increased weight for notebook row from 3 to 5
    main_frame.rowconfigure(11, weight=1)
    
    # Load features automatically at startup
    root.after(100, load_features)
    
    # Start the GUI
    root.mainloop()

# Command-line version for batch processing (updated to always include required features)
def generate_team_datasets(teams_config):
    try:
        # Read the CSV
        df = pd.read_csv(INPUT_FILE_PATH)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
        
        results = []
        
        # Process each team
        for team_name, selected_features in teams_config.items():
            try:
                # Always include required features
                for feature in REQUIRED_FEATURES:
                    if feature in df.columns and feature not in selected_features:
                        selected_features.append(feature)
                
                # Validate features
                invalid_features = [f for f in selected_features if f not in df.columns]
                if invalid_features:
                    results.append(f"Warning for {team_name}: Invalid features: {invalid_features}")
                    # Remove invalid features
                    selected_features = [f for f in selected_features if f in df.columns]
                
                if not selected_features:
                    results.append(f"Error for {team_name}: No valid features selected")
                    continue
                
                # Select only the chosen features
                df_selected = df[selected_features]
                
                # Define output path
                output_path = os.path.join(OUTPUT_DIRECTORY, f"{team_name}.csv")
                
                # Save the new CSV
                df_selected.to_csv(output_path, index=False)
                
                results.append(f"Success: Dataset for {team_name} created with {len(selected_features)} features")
                
            except Exception as e:
                results.append(f"Error for {team_name}: {str(e)}")
        
        # Print results
        print("\n=== Team Dataset Generation Results ===")
        for result in results:
            print(result)
        print(f"\nAll datasets saved to: {os.path.abspath(OUTPUT_DIRECTORY)}")
            
    except Exception as e:
        print(f"Error reading source file: {str(e)}")

if __name__ == "__main__":
    # Interactive GUI version:
    select_features()