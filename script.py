import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def parse_sql_file(sql_text):
    tables = {}
    table_defs = re.findall(r"CREATE TABLE.*?\((.*?)\);", sql_text, re.DOTALL | re.IGNORECASE)
    table_names = re.findall(r"CREATE TABLE\s+IF NOT EXISTS\s+(\w+)", sql_text, re.IGNORECASE)

    for table_name, table_body in zip(table_names, table_defs):
        lines = [line.strip().rstrip(',') for line in table_body.splitlines() if line.strip()]
        attributes = []
        primary_keys = []
        foreign_keys = []

        for line in lines:
            # PRIMARY KEY
            pk_match = re.match(r"PRIMARY KEY\s*\((.+?)\)", line, re.IGNORECASE)
            if pk_match:
                primary_keys += [x.strip() for x in pk_match.group(1).split(',')]
                continue

            # FOREIGN KEY (support multi-column and target table)
            fk_match = re.match(r"FOREIGN KEY\s*\((.+?)\)\s+REFERENCES\s+(\w+)\s*\((.+?)\)", line, re.IGNORECASE)
            if fk_match:
                local_keys = [x.strip() for x in fk_match.group(1).split(',')]
                target_table = fk_match.group(2).strip()
                target_keys = [x.strip() for x in fk_match.group(3).split(',')]
                for local_key in local_keys:
                    foreign_keys.append((local_key, target_table))
                continue

            # רגיל
            parts = line.split()
            if len(parts) >= 2:
                attributes.append(parts[0])

        tables[table_name] = {
            "attributes": attributes,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys  # now list of tuples (local_col, target_table)
        }

    return tables


def analyze_relationships(tables):
    relationships = []
    for table_name, table_data in tables.items():
        pks = set(table_data["primary_keys"])
        fks = table_data["foreign_keys"]

        for local_col, target_table in fks:
            if target_table not in tables or table_name == target_table:
                continue  # לדלג על קשרים לא הגיוניים

            target_pks = set(tables[target_table]["primary_keys"])

            if local_col in pks and len(pks) == 1:
                rel_type = "1:1 (Inheritance)"
            elif local_col in pks:
                rel_type = "Weak Entity"
            elif set(x[0] for x in fks) == pks and len(pks) >= 2:
                rel_type = "N:M (Join Table)"
            else:
                rel_type = "N:1"

            relationships.append({
                "from": table_name,
                "to": target_table,
                "key": local_col,
                "type": rel_type
            })

    return relationships


def print_erd(tables, relationships):
    print("\n📄 ישויות (טבלאות):")
    for table, data in tables.items():
        print(f"\n🧱 {table}")
        print(f"  מאפיינים: {data['attributes']}")
        print(f"  מפתח ראשי: {data['primary_keys']}")
        print(f"  מפתח זר: {[f'{k} → {t}' for k, t in data['foreign_keys']]}")

    print("\n🔗 קשרים בין ישויות:")
    for rel in relationships:
        print(f"{rel['from']} --({rel['key']})--> {rel['to']}   סוג קשר: {rel['type']}")


if __name__ == "__main__":
    sql_file_path = r"C:\Users\User\Desktop\הודיה\createTables (3).sql"  # שנה לפי הצורך

    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_text = f.read()

    tables = parse_sql_file(sql_text)
    relationships = analyze_relationships(tables)
    print_erd(tables, relationships)
