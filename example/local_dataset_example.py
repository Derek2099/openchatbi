"""Example script demonstrating local dataset loading with pandas.

This example shows how to:
1. Configure local datasets in config.yaml
2. Load datasets using the LocalDatasetManager
3. Perform basic data analysis with pandas
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

from openchatbi.local_dataset_loader import LocalDataset, LocalDatasetManager


def example_basic_usage():
    """Example of basic local dataset loading."""
    print("=" * 60)
    print("Example 1: Basic Dataset Loading")
    print("=" * 60)

    # Create a sample CSV file for demonstration
    sample_data = pd.DataFrame(
        {
            "product": ["Widget A", "Widget B", "Widget C", "Widget A", "Widget B"],
            "sales": [10000, 15000, 8000, 12000, 18000],
            "region": ["North", "South", "East", "North", "South"],
            "month": ["Jan", "Jan", "Jan", "Feb", "Feb"],
        }
    )

    # Save sample data
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    sample_file = data_dir / "sample_sales.csv"
    sample_data.to_csv(sample_file, index=False)
    print(f"Created sample file: {sample_file}")

    # Create a local dataset configuration
    dataset = LocalDataset(
        name="sample_sales",
        path=str(sample_file),
        description="Sample sales data for demonstration",
        file_type="csv",
    )

    # Load the dataset
    df = dataset.load()
    print(f"\nLoaded dataset: {dataset.name}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")

    # Basic analysis
    print(f"\nTotal sales: ${df['sales'].sum():,}")
    print(f"Average sales: ${df['sales'].mean():,.2f}")
    print(f"\nSales by region:\n{df.groupby('region')['sales'].sum()}")


def example_manager_usage():
    """Example of using LocalDatasetManager with multiple datasets."""
    print("\n" + "=" * 60)
    print("Example 2: Managing Multiple Datasets")
    print("=" * 60)

    # Create sample datasets
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)

    # Sales data
    sales_data = pd.DataFrame(
        {
            "product_id": [1, 2, 3, 1, 2],
            "sales": [10000, 15000, 8000, 12000, 18000],
            "date": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-02-01", "2024-02-01"],
        }
    )
    sales_file = data_dir / "sales.csv"
    sales_data.to_csv(sales_file, index=False)

    # Customer data
    customer_data = pd.DataFrame(
        {"customer_id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "region": ["North", "South", "East"]}
    )
    customer_file = data_dir / "customers.csv"
    customer_data.to_csv(customer_file, index=False)

    # Configure datasets
    datasets_config = [
        {"name": "sales", "path": str(sales_file), "description": "Sales transactions", "file_type": "csv"},
        {"name": "customers", "path": str(customer_file), "description": "Customer information", "file_type": "csv"},
    ]

    # Create manager
    manager = LocalDatasetManager(datasets_config)

    # List available datasets
    print("\nAvailable datasets:")
    for dataset_info in manager.list_datasets():
        print(f"  - {dataset_info['name']}: {dataset_info['description']}")

    # Load and display datasets
    print("\n--- Sales Dataset ---")
    sales_df = manager.get_dataset("sales")
    print(sales_df)

    print("\n--- Customers Dataset ---")
    customers_df = manager.get_dataset("customers")
    print(customers_df)

    # Example analysis combining datasets
    print("\n--- Combined Analysis ---")
    total_sales = sales_df["sales"].sum()
    total_customers = len(customers_df)
    print(f"Total sales: ${total_sales:,}")
    print(f"Total customers: {total_customers}")
    print(f"Average sales per customer: ${total_sales / total_customers:,.2f}")


def example_excel_usage():
    """Example of loading Excel files."""
    print("\n" + "=" * 60)
    print("Example 3: Loading Excel Files")
    print("=" * 60)

    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)

    # Create sample Excel file
    excel_file = data_dir / "products.xlsx"
    product_data = pd.DataFrame(
        {
            "product_id": [1, 2, 3, 4],
            "product_name": ["Widget A", "Widget B", "Widget C", "Widget D"],
            "price": [29.99, 39.99, 24.99, 34.99],
            "category": ["Electronics", "Electronics", "Home", "Home"],
        }
    )
    product_data.to_excel(excel_file, index=False, sheet_name="Products")
    print(f"Created Excel file: {excel_file}")

    # Load Excel dataset
    dataset = LocalDataset(
        name="products",
        path=str(excel_file),
        description="Product catalog",
        file_type="excel",
        options={"sheet_name": "Products"},
    )

    df = dataset.load()
    print(f"\nLoaded dataset: {dataset.name}")
    print(f"\nProduct catalog:\n{df}")
    print(f"\nAverage price by category:\n{df.groupby('category')['price'].mean()}")


def example_dataset_info():
    """Example of getting dataset information without loading."""
    print("\n" + "=" * 60)
    print("Example 4: Dataset Information")
    print("=" * 60)

    data_dir = Path("./data")
    sample_file = data_dir / "sample_sales.csv"

    if sample_file.exists():
        dataset = LocalDataset(
            name="sales_info", path=str(sample_file), description="Sales data", file_type="csv"
        )

        manager = LocalDatasetManager()
        manager.add_dataset(dataset)

        info = manager.get_dataset_info("sales_info")
        print("\nDataset Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")


def cleanup():
    """Clean up temporary files created by examples."""
    print("\n" + "=" * 60)
    print("Cleanup")
    print("=" * 60)

    import shutil

    data_dir = Path("./data")
    if data_dir.exists():
        shutil.rmtree(data_dir)
        print(f"Removed directory: {data_dir}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Local Dataset Loading Examples")
    print("=" * 60)

    try:
        # Run examples
        example_basic_usage()
        example_manager_usage()
        example_excel_usage()
        example_dataset_info()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    finally:
        # Clean up temporary files
        cleanup()

    print("\nNote: To use local datasets in your OpenChatBI configuration,")
    print("add the following to your config.yaml:")
    print("""
local_datasets:
  enabled: true
  datasets:
    - name: "my_data"
      path: "./data/my_file.csv"
      description: "My dataset"
      file_type: "csv"
""")
