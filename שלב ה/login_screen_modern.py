# login_screen_modern.py - Updated for Single Window System
import tkinter as tk
from tkinter import messagebox
from db_connection import DatabaseConnection

class ModernLoginScreen:
    def __init__(self, callback):
        self.callback = callback
        self.db = DatabaseConnection()
        self.create_login_window()
    
    def create_login_window(self):
        """יצירת חלון הכניסה"""
        self.window = tk.Tk()
        self.window.title("מערכת ניהול נתונים צבאית - צה״ל")
        self.window.geometry("500x400")
        self.window.configure(bg='#1a4d3a')  # ירוק כהה
        self.window.resizable(True, True)
        
        # Center window
        self.center_window()
        
        # Main container
        self.create_main_container()
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Focus on window
        self.window.focus_set()
        
        self.window.mainloop()
    
    def center_window(self):
        """מרכוז החלון במסך"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
    
    def create_main_container(self):
        """יצירת התוכן הראשי"""
        # Header with IDF styling
        header_frame = tk.Frame(self.window, bg='#2d5a3d', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # IDF symbols and title
        symbols_label = tk.Label(header_frame, text="🇮🇱 🛡️ צה״ל", 
                                font=('Arial', 20, 'bold'), fg='white', bg='#2d5a3d')
        symbols_label.pack(pady=20)
        
        # Login form container
        form_frame = tk.Frame(self.window, bg='#3d7050', relief='raised', bd=2)
        form_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Title
        title_label = tk.Label(form_frame, text="🎖️ כניסה למערכת 🎖️", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#3d7050')
        title_label.pack(pady=20)
        
        # Login fields
        self.create_login_fields(form_frame)
        
        # Buttons
        self.create_buttons(form_frame)
        
        # Footer
        footer_label = tk.Label(self.window, text="🔒 מערכת מאובטחת - יחידת מחשוב צה״ל", 
                               font=('Arial', 10), fg='#90EE90', bg='#1a4d3a')
        footer_label.pack(side='bottom', pady=10)
    
    def create_login_fields(self, parent):
        """יצירת שדות הכניסה"""
        fields_frame = tk.Frame(parent, bg='#3d7050')
        fields_frame.pack(padx=40, pady=20)
        
        # Username
        tk.Label(fields_frame, text="👤 שם משתמש:", 
                font=('Arial', 12, 'bold'), fg='white', bg='#3d7050').pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(fields_frame, font=('Arial', 12), width=25,
                                      bg='white', fg='#1a4d3a', relief='solid', bd=2)
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "admin")  # Default value
        
        # Password
        tk.Label(fields_frame, text="🔐 סיסמה:", 
                font=('Arial', 12, 'bold'), fg='white', bg='#3d7050').pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(fields_frame, show="*", font=('Arial', 12), width=25,
                                      bg='white', fg='#1a4d3a', relief='solid', bd=2)
        self.password_entry.pack(pady=(0, 15))
        self.password_entry.insert(0, "1234")  # Default value
        
        # Focus on username field
        self.username_entry.focus_set()
    
    def create_buttons(self, parent):
        """יצירת כפתורי הפעולה"""
        buttons_frame = tk.Frame(parent, bg='#3d7050')
        buttons_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(buttons_frame, text="🔓 כניסה למערכת", 
                             command=self.login,
                             bg='#1a4d3a', fg='white', font=('Arial', 14, 'bold'),
                             width=20, height=2, relief='raised', bd=3,
                             cursor='hand2')
        login_btn.pack(pady=10)
        
        # Test connection button
        test_btn = tk.Button(buttons_frame, text="🔧 בדיקת חיבור", 
                            command=self.test_connection,
                            bg='#5a8a6a', fg='white', font=('Arial', 11),
                            width=18, relief='raised', bd=2)
        test_btn.pack(pady=5)
        
        # Bind Enter key to login
        self.window.bind('<Return>', lambda event: self.login())
        
        # Add some keyboard shortcuts
        self.username_entry.bind('<Tab>', lambda event: self.password_entry.focus_set())
        self.password_entry.bind('<Return>', lambda event: self.login())
    
    def test_connection(self):
        """בדיקת חיבור לבסיס הנתונים"""
        self.show_loading_message("בודק חיבור...")
        
        try:
            if self.db.connect():
                self.db.disconnect()
                messagebox.showinfo("בדיקת חיבור", "✅ החיבור לבסיס הנתונים הצליח!")
            else:
                messagebox.showerror("בדיקת חיבור", "❌ החיבור לבסיס הנתונים נכשל!")
        except Exception as e:
            messagebox.showerror("שגיאת חיבור", f"❌ שגיאה בחיבור:\n{str(e)}")
        
        self.hide_loading_message()
    
    def show_loading_message(self, message):
        """הצגת הודעת טעינה"""
        self.loading_label = tk.Label(self.window, text=message, 
                                     font=('Arial', 12), fg='yellow', bg='#1a4d3a')
        self.loading_label.pack(side='bottom', pady=5)
        self.window.update()
    
    def hide_loading_message(self):
        """הסתרת הודעת הטעינה"""
        try:
            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.destroy()
        except tk.TclError:
            pass  # החלון כבר נהרס
    
    def login(self):
        """ביצוע התחברות"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not username:
            messagebox.showwarning("שגיאת הזדהות", "אנא הזן שם משתמש")
            self.username_entry.focus_set()
            return
        
        if not password:
            messagebox.showwarning("שגיאת הזדהות", "אנא הזן סיסמה")
            self.password_entry.focus_set()
            return
        
        # Check credentials
        if username == "admin" and password == "1234":
            self.show_loading_message("מתחבר למערכת...")
            
            try:
                if self.db.connect():
                    self.hide_loading_message()
                    messagebox.showinfo("התחברות הצליחה", f"🎖️ ברוך הבא, {username}!\nכניסה מאושרת למערכת")
                    
                    # סגירת חלון הכניסה והעברת השליטה לאפליקציה הראשית
                    self.window.destroy()
                    self.callback(self.db)
                else:
                    self.hide_loading_message()
                    messagebox.showerror("שגיאה", "❌ נכשל בחיבור לבסיס הנתונים")
            except Exception as e:
                self.hide_loading_message()
                messagebox.showerror("שגיאת מערכת", f"❌ שגיאה בהתחברות:\n{str(e)}")
        else:
            messagebox.showerror("שגיאת הזדהות", "❌ שם משתמש או סיסמה שגויים")
            # Clear password field on failed login
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus_set()
    
    def on_closing(self):
        """טיפול בסגירת החלון"""
        try:
            if self.db and hasattr(self.db, 'connection') and self.db.connection:
                self.db.disconnect()
        except:
            pass
        
        self.window.destroy()
        # Exit the application completely if login window is closed
        import sys
        sys.exit(0)