import os
import json
import pandas as pd
import random
from faker import Faker

fake = Faker()

# -------------------------
# ROW CONFIGURATION
# -------------------------
TABLE_ROW_COUNTS = {
    "users": 5000,      # change to 5000 later
    "request": 20000     # change to 20000 later
}

# -------------------------
# LOAD SCHEMA
# -------------------------
def load_schema():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "db_info.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# OUTPUT FOLDER
# -------------------------
def setup_output_folder():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "mock_db")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# -------------------------
# GENERIC VALUE GENERATOR
# -------------------------
def generate_value_from_type(col_name, col_type, i):
    col = col_name.lower()
    dtype = col_type.lower()

    if col == "user_id":
        return f"USR{i:05d}"

    if col == "req_id":
        return f"REQ{i:06d}"

    if col.endswith("_id"):
        return i

    if col == "full_name":
        return fake.name()

    if col == "first_name":
        return fake.first_name()

    if col == "middle_name":
        return fake.first_name()

    if col == "last_name":
        return fake.last_name()

    if "email" in col:
        return fake.email()

    if "phone" in col:
        return fake.phone_number()

    if col == "gender":
        return random.choice(["Male", "Female", "Other"])

    if col.startswith("language_"):
        return random.choice(["English", "Spanish", "Hindi", "French"])

    if "city" in col:
        return fake.city()

    if "state" in col:
        return fake.state()

    if "country" in col:
        return fake.country()

    if "addr" in col:
        return fake.street_address()

    if "zip" in col:
        return fake.postcode()

    if col == "time_zone":
        return random.choice([
            "America/Chicago",
            "America/New_York",
            "America/Los_Angeles",
            "Asia/Kolkata",
            "UTC"
        ])

    if col == "profile_picture_path":
        return f"/images/profile_{i}.jpg"

    if col == "req_doc_link":
        return fake.url()

    if col == "promotion_wizard_stage":
        return random.randint(1, 5)

    if col == "external_auth_provider":
        return random.choice(["google", "facebook", "apple", "local"])

    if col == "dob":
        return fake.date_of_birth(minimum_age=18, maximum_age=80)

    if "date" in col or "time" in col:
        return fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")

    if "boolean" in dtype:
        return random.choice([True, False])

    if "integer" in dtype or "bigint" in dtype or "small int" in dtype or "int" in dtype:
        return random.randint(1, 100)

    if "numeric" in dtype:
        return round(random.uniform(1, 100), 2)

    if "json" in dtype:
        return "{}"

    if "text" in dtype:
        return fake.sentence()

    return fake.word()

# -------------------------
# GENERATE GENERIC TABLE
# -------------------------
def generate_table(table_name, tables):
    columns = tables[table_name]["columns"]
    rows = TABLE_ROW_COUNTS.get(table_name, 100)

    data = []

    for i in range(1, rows + 1):
        row = {}

        for col in columns:
            col_name = col["name"]
            col_type = col["type"]
            row[col_name] = generate_value_from_type(col_name, col_type, i)

        data.append(row)

    return pd.DataFrame(data)

# -------------------------
# HELPER
# -------------------------
def get_column_values(df, column_name):
    if column_name in df.columns:
        return df[column_name].dropna().tolist()
    return []

# -------------------------
# GENERATE USERS TABLE
# -------------------------
def generate_users_table(tables, country_df, state_df, user_status_df, user_category_df):
    columns = tables["users"]["columns"]
    rows = TABLE_ROW_COUNTS.get("users", 100)

    country_ids = get_column_values(country_df, "country_id")
    state_ids = get_column_values(state_df, "state_id")
    user_status_ids = get_column_values(user_status_df, "user_status_id")
    user_category_ids = get_column_values(user_category_df, "user_category_id")

    data = []

    for i in range(1, rows + 1):
        row = {}

        first_name = fake.first_name()
        middle_name = fake.first_name()
        last_name = fake.last_name()

        for col in columns:
            col_name = col["name"]
            col_type = col["type"]

            if col_name == "user_id":
                row[col_name] = f"USR{i:05d}"
            elif col_name == "country_id":
                row[col_name] = random.choice(country_ids) if country_ids else random.randint(1, 100)
            elif col_name == "state_id":
                row[col_name] = random.choice(state_ids) if state_ids else f"ST{i:03d}"
            elif col_name == "user_status_id":
                row[col_name] = random.choice(user_status_ids) if user_status_ids else random.randint(1, 10)
            elif col_name == "user_category_id":
                row[col_name] = random.choice(user_category_ids) if user_category_ids else random.randint(1, 10)
            elif col_name == "first_name":
                row[col_name] = first_name
            elif col_name == "middle_name":
                row[col_name] = middle_name
            elif col_name == "last_name":
                row[col_name] = last_name
            elif col_name == "full_name":
                row[col_name] = f"{first_name} {middle_name} {last_name}"
            else:
                row[col_name] = generate_value_from_type(col_name, col_type, i)

        data.append(row)

    return pd.DataFrame(data)

# -------------------------
# GENERATE REQUEST TABLE
# -------------------------
def generate_request_table(
    tables,
    users_df,
    request_for_df,
    request_isleadvol_df,
    help_categories_df,
    request_type_df,
    request_priority_df,
    request_status_df
):
    columns = tables["request"]["columns"]
    rows = TABLE_ROW_COUNTS.get("request", 100)

    user_ids = get_column_values(users_df, "user_id")
    req_for_ids = get_column_values(request_for_df, "req_for_id")
    req_islead_ids = get_column_values(request_isleadvol_df, "req_islead_id")
    cat_ids = get_column_values(help_categories_df, "cat_id")
    req_type_ids = get_column_values(request_type_df, "req_type_id")
    req_priority_ids = get_column_values(request_priority_df, "req_priority_id")
    req_status_ids = get_column_values(request_status_df, "req_status_id")

    data = []

    for i in range(1, rows + 1):
        row = {}

        for col in columns:
            col_name = col["name"]
            col_type = col["type"]

            if col_name == "req_id":
                row[col_name] = f"REQ{i:06d}"
            elif col_name == "req_user_id":
                row[col_name] = random.choice(user_ids) if user_ids else f"USR{i:05d}"
            elif col_name == "req_for_id":
                row[col_name] = random.choice(req_for_ids) if req_for_ids else random.randint(1, 10)
            elif col_name == "req_islead_id":
                row[col_name] = random.choice(req_islead_ids) if req_islead_ids else random.randint(1, 10)
            elif col_name == "req_cat_id":
                row[col_name] = random.choice(cat_ids) if cat_ids else fake.word()
            elif col_name == "req_type_id":
                row[col_name] = random.choice(req_type_ids) if req_type_ids else random.randint(1, 10)
            elif col_name == "req_priority_id":
                row[col_name] = random.choice(req_priority_ids) if req_priority_ids else random.randint(1, 10)
            elif col_name == "req_status_id":
                row[col_name] = random.choice(req_status_ids) if req_status_ids else random.randint(1, 10)
            else:
                row[col_name] = generate_value_from_type(col_name, col_type, i)

        data.append(row)

    return pd.DataFrame(data)

# -------------------------
# MAIN
# -------------------------
# -------------------------
# MAIN
# -------------------------
def main():
    print("🚀 ENGINE STARTED")

    schema = load_schema()
    tables = schema["tables"]
    output_dir = setup_output_folder()

    print("DEBUG: schema loaded successfully")
    print("DEBUG: total tables =", len(tables))

    generated_tables = {}

    # 1. Generate lookup/reference tables first
    lookup_first = [
        "country",
        "state",
        "user_status",
        "user_category",
        "request_for",
        "request_isleadvol",
        "request_priority",
        "request_status",
        "request_type",
        "help_categories"
    ]

    for table_name in lookup_first:
        if table_name in tables:
            df = generate_table(table_name, tables)
            generated_tables[table_name] = df
            print(f"✅ {table_name} created")

    # 2. Generate users with valid foreign keys
    users_df = generate_users_table(
        tables,
        generated_tables["country"],
        generated_tables["state"],
        generated_tables["user_status"],
        generated_tables["user_category"]
    )
    generated_tables["users"] = users_df
    print("✅ users created")

    # 3. Generate request with valid foreign keys
    request_df = generate_request_table(
        tables,
        generated_tables["users"],
        generated_tables["request_for"],
        generated_tables["request_isleadvol"],
        generated_tables["help_categories"],
        generated_tables["request_type"],
        generated_tables["request_priority"],
        generated_tables["request_status"]
    )
    generated_tables["request"] = request_df
    print("✅ request created")

    # 4. Generate remaining tables
    already_done = set(generated_tables.keys())

    for table_name in tables:
        if table_name not in already_done:
            df = generate_table(table_name, tables)
            generated_tables[table_name] = df
            print(f"✅ {table_name} created")

    # 5. Save all tables
    for table_name, df in generated_tables.items():
        output_file = os.path.join(output_dir, f"{table_name}.csv")
        df.to_csv(output_file, index=False)

    print("🎉 ALL TABLES GENERATED")


if __name__ == "__main__":
    main()