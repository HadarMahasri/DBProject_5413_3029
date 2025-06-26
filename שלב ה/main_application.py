# main_application.py - עדכון לשימוש במודול CRUD מאוחד
import tkinter as tk
from tkinter import messagebox
from crud_manager import CRUDManager
from advanced_queries_manager import AdvancedQueriesManager


class MainApplication:
    def __init__(self):
        self.db = None
        self.main_window = None
        self.navigation_stack = []
        self.crud_manager = None  # מנהל ה-CRUD המאוחד
        self.start_application()
        self.advanced_queries_manager = None

    
    def start_application(self):
        """Start the application with login screen"""
        try:
            from login_screen_modern import ModernLoginScreen
            ModernLoginScreen(self.on_login_success)
        except ImportError:
            self.simple_login()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת מסך התחברות:\n{str(e)}")
    
    def simple_login(self):
        """Simple fallback login"""
        login_window = tk.Tk()
        login_window.title("התחברות למערכת")
        login_window.geometry("400x300")
        login_window.configure(bg='#1a4d3a')
        login_window.resizable(True, True)
        
        # Header
        header_label = tk.Label(login_window, text="🇮🇱 מערכת ניהול נתונים צבאית 🇮🇱", 
                               font=('Arial', 14, 'bold'), fg='white', bg='#1a4d3a')
        header_label.pack(pady=20)
        
        # Login form
        form_frame = tk.Frame(login_window, bg='#3d7050', relief='raised', bd=2)
        form_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(form_frame, text="שם משתמש:", font=('Arial', 12), 
                fg='white', bg='#3d7050').pack(pady=10)
        username_entry = tk.Entry(form_frame, font=('Arial', 12), width=20)
        username_entry.pack(pady=5)
        username_entry.insert(0, "admin")
        
        tk.Label(form_frame, text="סיסמה:", font=('Arial', 12), 
                fg='white', bg='#3d7050').pack(pady=10)
        password_entry = tk.Entry(form_frame, show="*", font=('Arial', 12), width=20)
        password_entry.pack(pady=5)
        password_entry.insert(0, "1234")
        
        def login():
            if username_entry.get() == "admin" and password_entry.get() == "1234":
                try:
                    from db_connection import DatabaseConnection
                    self.db = DatabaseConnection()
                    if self.db.connect():
                        messagebox.showinfo("הצלחה", "התחברות הצליחה!")
                        # יצירת מנהל CRUD לאחר חיבור למסד הנתונים
                        self.crud_manager = CRUDManager(self.db)
                        # המרת חלון הכניסה לחלון הראשי
                        self.main_window = login_window
                        self.main_window.title("🎖️ מערכת ניהול נתונים צבאית - תפריט ראשי")
                        self.main_window.geometry("1200x800")
                        self.show_main_menu()
                    else:
                        messagebox.showerror("שגיאה", "נכשל בחיבור לבסיס הנתונים")
                except Exception as e:
                    messagebox.showerror("שגיאה", f"שגיאה בחיבור: {str(e)}")
            else:
                messagebox.showerror("שגיאה", "שם משתמש או סיסמה שגויים")
        
        login_btn = tk.Button(form_frame, text="🔓 התחבר", command=login,
                            bg='#1a4d3a', fg='white', font=('Arial', 14, 'bold'),
                            width=15, height=2)
        login_btn.pack(pady=20)
        
        login_window.mainloop()
    
    def on_login_success(self, db_connection):
        self.db = db_connection
        self.main_window = tk.Tk()
        self.main_window.title("🎖️ מערכת ניהול נתונים צבאית - תפריט ראשי")
        self.main_window.geometry("1200x800")
        self.main_window.configure(bg='#1a4d3a')
        self.main_window.resizable(True, True)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.crud_manager = CRUDManager(self.db)
        self.advanced_queries_manager = AdvancedQueriesManager(self.db, self.main_window, self.navigation_stack)
        
        # הגדרת הפונקציה לחזרה לתפריט הראשי במנהל השאילתות
        self.advanced_queries_manager.set_main_menu_function(self.show_main_menu)

        self.show_main_menu()
        self.main_window.mainloop()

    
    def clear_window(self):
        """ניקוי תוכן החלון"""
        for widget in self.main_window.winfo_children():
            widget.destroy()
    
    def create_navigation_bar(self, title, back_function=None):
        """יצירת פס הניווט העליון"""
        nav_frame = tk.Frame(self.main_window, bg='#2d5a3d', height=60)
        nav_frame.pack(fill='x', padx=5, pady=5)
        nav_frame.pack_propagate(False)
        
        if back_function:
            back_btn = tk.Button(nav_frame, text="🔙 חזרה", 
                                command=back_function,
                                bg='#1a4d3a', fg='white', font=('Arial', 11, 'bold'),
                                relief='raised', bd=2)
            back_btn.pack(side='left', padx=10, pady=10)
        
        home_btn = tk.Button(nav_frame, text="🏠 תפריט ראשי", 
                            command=self.show_main_menu,
                            bg='#3d7050', fg='white', font=('Arial', 11, 'bold'),
                            relief='raised', bd=2)
        home_btn.pack(side='left', padx=10, pady=10)
        
        title_label = tk.Label(nav_frame, text=title, 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2d5a3d')
        title_label.pack(expand=True, pady=15)
        
        info_label = tk.Label(nav_frame, text="🔒 מאובטח", 
                             font=('Arial', 10), fg='#90EE90', bg='#2d5a3d')
        info_label.pack(side='right', padx=10, pady=15)
    
    def go_back(self):
        """חזרה לפונקציה הקודמת"""
        if self.navigation_stack:
            previous_function = self.navigation_stack.pop()
            previous_function()
    
    def show_main_menu(self):
        """הצגת התפריט הראשי"""
        self.clear_window()
        self.navigation_stack = []
        self.create_navigation_bar("🎖️ מערכת ניהול נתונים צבאית 🎖️")
        
        # Main content
        main_frame = tk.Frame(self.main_window, bg='#1a4d3a')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg='#3d7050', relief='raised', bd=3)
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        welcome_label = tk.Label(welcome_frame, text="🎖️ ברוכים הבאים למערכת הניהול הצבאית 🎖️", 
                                font=('Arial', 18, 'bold'), fg='white', bg='#3d7050')
        welcome_label.pack(pady=20)
        
        # Menu buttons frame - מרכזי
        buttons_main_frame = tk.Frame(main_frame, bg='#1a4d3a')
        buttons_main_frame.pack(expand=True, fill='both')
        
        # יצירת הכפתורים
        self.create_menu_buttons_horizontal(buttons_main_frame)
        
        # Footer
        footer_frame = tk.Frame(self.main_window, bg='#2d5a3d', height=40)
        footer_frame.pack(side='bottom', fill='x')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(footer_frame, text="🛡️ מערכת מאובטחת - יחידת מחשוב צה״ל", 
                            font=('Arial', 11, 'bold'), fg='#90EE90', bg='#2d5a3d')
        footer_label.pack(expand=True, pady=10)

    def create_menu_buttons_horizontal(self, parent):
        """Create menu buttons in horizontal layout with attractive icons"""
        menu_options = [
            ("🗂️ ניהול נתונים", "ניהול טבלאות, CRUD operations", self.open_crud_manager, "📊"),
            ("📊 שאילתות ודוחות", "ביצוע שאילתות ויצירת דוחות", self.open_queries, "📈"),
            ("📈 סטטיסטיקות", "הצגת סטטיסטיקות ומדדים", self.open_statistics, "📋")
        ]
        
        # יצירת frame מרכזי לכפתורים
        buttons_container = tk.Frame(parent, bg='#1a4d3a')
        buttons_container.pack(expand=True, fill='both')
        
        for i, (title, description, command, icon) in enumerate(menu_options):
            btn_frame = tk.Frame(buttons_container, bg='#3d7050', relief='raised', bd=3, cursor='hand2')
            btn_frame.grid(row=0, column=i, padx=20, pady=20, sticky='nsew', ipadx=30, ipady=30)
            
            content_frame = tk.Frame(btn_frame, bg='#3d7050')
            content_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # אייקון גדול בחלק העליון
            icon_label = tk.Label(content_frame, text=icon, 
                                font=('Arial', 48), fg='#90EE90', bg='#3d7050')
            icon_label.pack(pady=(20, 10))
            
            # כותרת הכפתור
            title_label = tk.Label(content_frame, text=title, 
                                font=('Arial', 16, 'bold'), fg='white', bg='#3d7050')
            title_label.pack(pady=(0, 5))
            
            # תיאור הכפתור
            desc_label = tk.Label(content_frame, text=description, 
                                font=('Arial', 12), fg='#E0E0E0', bg='#3d7050',
                                wraplength=200, justify='center')
            desc_label.pack(pady=(5, 15))
            
            # סטטוס זמינות
            status_label = tk.Label(content_frame, text="🟢 זמין", 
                                font=('Arial', 10, 'bold'), fg='#90EE90', bg='#3d7050')
            status_label.pack(side='bottom', pady=(0, 10))
            
            def make_command(cmd):
                return lambda event: cmd()
            
            # רשימת כל הוידג'טים לקליק
            all_widgets = [btn_frame, content_frame, icon_label, title_label, desc_label, status_label]
            
            for widget in all_widgets:
                widget.bind("<Button-1>", make_command(command))
            
            def make_hover_functions(frame, widgets):
                def on_enter(event):
                    frame.config(bg='#5a8a6a')
                    for w in widgets:
                        # שמירה על צבע האייקון הייחודי בעת ריחוף
                        if w == icon_label:
                            w.config(bg='#5a8a6a', fg='#B0FFB0')  # צבע בהיר יותר לאייקון
                        else:
                            w.config(bg='#5a8a6a')
                
                def on_leave(event):
                    frame.config(bg='#3d7050')
                    for w in widgets:
                        if w == icon_label:
                            w.config(bg='#3d7050', fg='#90EE90')  # חזרה לצבע המקורי
                        else:
                            w.config(bg='#3d7050')
                
                return on_enter, on_leave
            
            widgets = [content_frame, icon_label, title_label, desc_label, status_label]
            on_enter, on_leave = make_hover_functions(btn_frame, widgets)
            
            for widget in all_widgets:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
        
        # הגדרת משקלים לעמודות
        for i in range(3):
            buttons_container.grid_columnconfigure(i, weight=1)
        buttons_container.grid_rowconfigure(0, weight=1)

    
    def create_menu_buttons(self, parent):
        """Create menu buttons"""
        menu_options = [
            ("🗂️ ניהול נתונים", "ניהול טבלאות, CRUD operations", self.open_crud_manager),
            ("📊 שאילתות ודוחות", "ביצוע שאילתות ויצירת דוחות", self.open_queries),
            ("📈 סטטיסטיקות", "הצגת סטטיסטיקות ומדדים", self.open_statistics)
        ]
        
        for i, (title, description, command) in enumerate(menu_options):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(parent, bg='#3d7050', relief='raised', bd=3, cursor='hand2')
            btn_frame.grid(row=row, column=col, padx=20, pady=20, sticky='nsew', ipadx=30, ipady=30)
            
            content_frame = tk.Frame(btn_frame, bg='#3d7050')
            content_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            title_label = tk.Label(content_frame, text=title, 
                                  font=('Arial', 16, 'bold'), fg='white', bg='#3d7050')
            title_label.pack(pady=(10, 5))
            
            desc_label = tk.Label(content_frame, text=description, 
                                 font=('Arial', 12), fg='#E0E0E0', bg='#3d7050',
                                 wraplength=200, justify='center')
            desc_label.pack(pady=(5, 10))
            
            status_label = tk.Label(content_frame, text="🟢 זמין", 
                                   font=('Arial', 10, 'bold'), fg='#90EE90', bg='#3d7050')
            status_label.pack(side='bottom')
            
            def make_command(cmd):
                return lambda event: cmd()
            
            for widget in [btn_frame, content_frame, title_label, desc_label, status_label]:
                widget.bind("<Button-1>", make_command(command))
            
            def make_hover_functions(frame, widgets):
                def on_enter(event):
                    frame.config(bg='#5a8a6a')
                    for w in widgets:
                        w.config(bg='#5a8a6a')
                
                def on_leave(event):
                    frame.config(bg='#3d7050')
                    for w in widgets:
                        w.config(bg='#3d7050')
                
                return on_enter, on_leave
            
            widgets = [content_frame, title_label, desc_label, status_label]
            on_enter, on_leave = make_hover_functions(btn_frame, widgets)
            
            for widget in [btn_frame] + widgets:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
        
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
    
    def open_crud_manager(self):
        """פתיחת מנהל ה-CRUD"""
        self.navigation_stack.append(self.show_main_menu)
        self.show_table_selection()
    
    def show_table_selection(self):
        """הצגת בחירת טבלאות ל-CRUD"""
        self.clear_window()
        self.create_navigation_bar("🗂️ בחירת טבלה לניהול", self.go_back)
        
        main_frame = tk.Frame(self.main_window, bg='#1a4d3a')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        welcome_frame = tk.Frame(main_frame, bg='#3d7050', relief='raised', bd=3)
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        welcome_label = tk.Label(welcome_frame, text="🎖️ בחר את הטבלה לניהול 🎖️", 
                                font=('Arial', 18, 'bold'), fg='white', bg='#3d7050')
        welcome_label.pack(pady=20)
        
        tables_frame = tk.Frame(main_frame, bg='#1a4d3a')
        tables_frame.pack(expand=True, fill='both')
        
        # שימוש בהגדרות הטבלאות מהמודול המאוחד
        for i, (table_key, table_config) in enumerate(self.crud_manager.table_configs.items()):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(tables_frame, bg='#3d7050', relief='raised', bd=3, cursor='hand2')
            btn_frame.grid(row=row, column=col, padx=20, pady=20, sticky='nsew', ipadx=20, ipady=20)
            
            icon_label = tk.Label(btn_frame, text=table_config['name'][:2], 
                                 font=('Arial', 24), fg='white', bg='#3d7050')
            icon_label.pack(pady=(15, 5))
            
            name_label = tk.Label(btn_frame, text=table_config['name'][2:], 
                                 font=('Arial', 14, 'bold'), fg='white', bg='#3d7050')
            name_label.pack(pady=(0, 15))
            
            def make_table_handler(table=table_key):
                def on_click():
                    self.navigation_stack.append(self.show_table_selection)
                    self.show_crud_interface(table)
                return on_click
            
            click_handler = make_table_handler(table_key)
            
            btn_frame.bind("<Button-1>", lambda e, handler=click_handler: handler())
            for widget in btn_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, handler=click_handler: handler())
            
            def make_hover_handlers(frame, widgets):
                def on_enter(e):
                    frame.config(bg='#5a8a6a')
                    for widget in widgets:
                        widget.config(bg='#5a8a6a')
                
                def on_leave(e):
                    frame.config(bg='#3d7050')
                    for widget in widgets:
                        widget.config(bg='#3d7050')
                
                return on_enter, on_leave
            
            widgets = btn_frame.winfo_children()
            on_enter, on_leave = make_hover_handlers(btn_frame, widgets)
            
            btn_frame.bind("<Enter>", on_enter)
            btn_frame.bind("<Leave>", on_leave)
            for widget in widgets:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
        
        for i in range(2):
            tables_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            tables_frame.grid_rowconfigure(i, weight=1)
    
    def show_crud_interface(self, table_name):
        """הצגת ממשק CRUD באמצעות המודול המאוחד"""
        try:
            self.clear_window()
            table_config = self.crud_manager.table_configs[table_name]
            self.create_navigation_bar(f"🗂️ ניהול: {table_config['name']}", self.go_back)
            
            # Main content frame
            main_frame = tk.Frame(self.main_window, bg='#1a4d3a')
            main_frame.pack(expand=True, fill='both', padx=10, pady=5)
            
            # יצירת הממשק באמצעות המודול המאוחד
            self.crud_manager.create_input_section(main_frame, table_name)
            self.crud_manager.create_buttons_section(main_frame)
            self.crud_manager.create_display_section(main_frame, table_name)
            
            # רענון נתונים ראשוני
            self.crud_manager.refresh_data()
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בפתיחת מנהל הנתונים:\n{str(e)}")
    
    # שאילתות ופונקציות שאר הפונקציות נשארות כמו שהיו...
    def open_queries(self):
        """פתיחת ממשק שאילתות"""
        self.navigation_stack.append(self.show_main_menu)
        if self.advanced_queries_manager:
            self.advanced_queries_manager.show_interface()

    
    def show_queries_interface(self):
        """הצגת ממשק השאילתות - מקוצר לדוגמה"""
        self.clear_window()
        self.create_navigation_bar("📊 שאילתות ודוחות", self.go_back)
        
        content_frame = tk.Frame(self.main_window, bg='#3d7050', relief='raised', bd=3)
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        info_label = tk.Label(content_frame, text="📊 מודול שאילתות ודוחות\n\nמודול זה בפיתוח", 
                             font=('Arial', 16, 'bold'), fg='white', bg='#3d7050')
        info_label.pack(expand=True)
    
    def open_statistics(self):
        """פתיחת ממשק סטטיסטיקות"""
        self.navigation_stack.append(self.show_main_menu)
        self.show_statistics_interface()
    
    def show_statistics_interface(self):
        """הצגת סטטיסטיקות - מקוצר לדוגמה"""
        self.clear_window()
        self.create_navigation_bar("📈 סטטיסטיקות מערכת", self.go_back)
        
        try:
            main_frame = tk.Frame(self.main_window, bg='#1a4d3a')
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            content_frame = tk.Frame(main_frame, bg='#3d7050', relief='raised', bd=3)
            content_frame.pack(expand=True, fill='both')
            
            header_label = tk.Label(content_frame, text="📈 סטטיסטיקות מערכת", 
                                   font=('Arial', 18, 'bold'), fg='white', bg='#3d7050')
            header_label.pack(pady=20)
            
            stats_text = "📊 סטטיסטיקות בסיסיות:\n\n"
            
            tables = ['equipment', 'medical_event', 'requires', 'uses']
            for table_name in tables:
                try:
                    result, _ = self.db.get_table_data(table_name, 1000)
                    count = len(result)
                    stats_text += f"🔹 {table_name}: {count} רשומות\n"
                except:
                    stats_text += f"🔹 {table_name}: שגיאה בטעינה\n"
            
            stats_text += "\n🔒 מערכת פועלת תקין"
            
            stats_label = tk.Label(content_frame, text=stats_text, 
                                  font=('Arial', 14), fg='white', bg='#3d7050',
                                  justify='right')
            stats_label.pack(expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהצגת סטטיסטיקות:\n{str(e)}")
    
    def on_closing(self):
        """פעולה בעת סגירת החלון הראשי"""
        if messagebox.askokcancel("יציאה", "האם אתה בטוח שברצונך לצאת מהמערכת?"):
            self.main_window.destroy()

def main():
    """Main function to start the application"""
    try:
        app = MainApplication()
    except Exception as e:
        messagebox.showerror("שגיאה חמורה", f"שגיאה בהפעלת המערכת:\n{str(e)}")

if __name__ == "__main__":
    main()