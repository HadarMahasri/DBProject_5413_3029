# crud_manager.py - מודול CRUD נקי עם הדגשה באימוג'ים
import tkinter as tk
from tkinter import ttk, messagebox

class CRUDManager:
    def __init__(self, db):
        self.db = db
        self.current_table = None
        self.current_data = []
        self.input_entries = {}
        self.original_primary_key_values = {}
        self.tree = None
        self.highlighted_items = []  # רשימת פריטים מודגשים
        
        # הגדרות טבלאות מרכזיות
        self.table_configs = {
            'equipment': {
                'name': '🔫 ציוד צבאי',
                'fields': ['equipmentid', 'name', 'quantity', 'equipment_type'],
                'display_names': ['מזהה ציוד', 'שם הציוד', 'כמות', 'סוג ציוד'],
                'primary_key': ('equipmentid', 'equipment_type')
            },
            'medical_event': {
                'name': '🚑 אירועים רפואיים',
                'fields': ['event_id', 'event_location', 'number_of_injured', 'event_date', 'operation_id'],
                'display_names': ['מזהה אירוע', 'מיקום', 'מספר פצועים', 'תאריך', 'מזהה מבצע'],
                'primary_key': 'event_id'
            },
            'uses': {
                'name': '🏥 דרישות ציוד רפואי',
                'fields': ['equipment_id', 'treatment_id', 'equipment_type'],
                'display_names': ['מזהה ציוד', 'מזהה טיפול', 'סוג ציוד'],
                'primary_key': ('equipment_id', 'treatment_id')
            },
            'requires': {
                'name': '⚔️ דרישות ציוד צבאי',
                'fields': ['equipmentid','operationid', 'requiredquantity','equipment_type'],
                'display_names': ['מזהה ציוד','מזהה מבצע', 'כמות ציוד','סוג ציוד'],
                'primary_key': ('operationid', 'equipmentid')
            }
        }


    def force_combo_selection(self):
        """מאפשר שמירה של ערכים שנבחרו בקומבובוקסים"""
        print("🔧 מאלץ עדכון קומבובוקסים...")
        for field_name, entry in self.input_entries.items():
            if isinstance(entry, ttk.Combobox):
                current_value = entry.get()
                print(f"  📋 {field_name}: ערך נוכחי = '{current_value}'")
                if current_value:
                    # וידוא שהערך נשמר
                    entry.selection_clear()
                    entry.set(current_value)
                    print(f"     ✅ עודכן ל-'{entry.get()}'")

        # פונקציה נוספת לבדיקת ערכי קומבובוקס
    def debug_combo_values(self):
        """פונקציה לדיבוג ערכי קומבובוקסים"""
        print("\n🔍 דיבוג ערכי קומבובוקסים:")
        for field_name, widget in self.input_entries.items():
            if isinstance(widget, ttk.Combobox):
                current = widget.get()
                available = list(widget['values'])
                print(f"  📋 {field_name}:")
                print(f"      ערך נוכחי: '{current}'")
                print(f"      ערכים זמינים: {available}")
                print(f"      האם תקף: {current in available}")

    # פונקציה לבדיקה ידנית של הערכים
    def test_update_values(self):
        """פונקציה לבדיקה ידנית של הערכים לפני עדכון"""
        print("\n🧪 בדיקת ערכים לפני עדכון:")
        config = self.table_configs[self.current_table]
        
        for field in config['fields']:
            widget = self.input_entries[field]
            value = widget.get()
            print(f"  📄 {field}: '{value}' (סוג: {type(widget).__name__})")
            
            if isinstance(widget, ttk.Combobox):
                available = list(widget['values'])
                valid = value in available if value else True
                print(f"      זמינים: {available}")
                print(f"      תקף: {valid}")

    def update_record(self):
        print("🔄 מתחיל עדכון רשומה...")
        
        # קודם כל - נאלץ את כל הקומבובוקסים לשמור את הערכים שלהם
        self.force_combo_selection()
        
        config = self.table_configs[self.current_table]
        primary_key = config['primary_key']

        if not self.original_primary_key_values:
            messagebox.showwarning("שגיאה", "לא נבחרה רשומה לעדכון.")
            return

        print(f"🔑 מפתח ראשי: {primary_key}")
        print(f"🔑 ערכי מפתח מקוריים: {self.original_primary_key_values}")

        # בניית תנאי WHERE לפי מפתח המקורי
        where_conditions = []
        where_values = []

        if isinstance(primary_key, tuple):
            for key_field in primary_key:
                value = self.original_primary_key_values.get(key_field)
                if not value:
                    messagebox.showwarning("שגיאה", f"אין ערך למפתח {key_field}")
                    return
                where_conditions.append(f"{key_field} = %s")
                where_values.append(value)
        else:
            value = self.original_primary_key_values.get(primary_key)
            if not value:
                messagebox.showwarning("שגיאה", f"אין ערך למפתח {primary_key}")
                return
            where_conditions.append(f"{primary_key} = %s")
            where_values.append(value)

        # איסוף כל השדות לעדכון - כולל מפתח ראשי!
        update_fields = []
        update_values = []
        new_primary_key_values = {}

        print(f"\n📝 בודק שדות לעדכון:")
        for field in config['fields']:
            widget = self.input_entries[field]
            value = widget.get().strip()
            
            print(f"  🔍 שדה {field}:")
            print(f"      📋 סוג וידג'ט: {type(widget).__name__}")
            print(f"      📄 ערך: '{value}'")
            
            # בדיקה אם זה שדה מפתח ראשי
            is_primary_key_field = field in (primary_key if isinstance(primary_key, tuple) else [primary_key])
            
            # טיפול מיוחד בקומבובוקסים
            if isinstance(widget, ttk.Combobox):
                available_values = list(widget['values'])
                print(f"      📑 ערכים זמינים: {available_values}")
                
                if value:
                    if value in available_values:
                        # עדכון גם שדות מפתח ראשי
                        update_fields.append(f"{field} = %s")
                        update_values.append(value)
                        if is_primary_key_field:
                            new_primary_key_values[field] = value
                            print(f"      🔑 מפתח ראשי חדש: {value}")
                        else:
                            print(f"      ✅ נוסף לעדכון: {value}")
                    else:
                        print(f"      ❌ ערך לא תקף!")
                        messagebox.showwarning("שגיאה", 
                            f"הערך '{value}' שנבחר לשדה '{field}' אינו תקף.\n"
                            f"ערכים מותרים: {available_values}")
                        return
                else:
                    if is_primary_key_field:
                        print(f"      ⚠️ מפתח ראשי ריק - משתמש בערך המקורי")
                        # אם מפתח ראשי ריק, נשתמש בערך המקורי
                        original_value = self.original_primary_key_values.get(field)
                        if original_value:
                            update_fields.append(f"{field} = %s")
                            update_values.append(original_value)
                            new_primary_key_values[field] = original_value
                    else:
                        print(f"      ⚪ ערך ריק - לא מעדכן")
            else:
                # שדה רגיל
                if value:
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
                    if is_primary_key_field:
                        new_primary_key_values[field] = value
                        print(f"      🔑 מפתח ראשי חדש: {value}")
                    else:
                        print(f"      ✅ נוסף לעדכון: {value}")
                else:
                    if is_primary_key_field:
                        print(f"      ⚠️ מפתח ראשי ריק - משתמש בערך המקורי")
                        # אם מפתח ראשי ריק, נשתמש בערך המקורי
                        original_value = self.original_primary_key_values.get(field)
                        if original_value:
                            update_fields.append(f"{field} = %s")
                            update_values.append(original_value)
                            new_primary_key_values[field] = original_value
                    else:
                        print(f"      ⚪ ערך ריק - לא מעדכן")

        if not update_fields:
            print("❌ אין שדות לעדכון!")
            messagebox.showwarning("שגיאה", "יש להזין לפחות שדה אחד לעדכון.")
            return

        print(f"\n🔄 מבצע עדכון:")
        print(f"   📋 שדות: {[f.split(' = ')[0] for f in update_fields]}")
        print(f"   📊 ערכים: {update_values}")
        print(f"   🔑 תנאי WHERE: {where_conditions}")
        print(f"   🎯 ערכי WHERE: {where_values}")
        print(f"   🆕 מפתח ראשי חדש: {new_primary_key_values}")

        try:
            if isinstance(primary_key, tuple):
                rows_affected, _ = self.db.update_record_composite(
                    self.current_table, list(primary_key), where_values,
                    [f.split(' = ')[0] for f in update_fields], update_values
                )
            else:
                rows_affected, _ = self.db.update_record(
                    self.current_table, primary_key, where_values[0],
                    [f.split(' = ')[0] for f in update_fields], update_values
                )

            print(f"📈 רשומות מושפעות: {rows_affected}")

            if rows_affected > 0:
                print("✅ עדכון הושלם בהצלחה!")
                self.show_success_message("✅ הרשומה עודכנה בהצלחה!")
                
                # עדכון המפתח המקורי לחדש
                self.original_primary_key_values.update(new_primary_key_values)
                
                # הדגשה לפי המפתח החדש
                if isinstance(primary_key, tuple):
                    pk_for_highlight = tuple(new_primary_key_values.get(pk, where_values[i]) 
                                        for i, pk in enumerate(primary_key))
                else:
                    pk_for_highlight = new_primary_key_values.get(primary_key, where_values[0])
                
                print(f"🎯 מדגיש רשומה: {pk_for_highlight}")
                self.refresh_data(pk_for_highlight, "updated")
            else:
                print("⚠️ לא נמצאה רשומה לעדכון")
                messagebox.showwarning("אזהרה", "לא נמצאה רשומה לעדכון.")
                
        except Exception as e:
            print(f"💥 שגיאה בעדכון: {str(e)}")
            messagebox.showerror("שגיאה", f"שגיאה בעדכון הרשומה:\n{str(e)}")


    # פונקציה נוספת לטיפול טוב יותר בקומבובוקסים
    def create_input_section(self, parent, table_name):
        """יצירת סקציית הזנת נתונים - עם טיפול משופר בקומבובוקסים"""
        config = self.table_configs[table_name]
        self.current_table = table_name
        
        # Input header
        input_header = tk.Frame(parent, bg='#3d7050', height=40)
        input_header.pack(fill='x', padx=10, pady=(10, 0))
        input_header.pack_propagate(False)
        
        header_label = tk.Label(input_header, text="📝 הזנת נתונים", 
                            font=('Arial', 14, 'bold'), fg='white', bg='#3d7050')
        header_label.pack(expand=True, pady=10)
        
        # Input fields frame
        input_frame = tk.Frame(parent, bg='#5a8a6a', relief='raised', bd=2)
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        fields_frame = tk.Frame(input_frame, bg='#5a8a6a')
        fields_frame.pack(fill='x', padx=20, pady=15)
        
        self.input_entries = {}
        
        # יצירת שדות קלט
        for i, (field, display_name) in enumerate(zip(config['fields'], config['display_names'])):
            row = i // 3
            col = i % 3
            
            field_frame = tk.Frame(fields_frame, bg='#5a8a6a')
            field_frame.grid(row=row, column=col, padx=10, pady=8, sticky='ew')
            
            label = tk.Label(field_frame, text=f"{display_name}:", 
                        font=('Arial', 11, 'bold'), fg='white', bg='#5a8a6a')
            label.pack(anchor='w')
            
            # יצירת ComboBox עבור foreign keys
            combo_options = self._get_foreign_key_options(table_name, field)
            
            if combo_options:
                combo = ttk.Combobox(field_frame, values=combo_options, font=('Arial', 11), width=20)
                combo.pack(fill='x', pady=2)
                
                # הוספת event handlers לקומבובוקס
                def on_combo_select(event, combo_widget=combo):
                    """מטפל בבחירה בקומבובוקס"""
                    combo_widget.selection_clear()
                    
                def on_combo_focus_out(event, combo_widget=combo):
                    """מטפל ביציאה מהקומבובוקס"""
                    value = combo_widget.get()
                    if value and value not in combo_widget['values']:
                        # אם הערך לא בתוך הרשימה, נאפס אותו
                        combo_widget.set('')
                
                combo.bind('<<ComboboxSelected>>', on_combo_select)
                combo.bind('<FocusOut>', on_combo_focus_out)
                
                self.input_entries[field] = combo
            else:
                entry = tk.Entry(field_frame, font=('Arial', 11), width=20,
                                bg='white', fg='#1a4d3a', relief='solid', bd=1)
                entry.pack(fill='x', pady=2)
                self.input_entries[field] = entry
        
        # Configure grid weights
        for i in range(3):
            fields_frame.grid_columnconfigure(i, weight=1)
    
    def _get_foreign_key_options(self, table_name, field):
        """קבלת אפשרויות עבור foreign keys"""
        try:
            foreign_key_mappings = {
                'medical_event': {
                    'operation_id': "SELECT DISTINCT operationid FROM operation ORDER BY operationid"
                },
                'uses': {
                    'equipment_id': "SELECT DISTINCT equipmentid FROM equipment ORDER BY equipmentid",
                    'treatment_id': "SELECT DISTINCT treatment_id FROM treatment ORDER BY treatment_id"
                },
                'requires': {
                    'equipmentid': "SELECT DISTINCT equipmentid FROM equipment ORDER BY equipmentid",
                    'operationid': "SELECT DISTINCT operationid FROM operation ORDER BY operationid"
                }
            }
            
            if table_name in foreign_key_mappings and field in foreign_key_mappings[table_name]:
                query = foreign_key_mappings[table_name][field]
                ref_data, _ = self.db.execute_query(query)
                return [str(row[0]) for row in ref_data if row[0] is not None]
            
        except Exception as e:
            print(f"שגיאה בטעינת foreign key options לשדה {field}: {e}")
        
        return []
    
    def create_buttons_section(self, parent):
        """יצירת סקציית הכפתורים"""
        buttons_frame = tk.Frame(parent, bg='#1a4d3a', height=70)
        buttons_frame.pack(fill='x', padx=10, pady=5)
        buttons_frame.pack_propagate(False)
        
        buttons_data = [
            ("➕ הוסף", self.add_record, '#2d5a3d'),
            ("✏️ עדכן", self.update_record, '#3d7050'),
            ("🗑️ מחק", self.delete_record, '#8b4513'),
            ("🔍 חפש", self.search_records, '#4682b4'),
            ("🔄 רענן", self.refresh_data_simple, '#5a8a6a'),
        ]
        
        for i, (text, command, color) in enumerate(buttons_data):
            btn = tk.Button(buttons_frame, text=text, command=command,
                           bg=color, fg='white', font=('Arial', 12, 'bold'),
                           width=12, height=2, relief='raised', bd=3,
                           cursor='hand2')
            btn.grid(row=0, column=i, padx=8, pady=15)
        
        for i in range(len(buttons_data)):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def create_display_section(self, parent, table_name):
        """יצירת סקציית תצוגת הנתונים"""
        config = self.table_configs[table_name]
        
        # Header
        display_header = tk.Frame(parent, bg='#2d5a3d', height=40)
        display_header.pack(fill='x', padx=10, pady=(10, 0))
        display_header.pack_propagate(False)
        
        header_label = tk.Label(display_header, text="📊 תצוגת נתונים", 
                               font=('Arial', 14, 'bold'), fg='white', bg='#2d5a3d')
        header_label.pack(side='left', padx=20, pady=10)
        
        self.record_count_label = tk.Label(display_header, text="0 רשומות", 
                                          font=('Arial', 12), fg='#90EE90', bg='#2d5a3d')
        self.record_count_label.pack(side='right', padx=20, pady=10)
        
        # Data display frame
        display_frame = tk.Frame(parent, bg='#5a8a6a', relief='raised', bd=2)
        display_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))
        
        tree_frame = tk.Frame(display_frame, bg='#5a8a6a')
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=config['display_names'], show='headings')
        
        # Configure columns
        for i, display_name in enumerate(config['display_names']):
            self.tree.heading(f"#{i+1}", text=display_name)
            self.tree.column(f"#{i+1}", width=150, anchor='center')
        
        # Treeview styling פשוט
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background='white',
                       foreground='#1a4d3a',
                       rowheight=30,  
                       fieldbackground='white',
                       font=('Arial', 10))
        style.configure("Treeview.Heading",
                       background='#3d7050',
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        v_scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        h_scrollbar.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(expand=True, fill='both')
        self.tree.bind('<Double-1>', self.on_record_select)
    
    # ================== פונקציות הדגשה עם אימוג'ים ==================
    
    def highlight_item(self, item_id, action_type):
        """הדגשת פריט ברשימה עם אימוג'ים"""
        if item_id not in self.highlighted_items:
            self.highlighted_items.append(item_id)
            
            try:
                # קבלת הערך הראשון והוספת אימוג'י
                current_value = self.tree.set(item_id, '#1')
                
                if action_type == "new":
                    # רשומה חדשה - אימוג'י ירוק
                    new_value = "🆕 " + str(current_value)
                elif action_type == "updated":
                    # רשומה מעודכנת - אימוג'י עריכה
                    new_value = "✏️ " + str(current_value)
                elif action_type == "selected":
                    # רשומה נבחרת - אימוג'י כחול
                    new_value = "👆 " + str(current_value)
                else:
                    new_value = "⭐ " + str(current_value)
                
                # עדכון הערך בעמודה הראשונה
                self.tree.set(item_id, '#1', new_value)
                
                # גלילה לפריט המודגש
                self.tree.see(item_id)
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)
                
                # הסרת ההדגשה אחרי זמן מוגדר
                duration = 3000 if action_type == "selected" else 4000
                self.tree.after(duration, lambda: self.remove_highlight(item_id))
                
            except Exception as e:
                pass
    
    def remove_highlight(self, item_id):
        """הסרת הדגשה מפריט"""
        try:
            if item_id in self.highlighted_items:
                self.highlighted_items.remove(item_id)
                
                # קבלת הערך הנוכחי והסרת האימוג'י
                current_value = str(self.tree.set(item_id, '#1'))
                
                # הסרת האימוג'ים הידועים
                emojis_to_remove = ["🆕 ", "✏️ ", "👆 ", "⭐ "]
                
                for emoji in emojis_to_remove:
                    if current_value.startswith(emoji):
                        new_value = current_value[len(emoji):]
                        self.tree.set(item_id, '#1', new_value)
                        break
                        
        except Exception:
            pass
    
    def show_success_message(self, message):
        """הצגת הודעת הצלחה קצרה"""
        try:
            success_window = tk.Toplevel()
            success_window.title("הודעה")
            success_window.geometry("300x100")
            success_window.configure(bg='#2d5a3d')
            success_window.resizable(False, False)
            
            # מיקום יחסי למסך
            success_window.transient()
            
            # הודעה
            label = tk.Label(success_window, text=message, 
                            font=('Arial', 12, 'bold'), fg='white', bg='#2d5a3d')
            label.pack(expand=True)
            
            # סגירה אוטומטית אחרי 2 שניות
            success_window.after(2000, success_window.destroy)
            
        except Exception:
            pass
    
    # ================== פעולות CRUD ==================
    
    def add_record(self):
        """הוספת רשומה חדשה עם הדגשה"""
        config = self.table_configs[self.current_table]
        values = []
        
        for field in config['fields']:
            value = self.input_entries[field].get().strip()
            values.append(value if value else None)
        
        try:
            # הוספת הרשומה למסד הנתונים
            self.db.insert_record(self.current_table, config['fields'], values)
            
            # הצגת הודעת הצלחה
            self.show_success_message("✅ הרשומה נוספה בהצלחה!")
            
            # קביעת המפתח להדגשה
            pk_field = config['primary_key']
            if isinstance(pk_field, tuple):
                # מפתח מורכב
                highlight_pk = tuple(values[config['fields'].index(pk)] for pk in pk_field)
            else:
                # מפתח יחיד
                highlight_pk = values[config['fields'].index(pk_field)]
            
            # רענון עם הדגשה של רשומה חדשה
            self.refresh_data(highlight_pk, "new")
            
            # ניקוי השדות
            self.clear_inputs()
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת הרשומה:\n{str(e)}")
    
        
    def delete_record(self):
        """מחיקת רשומה"""
        config = self.table_configs[self.current_table]
        primary_key = config['primary_key']
        
        # קבלת ערכי המפתח
        if isinstance(primary_key, tuple):
            pk_values = []
            for pk_field in primary_key:
                value = self.input_entries[pk_field].get().strip()
                if not value:
                    messagebox.showwarning("שגיאה", f"אנא הזן {pk_field}")
                    return
                pk_values.append(value)
            pk_display = " + ".join(pk_values)
        else:
            pk_value = self.input_entries[primary_key].get().strip()
            if not pk_value:
                messagebox.showwarning("שגיאה", f"אנא הזן {primary_key}")
                return
            pk_values = [pk_value]
            pk_display = pk_value
        
        # אישור מחיקה
        if not messagebox.askyesno("⚠️ אישור מחיקה", 
            f"האם אתה בטוח שברצונך למחוק את הרשומה {pk_display}?"):
            return
        
        try:
            if isinstance(primary_key, tuple):
                # מפתח מורכב
                conditions = []
                for pk_field, pk_val in zip(primary_key, pk_values):
                    conditions.append(f"{pk_field} = %s")
                
                where_clause = " AND ".join(conditions)
                query = f"DELETE FROM {self.current_table} WHERE {where_clause}"
                rows_affected, _ = self.db.execute_query(query, pk_values)
            else:
                # מפתח יחיד
                rows_affected, error = self.db.delete_record_safe(
                    self.current_table, primary_key, pk_values[0]
                )
                if error == "יש תלויות":
                    return
            
            if rows_affected > 0:
                self.show_success_message("✅ הרשומה נמחקה בהצלחה!")
                self.refresh_data()
                self.clear_inputs()
            else:
                messagebox.showwarning("אזהרה", "לא נמצאה רשומה למחיקה")
                
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה במחיקת הרשומה:\n{str(e)}")
    
    def search_records(self):
        """חיפוש רשומות"""
        config = self.table_configs[self.current_table]
        conditions = []
        values = []
        
        for field in config['fields']:
            value = self.input_entries[field].get().strip()
            if value:
                if field.endswith('_id') or field == 'equipmentid':
                    conditions.append(f"{field} = %s")
                    values.append(value)
                else:
                    conditions.append(f"CAST({field} AS TEXT) ILIKE %s")
                    values.append(f"%{value}%")
        
        if not conditions:
            messagebox.showwarning("שגיאה", "אנא הזן לפחות שדה אחד לחיפוש")
            return
        
        try:
            results, columns = self.db.search_records(self.current_table, conditions, values)
            
            # עדכון התצוגה
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for row in results:
                self.tree.insert('', 'end', values=row)
            
            self.record_count_label.config(text=f"{len(results)} תוצאות")
            
            # הצגת הודעה
            if results:
                self.show_success_message(f"🔍 נמצאו {len(results)} תוצאות")
            else:
                messagebox.showinfo("תוצאות חיפוש", "לא נמצאו תוצאות התואמות לחיפוש")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בחיפוש:\n{str(e)}")
    
    def check_dependencies(self):
        """בדיקת תלויות של רשומה"""
        config = self.table_configs[self.current_table]
        primary_key = config['primary_key']
        
        if isinstance(primary_key, tuple):
            messagebox.showinfo("מידע", "בדיקת תלויות זמינה רק עבור מפתחות יחידים")
            return
        
        pk_value = self.input_entries[primary_key].get().strip()
        if not pk_value:
            messagebox.showwarning("שגיאה", f"אנא הזן {primary_key}")
            return
        
        try:
            related_records = self.db.check_related_records(self.current_table, primary_key, pk_value)
            
            if related_records:
                deps_text = f"🔗 תלויות עבור רשומה {pk_value}:\n\n"
                total_records = 0
                
                for table, count in related_records.items():
                    deps_text += f"📋 {table}: {count} רשומות\n"
                    total_records += count
                
                deps_text += f"\n📊 סך הכל: {total_records} רשומות תלויות"
                deps_text += f"\n\n⚠️ במחיקה - כל הרשומות האלה יימחקו!"
                
                messagebox.showwarning("🔗 תלויות נמצאו", deps_text)
            else:
                messagebox.showinfo("✅ אין תלויות", 
                    f"הרשומה {pk_value} אינה משמשת בטבלאות אחרות.\n"
                    f"ניתן למחוק בבטחה.")
                
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בבדיקת תלויות:\n{str(e)}")
    
    def refresh_data(self, highlight_pk=None, highlight_type="updated"):
        """רענון נתונים עם אפשרות להדגיש רשומה מסוימת"""
        try:
            result, columns = self.db.get_table_data(self.current_table)
            self.current_data = result
            
            # Clear previous highlights
            self.highlighted_items = []
            
            # Clear and populate tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            config = self.table_configs[self.current_table]
            pk_field = config['primary_key']
            
            for row in result:
                item_id = self.tree.insert('', 'end', values=row)
                
                # אם צריך להדגיש רשומה מסוימת
                if highlight_pk is not None:
                    should_highlight = False
                    
                    if isinstance(pk_field, tuple):
                        # מפתח מורכב
                        pk_indices = [config['fields'].index(pk) for pk in pk_field]
                        current_pk = tuple(str(row[i]) for i in pk_indices)
                        if isinstance(highlight_pk, tuple):
                            target_pk = tuple(str(val) for val in highlight_pk)
                        else:
                            target_pk = highlight_pk
                        should_highlight = current_pk == target_pk
                    else:
                        # מפתח יחיד
                        pk_index = config['fields'].index(pk_field)
                        should_highlight = str(row[pk_index]) == str(highlight_pk)
                    
                    if should_highlight:
                        # השהיה קצרה כדי שהעמודה תטען לפני ההדגשה
                        self.tree.after(100, lambda item=item_id, htype=highlight_type: self.highlight_item(item, htype))
            
            # Update count
            self.record_count_label.config(text=f"{len(result)} רשומות")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת נתונים:\n{str(e)}")
    
    def refresh_data_simple(self):
        """רענון נתונים פשוט ללא הדגשות"""
        self.refresh_data()
    
    def clear_inputs(self):
        """ניקוי שדות הקלט"""
        try:
            for entry in self.input_entries.values():
                if hasattr(entry, 'delete'):
                    entry.delete(0, tk.END)
            
            # הסרת בחירה מהטבלה
            for item in self.tree.selection():
                self.tree.selection_remove(item)
            
            # איפוס ערכי המפתח המקוריים
            self.original_primary_key_values = {}
            
        except Exception as e:
            pass
    
    def on_record_select(self, event):
        """טעינת רשומה נבחרת עם הדגשה זמנית"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            config = self.table_configs[self.current_table]
            self.original_primary_key_values = {}
            
            # טעינת הערכים לשדות
            for i, field in enumerate(config['fields']):
                if i < len(values):
                    self.input_entries[field].delete(0, tk.END)
                    self.input_entries[field].insert(0, str(values[i]))
                    
                    # שמירת ערכי המפתח המקוריים
                    if field in (config['primary_key'] if isinstance(config['primary_key'], (tuple, list)) else [config['primary_key']]):
                        self.original_primary_key_values[field] = str(values[i])
            
            # הדגשה זמנית של הרשומה הנבחרת
            selected_item = selection[0]
            self.highlight_item(selected_item, "selected")