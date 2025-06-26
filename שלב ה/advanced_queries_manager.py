# advanced_queries_manager.py - FIXED Navigation
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class AdvancedQueriesManager:
    def __init__(self, db, main_window, navigation_stack):
        self.db = db
        self.main_window = main_window
        self.navigation_stack = navigation_stack
        # שמירת הפונקציה לחזרה לתפריט הראשי
        self.main_menu_function = None
    
    def set_main_menu_function(self, main_menu_func):
        """הגדרת הפונקציה לחזרה לתפריט הראשי"""
        self.main_menu_function = main_menu_func
    
    def clear_window(self):
        """ניקוי תוכן החלון"""
        for widget in self.main_window.winfo_children():
            widget.destroy()
    
    def create_navigation_bar(self, title, show_back=True):
        """יצירת פס הניווט העליון עם כפתורי ניווט"""
        nav_frame = tk.Frame(self.main_window, bg='#2d5a3d', height=80)
        nav_frame.pack(fill='x', padx=5, pady=5)
        nav_frame.pack_propagate(False)
        
        # כפתור חזרה (רק אם יש לאן לחזור)
        if show_back and self.navigation_stack:
            back_btn = tk.Button(nav_frame, text="🔙 חזרה", 
                                command=self.go_back,
                                bg='#1a4d3a', fg='white', font=('Arial', 11, 'bold'),
                                relief='raised', bd=2, width=10)
            back_btn.pack(side='left', padx=10, pady=20)
        
        # כפתור תפריט ראשי (תמיד זמין)
        if self.main_menu_function:
            home_btn = tk.Button(nav_frame, text="🏠 תפריט ראשי", 
                                command=self.go_to_main_menu,
                                bg='#3d7050', fg='white', font=('Arial', 11, 'bold'),
                                relief='raised', bd=2, width=12)
            home_btn.pack(side='left', padx=10, pady=20)
        
        # כותרת מרכזית
        title_label = tk.Label(nav_frame, text=title, 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2d5a3d')
        title_label.pack(expand=True, pady=20)
        
        # מידע מערכת
        info_label = tk.Label(nav_frame, text="🔒 מאובטח", 
                             font=('Arial', 10), fg='#90EE90', bg='#2d5a3d')
        info_label.pack(side='right', padx=10, pady=20)
    
    def go_back(self):
        """חזרה לפונקציה הקודמת"""
        if self.navigation_stack:
            previous_function = self.navigation_stack.pop()
            previous_function()
        else:
            # אם אין לאן לחזור, חזור לתפריט הראשי
            self.go_to_main_menu()
    
    def go_to_main_menu(self):
        """חזרה לתפריט הראשי"""
        if self.main_menu_function:
            # ניקוי ה-navigation stack
            self.navigation_stack.clear()
            self.main_menu_function()
    
    def show_interface(self):
        """הצגת הממשק הראשי"""
        self.clear_window()
        # ה-navigation stack כבר מכיל את הפונקציה לחזרה לתפריט הראשי
        self.create_navigation_bar("🎖️ מערכת שאילתות ופונקציות מתקדמות 🎖️", show_back=True)
        self.show_main_menu()
    
    def show_main_menu(self):
        """הצגת התפריט הראשי"""
        # Main content
        main_frame = tk.Frame(self.main_window, bg='#1a4d3a')
        main_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Welcome section
        welcome_frame = tk.Frame(main_frame, bg='#3d7050', relief='raised', bd=3)
        welcome_frame.pack(fill='x', padx=20, pady=20)
        
        welcome_label = tk.Label(welcome_frame, text="🎖️ בחר את סוג הפעולה המבוקשת 🎖️", 
                                font=('Arial', 18, 'bold'), fg='white', bg='#3d7050')
        welcome_label.pack(pady=20)
        
        # Categories grid - 3 קטגוריות
        categories_frame = tk.Frame(main_frame, bg='#1a4d3a')
        categories_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        categories = [
            ("📊 שאילתות", "שאילתות מתקדמות", self.show_select_queries),
            ("⚙️ פונקציות", "פונקציות מותאמות אישית", self.show_functions),
            ("🔧 פרוצדורות", "פרוצדורות מערכת", self.show_procedures),
        ]
        
        for i, (title, description, command) in enumerate(categories):
            self.create_category_button(categories_frame, title, description, command, i)
        
        # Configure grid
        for i in range(3):
            categories_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            categories_frame.grid_rowconfigure(i, weight=1)
    
    def create_category_button(self, parent, title, description, command, index):
        row = index // 3
        col = index % 3
        
        btn_frame = tk.Frame(parent, bg='#3d7050', relief='raised', bd=3, cursor='hand2')
        btn_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew', ipadx=20, ipady=20)
        
        # Title
        title_label = tk.Label(btn_frame, text=title, 
                              font=('Arial', 16, 'bold'), fg='white', bg='#3d7050')
        title_label.pack(pady=(15, 5))
        
        # Description
        desc_label = tk.Label(btn_frame, text=description, 
                             font=('Arial', 12), fg='#E0E0E0', bg='#3d7050',
                             wraplength=200, justify='center')
        desc_label.pack(pady=(5, 15))
        
        # Click event - תיקון חשוב כאן!
        def make_command():
            # הוספה לnavigation stack - חזרה לתפריט השאילתות
            self.navigation_stack.append(self.show_interface)
            command()
        
        btn_frame.bind("<Button-1>", lambda e: make_command())
        for widget in btn_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: make_command())
        
        # Hover effects
        def on_enter(e):
            btn_frame.config(bg='#5a8a6a')
            for widget in btn_frame.winfo_children():
                widget.config(bg='#5a8a6a')
        
        def on_leave(e):
            btn_frame.config(bg='#3d7050')
            for widget in btn_frame.winfo_children():
                widget.config(bg='#3d7050')
        
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        for widget in btn_frame.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def show_select_queries(self):
        """הצגת שאילתות בחירה"""
        queries = [
            ("מבצעים עם ציוד מעל הממוצע", self.query_operations_above_avg_equipment),
            ("מבצעים עם משימות מעל הממוצע", self.query_operations_above_avg_tasks),
            ("מבצעים ארוכי טווח", self.query_long_duration_operations),
            ("סטטיסטיקות מבצעים לפי חודש", self.query_operations_by_month)
        ]
        
        self.create_queries_interface("שאילתות בחירה", queries)
    
    def show_functions(self):
        """הצגת פונקציות"""
        functions = [
            ("סיכום פצועים לפי חיל", self.function_corps_patient_summary),
            ("מצב לוגיסטי למבצע", self.function_logistic_status_by_operation)
        ]
        
        self.create_queries_interface("פונקציות", functions)
    
    def show_procedures(self):
        """הצגת פרוצדורות"""
        procedures = [
            ("סיכום עומס רפואי לדוחות", self.procedure_summarize_medical_load),
            ("בדיקת סיכונים לוגיסטיים", self.procedure_check_logistic_risks)
        ]
        
        self.create_queries_interface("פרוצדורות", procedures)
    
    def create_queries_interface(self, title, queries_list):
        """יצירת ממשק השאילתות"""
        self.clear_window()
        self.create_navigation_bar(f"📋 {title}", show_back=True)
        
        # Header
        header_frame = tk.Frame(self.main_window, bg='#3d7050', height=50)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=f"📋 {title}", 
                               font=('Arial', 16, 'bold'), fg='white', bg='#3d7050')
        header_label.pack(expand=True, pady=15)
        
        # Content frame
        content_frame = tk.Frame(self.main_window, bg='#1a4d3a')
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Left side - queries list
        left_frame = tk.Frame(content_frame, bg='#3d7050', width=400)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        queries_label = tk.Label(left_frame, text="🔍 בחר שאילתה:", 
                                font=('Arial', 14, 'bold'), fg='white', bg='#3d7050')
        queries_label.pack(pady=10)
        
        for name, func in queries_list:
            btn = tk.Button(left_frame, text=name, command=func,
                           bg='#5a8a6a', fg='white', font=('Arial', 11),
                           width=35, height=2, relief='raised', bd=2)
            btn.pack(pady=5, padx=10)
        
        # Right side - results
        right_frame = tk.Frame(content_frame, bg='#2d5a3d')
        right_frame.pack(side='right', expand=True, fill='both')
        
        results_label = tk.Label(right_frame, text="📊 תוצאות:", 
                                font=('Arial', 14, 'bold'), fg='white', bg='#2d5a3d')
        results_label.pack(pady=10)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(right_frame, 
                                                     font=('Courier', 10),
                                                     bg='white', fg='#1a4d3a',
                                                     height=25)
        self.results_text.pack(expand=True, fill='both', padx=10, pady=10)
    
    def execute_and_display_query(self, query, title):
        """Execute query and display results"""
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"🔍 {title}\n")
            self.results_text.insert(tk.END, "="*60 + "\n\n")
            
            result, columns = self.db.execute_query(query)
            
            if result:
                # Display headers
                header_line = " | ".join(f"{col:15}" for col in columns)
                self.results_text.insert(tk.END, header_line + "\n")
                self.results_text.insert(tk.END, "-" * len(header_line) + "\n")
                
                # Display data
                for row in result:
                    row_line = " | ".join(f"{str(cell):15}" for cell in row)
                    self.results_text.insert(tk.END, row_line + "\n")
                
                self.results_text.insert(tk.END, f"\n📊 סך הכל: {len(result)} רשומות\n")
            else:
                self.results_text.insert(tk.END, "❌ לא נמצאו תוצאות\n")
                
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ שגיאה: {str(e)}\n")
    
    # Query implementations
    def query_operations_above_avg_equipment(self):
        query = """
        SELECT o.operationid, o.operationname, COUNT(r.equipmentid) as equipment_count
        FROM operation o
        JOIN requires r ON o.operationid = r.operationid
        GROUP BY o.operationid, o.operationname
        HAVING COUNT(r.equipmentid) > (
            SELECT AVG(equipment_count)
            FROM (
                SELECT COUNT(r2.equipmentid) as equipment_count
                FROM operation o2
                JOIN requires r2 ON o2.operationid = r2.operationid
                GROUP BY o2.operationid
            ) as avg_calc
        )
        ORDER BY equipment_count DESC;
        """
        self.execute_and_display_query(query, "מבצעים עם ציוד מעל הממוצע")
    
    def query_operations_above_avg_tasks(self):
        query = """
        SELECT o.operationid, o.operationname, COUNT(t.taskid) as task_count
        FROM operation o
        JOIN task t ON o.operationid = t.operationid
        GROUP BY o.operationid, o.operationname
        HAVING COUNT(t.taskid) > (
            SELECT AVG(task_count)
            FROM (
                SELECT COUNT(t2.taskid) as task_count
                FROM operation o2
                JOIN task t2 ON o2.operationid = t2.operationid
                GROUP BY o2.operationid
            ) as avg_calc
        )
        ORDER BY task_count DESC;
        """
        self.execute_and_display_query(query, "מבצעים עם משימות מעל הממוצע")
    
    def query_long_duration_operations(self):
        query = """
        SELECT operationid, operationname, startdate, enddate,
               (enddate - startdate) as duration_days
        FROM operation
        WHERE (enddate - startdate) > 500
        ORDER BY duration_days DESC;
        """
        self.execute_and_display_query(query, "מבצעים ארוכי טווח")
    
    def query_operations_by_month(self):
        query = """
        SELECT EXTRACT(MONTH FROM startdate) as month_number,
               TO_CHAR(startdate, 'Month') as month_name,
               COUNT(*) as operations_count
        FROM operation
        WHERE EXTRACT(YEAR FROM startdate) = 2023
        GROUP BY EXTRACT(MONTH FROM startdate), TO_CHAR(startdate, 'Month')
        ORDER BY month_number;
        """
        self.execute_and_display_query(query, "סטטיסטיקות מבצעים לפי חודש")
    
    # Functions
    def function_corps_patient_summary(self):
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "🔍 סיכום פצועים לפי חיל\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")

            cur = self.db.connection.cursor()
            
            # התחלת טרנזקציה
            cur.execute("BEGIN;")
            
            # קריאה לפונקציה שמחזירה refcursor
            cur.execute("SELECT get_corps_patient_summary();")
            cursor_name = cur.fetchone()[0]
            
            # שליפת כל הנתונים מהקורסור
            cur.execute(f'FETCH ALL FROM "{cursor_name}";')
            rows = cur.fetchall()
            
            # קבלת שמות העמודות
            columns = [desc[0] for desc in cur.description] if cur.description else []
            
            # סגירת הקורסור וסיום הטרנזקציה
            cur.execute(f'CLOSE "{cursor_name}";')
            cur.execute("COMMIT;")
            cur.close()

            if rows and columns:
                # הצגת כותרות
                header_line = " | ".join(f"{col:15}" for col in columns)
                self.results_text.insert(tk.END, header_line + "\n")
                self.results_text.insert(tk.END, "-" * len(header_line) + "\n")

                # הצגת הנתונים
                for row in rows:
                    row_line = " | ".join(f"{str(cell):15}" for cell in row)
                    self.results_text.insert(tk.END, row_line + "\n")

                self.results_text.insert(tk.END, f"\n📊 סך הכל: {len(rows)} רשומות\n")
            else:
                self.results_text.insert(tk.END, "❌ לא נמצאו תוצאות\n")

        except Exception as e:
            try:
                cur.execute("ROLLBACK;")
                cur.close()
            except:
                pass
            self.results_text.insert(tk.END, f"❌ שגיאה: {str(e)}\n")
    
    def function_logistic_status_by_operation(self):
        try:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "🔍 מצב לוגיסטי למבצע\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")

            cur = self.db.connection.cursor()
            
            # התחלת טרנזקציה
            cur.execute("BEGIN;")
            
            # קריאה לפונקציה שמחזירה refcursor
            cur.execute("SELECT get_logistic_status_by_operation();")
            cursor_name = cur.fetchone()[0]
            
            # שליפת כל הנתונים מהקורסור
            cur.execute(f'FETCH ALL FROM "{cursor_name}";')
            rows = cur.fetchall()
            
            # קבלת שמות העמודות
            columns = [desc[0] for desc in cur.description] if cur.description else []
            
            # סגירת הקורסור וסיום הטרנזקציה
            cur.execute(f'CLOSE "{cursor_name}";')
            cur.execute("COMMIT;")
            cur.close()

            if rows and columns:
                # הצגת כותרות
                header_line = " | ".join(f"{col:15}" for col in columns)
                self.results_text.insert(tk.END, header_line + "\n")
                self.results_text.insert(tk.END, "-" * len(header_line) + "\n")

                # הצגת הנתונים
                for row in rows:
                    row_line = " | ".join(f"{str(cell):15}" for cell in row)
                    self.results_text.insert(tk.END, row_line + "\n")

                self.results_text.insert(tk.END, f"\n📊 סך הכל: {len(rows)} רשומות\n")
            else:
                self.results_text.insert(tk.END, "❌ לא נמצאו תוצאות\n")

        except Exception as e:
            try:
                cur.execute("ROLLBACK;")
                cur.close()
            except:
                pass
            self.results_text.insert(tk.END, f"❌ שגיאה: {str(e)}\n")
    
    # Procedures
    def procedure_summarize_medical_load(self):
        if messagebox.askyesno("הפעלת פרוצדורה", "האם להפעיל פרוצדורת סיכום עומס רפואי?"):
            try:
                # הפעלת הפרוצדורה
                self.db.execute_query("CALL summarize_medical_load_to_report();")
                
                # הצגת התוצאות בטקסט
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🏥 פרוצדורת סיכום עומס רפואי הופעלה\n")
                self.results_text.insert(tk.END, "="*60 + "\n\n")
                
                # הצגת הדוחות שנוצרו
                self.show_operational_reports("עומס רפואי")
                
                messagebox.showinfo("הצלחה", "הפרוצדורה הופעלה בהצלחה!\nדוחות רפואיים נוצרו בטבלת operational_report")
                
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בהפעלת הפרוצדורה:\n{str(e)}")
    
    def procedure_check_logistic_risks(self):
        if messagebox.askyesno("הפעלת פרוצדורה", "האם להפעיל פרוצדורת בדיקת סיכונים לוגיסטיים?"):
            try:
                # הפעלת הפרוצדורה
                self.db.execute_query("CALL check_logistic_risk_operations();")
                
                # הצגת התוצאות בטקסט
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "📊 פרוצדורת בדיקת סיכונים לוגיסטיים הופעלה\n")
                self.results_text.insert(tk.END, "="*60 + "\n\n")
                
                # הצגת הדוחות שנוצרו
                self.show_operational_reports("לוגיסטי")
                
                messagebox.showinfo("הצלחה", "הפרוצדורה הופעלה בהצלחה!\nדוחות לוגיסטיים נוצרו בטבלת operational_report")
                
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בהפעלת הפרוצדורה:\n{str(e)}")
    
    def show_operational_reports(self, report_type):
        """הצגת הדוחות שנוצרו בטבלת operational_report"""
        try:
            # שאילתה לקבלת הדוחות האחרונים
            if report_type == "עומס רפואי":
                query = """
                SELECT reportid, operationid, date, content
                FROM operational_report
                WHERE content ILIKE '%עומס רפואי%'
                ORDER BY date DESC, reportid DESC
                LIMIT 10;
                """
            else:  # לוגיסטי
                query = """
                SELECT reportid, operationid, date, content
                FROM operational_report
                WHERE content ILIKE '%לוגיסטי%'
                ORDER BY date DESC, reportid DESC
                LIMIT 10;
                """
            
            result, columns = self.db.execute_query(query)
            
            if result:
                self.results_text.insert(tk.END, f"📋 דוחות {report_type} שנוצרו:\n\n")
                
                # הצגת כותרות
                header_line = " | ".join(f"{col:15}" for col in columns)
                self.results_text.insert(tk.END, header_line + "\n")
                self.results_text.insert(tk.END, "-" * len(header_line) + "\n")
                
                # הצגת הנתונים
                for row in result:
                    row_line = " | ".join(f"{str(cell):15}" for cell in row)
                    self.results_text.insert(tk.END, row_line + "\n")
                
                self.results_text.insert(tk.END, f"\n📊 סך הכל: {len(result)} דוחות {report_type}\n")
            else:
                self.results_text.insert(tk.END, f"❌ לא נמצאו דוחות {report_type}\n")
                
        except Exception as e:
            self.results_text.insert(tk.END, f"❌ שגיאה בהצגת דוחות: {str(e)}\n")

    # Additional utility functions and error handling
    def show_error_message(self, title, message):
        """הצגת הודעת שגיאה"""
        messagebox.showerror(title, message)
    
    def show_success_message(self, title, message):
        """הצגת הודעת הצלחה"""
        messagebox.showinfo(title, message)
    
    def show_warning_message(self, title, message):
        """הצגת הודעת אזהרה"""
        messagebox.showwarning(title, message)