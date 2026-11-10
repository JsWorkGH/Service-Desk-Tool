import customtkinter as ctk
import subprocess
import json

#=======================================

with open("templates.json", "r", encoding="utf-8") as file:
    template_data = json.load(file)
    
#=======================================

def get_windows_display_name():
    ps_command = r"""
$identity = whoami

$session = Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\SessionData' -ErrorAction SilentlyContinue |
    Get-ItemProperty -ErrorAction SilentlyContinue |
    Where-Object { $_.LoggedOnUser -eq $identity } |
    Select-Object -First 1
    
$displayName = $session.LoggedOnDisplayName

if ($displayName) {
    $displayName.Trim()
}
    """
    
    result = subprocess.run(
    [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        ps_command
    ],
    capture_output=True,
    text=True,
    timeout=10,
    )
    
    return result.stdout.strip()

#=======================================

    
def template_text(selected_template, selected_action):
    template_content = template_data["templates"][selected_template][selected_action]
    
    for variable, value in template_variables.items():
        template_content = template_content.replace("{" + variable + "}", value)
        
    return template_content

#=======================================

def copy_text(text, button):
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
    
    button.configure(text="Copied!")
    
    window.after(5000, lambda: button.configure(text="Copy"))

#=======================================

def dynamic_wraplength(event, label, padding=5):
    available_width = max(50, event.width - padding)
    
    if label.cget("wraplength") != available_width:
        label.configure(wraplength=available_width)

#=======================================
    
def template_buttons(selected_template):
    for widget in template_frame.winfo_children():
        widget.destroy()
        
    if selected_template == "Choose Template":
        return
        
    templates = template_data["templates"][selected_template]
    
    open_template = None
    
    def toggle_template(content_frame):
        nonlocal open_template
        
        if open_template == content_frame:
            content_frame.pack_forget()
            open_template = None
        else:
            if open_template is not None:
                open_template.pack_forget()
                
            content_frame.pack(fill="x", pady=5)
            open_template = content_frame
                
    for action in templates.keys():
        if action == "FAQs":
            continue
            
        template_content = template_text(selected_template, action)
        
        template_item_frame = ctk.CTkFrame(
            template_frame,
            fg_color="transparent"
        )
        template_item_frame.pack(fill="x", padx= 5, pady=5)
        
        content_frame = ctk.CTkFrame(
            template_item_frame,
            fg_color="transparent"
        )

        copy_button = ctk.CTkButton(
            content_frame,
            text="Copy",
            width=30,
            bg_color="transparent"            
        )
        
        copy_button.configure(
            command=lambda text=template_content, button=copy_button: copy_text(text, button)
        )
        
        copy_button.pack(side="right", anchor="n", padx=(10, 0), pady=5)
        
        template_label = ctk.CTkLabel(
            content_frame,
            text=template_content,
            width=1,
            anchor="nw",
            justify="left",
            wraplength=100
        )
        template_label.pack(side="left", fill="x", expand=True, anchor="n", pady=5)
        
        template_item_frame.bind(
            "<Configure>",
            lambda event, label=template_label: dynamic_wraplength(event, label, padding=65)
        )

        template_button = ctk.CTkButton(
            template_item_frame,
            text=action,
            anchor="w",
            command=lambda frame=content_frame: toggle_template(frame)
        )
        template_button.pack(fill="x")

    faqs_text(selected_template)

#=======================================
        
def faqs_text(selected_template):
    for widget in faq_frame.winfo_children():
        widget.destroy()
        
    faqs = template_data["templates"][selected_template]["FAQs"]
    
    open_answer = None
    
    def toggle_answer(answer_label):
        nonlocal open_answer
        
        if open_answer == answer_label:
            answer_label.pack_forget()
            open_answer = None
        else:
            if open_answer is not None:
                open_answer.pack_forget()
                
            answer_label.pack(fill="x", pady=5)
            open_answer = answer_label
            
    for faq in faqs:
        faq_item_frame = ctk.CTkFrame(
            faq_frame,
            fg_color="transparent"
        )
        faq_item_frame.pack(fill="x", padx=5, pady=5)
            
        answer_label = ctk.CTkLabel(
            faq_item_frame,
            text=faq["answer"],
            anchor="w",
            justify="left",
            wraplength=300
        )
        
        faq_item_frame.bind(
            "<Configure>",
            lambda event, label=answer_label: dynamic_wraplength(event, label)
        )
            
        question_button = ctk.CTkButton(
            faq_item_frame,
            text=faq["question"],
            anchor="w",
            command=lambda answer=answer_label: toggle_answer(answer)
        )
        question_button.pack(fill="x")
            
        answer_label.pack_forget()

#=======================================

fullname = get_windows_display_name()
firstname = fullname.split()[0] if fullname else ""

#=======================================

template_variables = {
    "fullname": fullname,
    "firstname": firstname,
    "signature": template_data["variables"]["signature"].replace("{fullname}", fullname),
    "description": template_data["variables"]["description"],
    "endnotes": template_data["variables"]["endnotes"]
}

#=======================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()

window.title("Service Desk Toolkit")
window.geometry("800x450")
window.minsize(400, 250)

main_frame = ctk.CTkFrame(
    window,
    fg_color="transparent"
)
main_frame.pack(fill="both", expand=True, pady=20)

top_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
top_frame.pack(fill="x", pady=10)

bottom_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
bottom_frame.pack(fill="both", expand=True)

left_frame = ctk.CTkFrame(
    bottom_frame,
    width=350,
    fg_color="transparent"
)
left_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

right_frame = ctk.CTkFrame(
    bottom_frame,
    width=350,
    fg_color="transparent"
)
right_frame.pack(side="right", fill="both", expand=True, padx=(0, 5))

label = ctk.CTkLabel(
    top_frame,
    text="Welcome to your Ticketing Toolkit", 
    font=("Segoe UI", 16)
)
label.pack()

template_dropdown = ctk.CTkComboBox(
    top_frame,
    values=list(template_data["templates"].keys()),
    command=template_buttons,
    width=250,
    height=35,
    state="readonly"
)
template_dropdown.pack(pady=10)

template_dropdown.set("Choose Template")


template_label = ctk.CTkLabel(
    left_frame,
    text="Templates",
    font=("Segoe UI", 16, "bold")
)
template_label.pack(anchor="c", pady=10)

template_frame = ctk.CTkScrollableFrame(
    left_frame
)
template_frame.pack(fill="both", expand=True, padx=15, pady=10, anchor="n")

faq_label = ctk.CTkLabel(
    right_frame,
    text="Frequently Asked Questions",
    font=("Segoe UI", 16, "bold")
)
faq_label.pack(anchor="c", pady=10)

faq_frame = ctk.CTkScrollableFrame(
    right_frame
)
faq_frame.pack(fill="both", expand=True, padx=15, pady=10)

#=======================================

window.mainloop()