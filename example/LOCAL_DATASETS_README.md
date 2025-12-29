# Local Dataset Loading with Pandas

This feature allows you to load local data files (CSV, Excel, Parquet, JSON) using pandas directly in OpenChatBI.

## Configuration

Add the following section to your `config.yaml`:

```yaml
local_datasets:
  enabled: true
  datasets:
    - name: "sales_data"
      path: "./data/sales.csv"
      description: "Sales transaction data"
      file_type: "csv"
      options:
        encoding: "utf-8"
        sep: ","
    
    - name: "customer_data"
      path: "./data/customers.xlsx"
      description: "Customer information"
      file_type: "excel"
      options:
        sheet_name: "Sheet1"
```

## Supported File Types

- **CSV**: `file_type: "csv"`
- **Excel**: `file_type: "excel"` or `"xlsx"` or `"xls"`
- **Parquet**: `file_type: "parquet"`
- **JSON**: `file_type: "json"`

## Usage in Python

```python
from openchatbi import config

# Get the local dataset manager from config
cfg = config.get()
dataset_manager = cfg.local_dataset_manager

# List available datasets
datasets = dataset_manager.list_datasets()
for ds in datasets:
    print(f"{ds['name']}: {ds['description']}")

# Load a specific dataset
df = dataset_manager.get_dataset("sales_data")
print(df.head())

# Get dataset info without loading
info = dataset_manager.get_dataset_info("sales_data")
print(info)
```

## Pandas Read Options

You can pass any pandas read options in the `options` field:

### CSV Options
```yaml
options:
  encoding: "utf-8"
  sep: ","
  header: 0
  index_col: 0
  usecols: ["col1", "col2"]
  dtype: {"col1": "str", "col2": "int"}
```

### Excel Options
```yaml
options:
  sheet_name: "Sheet1"
  header: 0
  usecols: "A:D"
```

### Parquet Options
```yaml
options:
  engine: "pyarrow"
  columns: ["col1", "col2"]
```

### JSON Options
```yaml
options:
  orient: "records"
  lines: true
```

## Example

See `example/local_dataset_example.py` for a complete working example demonstrating:
- Basic dataset loading
- Managing multiple datasets
- Loading different file formats
- Basic data analysis

Run the example:
```bash
python example/local_dataset_example.py
```

## Requirements

- pandas >= 2.3.3
- openpyxl (for Excel files)
- pyarrow (for Parquet files, optional)

These are already included in the OpenChatBI dependencies.
