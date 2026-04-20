# Mock Data Generation

## Objective
This project generates synthetic/mock CSV data for database tables using the provided schema.

Used for:
- testing
- development
- demos

## Files
- generate_data.py → main script
- db_info.json → schema info
- lookup_tables/ → reference CSV files
- mock_db/ → generated CSV files

## Features
- One CSV per table
- Uses schema automatically
- Preserves foreign key references
- Generates users and request with custom logic

## Run

```bash
python generate_data.py