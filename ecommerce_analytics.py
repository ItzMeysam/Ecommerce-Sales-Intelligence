import pandas as pd
import matplotlib.pyplot as plt


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers_df = pd.read_csv("customers.csv")
    orders_df = pd.read_csv("orders.csv")
    order_items_df = pd.read_csv("order_items.csv")
    return customers_df, orders_df, order_items_df


def merge_data(customers: pd.DataFrame, orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    merged_df = pd.merge(customers, orders, on="customer_id", how="inner")
    merged_df = pd.merge(merged_df, items, on="order_id", how="inner")
    return merged_df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df['total_price'] = df['quantity'] * df['price']
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df


def analyze_sales(df: pd.DataFrame) -> dict:
    revenue_by_status = df.groupby("status")['total_price'].sum()
    customer_analyze = df.groupby("is_premium")['total_price'].agg(['sum', 'mean'])
    category_analysis = (
        df.groupby("category")
        .agg(total_revenue=("total_price", "sum"),
             total_quantity=("quantity", "sum"))
        .sort_values("total_revenue", ascending=False)
    )
    city_analysis = (
        df.groupby("city")["total_price"].sum()
        .sort_values(ascending=False)
    )
    monthly_sales = (
        df.groupby(df['order_date'].dt.to_period("M"))['total_price'].sum()
    )

    analyze_dict = {
        "revenue_by_status": revenue_by_status,
        "customer_analyze": customer_analyze,
        "category_analysis": category_analysis,
        "city_analysis": city_analysis,
        "monthly_sales": monthly_sales
    }
    return analyze_dict


def plot_dashboard(metrics: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    fig.suptitle("E-Commerce Performance Dashboard", fontsize=16, fontweight="bold")

    monthly = metrics['monthly_sales']
    axes[0, 0].plot(monthly.index.astype(str), monthly.values)
    axes[0, 0].set_title("Monthly Trends")
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid()

    cat_data = metrics['category_analysis']
    axes[0, 1].bar(cat_data.index, cat_data['total_revenue'])
    axes[0, 1].set_title("Revenue by Category")

    status_data = metrics['revenue_by_status']
    axes[1, 0].pie(status_data.values, labels=status_data.index, autopct="%1.1f%%", startangle=90)
    axes[1, 0].set_title("Order Status Distribution")

    city_data = metrics['city_analysis']
    axes[1, 1].bar(city_data.index, city_data.values, color='coral')
    axes[1, 1].set_title("Sales by City")

    fig.savefig("dashboard.png", dpi=150)

    manager = plt.get_current_fig_manager()
    try:
        manager.window.state('zoomed')
    except Exception:
        try:
            manager.full_screen_toggle()
        except Exception:
            pass

    plt.show()


def print_summary(metrics: dict) -> None:
    print("=" * 40)
    print("      EXECUTIVE SUMMARY REPORT      ")
    print("=" * 40)
    top_cat = metrics['category_analysis'].index[0]
    top_city = metrics['city_analysis'].idxmax()
    best_month = metrics['monthly_sales'].idxmax()

    print(f"• Top Performing Category: {top_cat}")
    print(f"• Top Performing City:     {top_city}")
    print(f"• Best Sales Month:        {best_month}")
    print("=" * 40)


if __name__ == "__main__":
    customers_df, orders_df, order_items_df = load_data()
    final_data = merge_data(customers_df, orders_df, order_items_df)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    final_data = prepare_data(final_data)
    analyze_dict = analyze_sales(final_data)
    plot_dashboard(analyze_dict)
    print_summary(analyze_dict)
