"""Generate a polished Star Schema ER diagram for the Retail Sales Data Warehouse."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ── colour palette ──────────────────────────────────────────────────
COLORS = {
    "fact_header":  "#C0392B",
    "fact_body":    "#FADBD8",
    "dim_date_h":   "#2471A3",
    "dim_date_b":   "#D4E6F1",
    "dim_prod_h":   "#1E8449",
    "dim_prod_b":   "#D5F5E3",
    "dim_cust_h":   "#7D3C98",
    "dim_cust_b":   "#E8DAEF",
    "line":         "#566573",
    "bg":           "#FDFEFE",
    "text_dark":    "#1C2833",
    "text_light":   "#FFFFFF",
    "pk":           "#E74C3C",
    "fk":           "#2980B9",
}

ROW_H   = 0.38
HDR_H   = 0.50
PAD     = 0.18
COL_GAP = 0.12

def _table_height(n_rows):
    return HDR_H + n_rows * ROW_H + PAD

def draw_table(ax, x, y, width, title, rows, header_color, body_color):
    """
    Draw an entity table at (x, y) = top-left corner.
    rows: list of (badge, col_name, col_type)  where badge is 'PK', 'FK', or ''.
    Returns (center_x, center_y, width, height) for connection routing.
    """
    n = len(rows)
    h = _table_height(n)

    body = FancyBboxPatch(
        (x, y - h), width, h,
        boxstyle="round,pad=0.03", linewidth=1.2,
        edgecolor=header_color, facecolor=body_color, zorder=2,
    )
    ax.add_patch(body)

    header = FancyBboxPatch(
        (x, y - HDR_H), width, HDR_H,
        boxstyle="round,pad=0.03", linewidth=1.2,
        edgecolor=header_color, facecolor=header_color, zorder=3,
    )
    ax.add_patch(header)

    ax.add_patch(plt.Rectangle(
        (x, y - HDR_H - 0.04), width, 0.08,
        color=header_color, zorder=3, linewidth=0,
    ))

    ax.text(
        x + width / 2, y - HDR_H / 2,
        title, fontsize=11, fontweight="bold",
        color=COLORS["text_light"], ha="center", va="center",
        fontfamily="sans-serif", zorder=4,
    )

    col1_x = x + PAD
    col2_x = x + PAD + 0.45
    col3_x = x + width - PAD

    for i, (badge, name, dtype) in enumerate(rows):
        row_y = y - HDR_H - (i + 0.5) * ROW_H

        if badge == "PK":
            ax.text(col1_x, row_y, "PK", fontsize=7, fontweight="bold",
                    color=COLORS["pk"], ha="left", va="center",
                    fontfamily="monospace", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", fc="#FDEDEC", ec=COLORS["pk"], lw=0.6))
        elif badge == "FK":
            ax.text(col1_x, row_y, "FK", fontsize=7, fontweight="bold",
                    color=COLORS["fk"], ha="left", va="center",
                    fontfamily="monospace", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", fc="#EBF5FB", ec=COLORS["fk"], lw=0.6))

        ax.text(col2_x, row_y, name, fontsize=9,
                color=COLORS["text_dark"], ha="left", va="center",
                fontfamily="monospace", zorder=4)
        ax.text(col3_x, row_y, dtype, fontsize=8,
                color="#7F8C8D", ha="right", va="center",
                fontfamily="monospace", zorder=4)

        if i < n - 1:
            line_y = y - HDR_H - (i + 1) * ROW_H
            ax.plot([x + 0.06, x + width - 0.06], [line_y, line_y],
                    color="#D5D8DC", linewidth=0.5, zorder=3)

    return (x, y, width, h)


def draw_connection(ax, fact_box, dim_box, fact_side, dim_side, label):
    """Draw a relationship line between two table boxes with a FK label."""
    fx, fy, fw, fh = fact_box
    dx, dy, dw, dh = dim_box

    sides = {
        "left":   lambda b: (b[0], b[1] - b[3] / 2),
        "right":  lambda b: (b[0] + b[2], b[1] - b[3] / 2),
        "top":    lambda b: (b[0] + b[2] / 2, b[1]),
        "bottom": lambda b: (b[0] + b[2] / 2, b[1] - b[3]),
    }

    x1, y1 = sides[fact_side](fact_box)
    x2, y2 = sides[dim_side](dim_box)

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    if fact_side in ("left", "right") and dim_side in ("left", "right"):
        mx = (x1 + x2) / 2
        path_x = [x1, mx, mx, x2]
        path_y = [y1, y1, y2, y2]
    elif fact_side in ("top", "bottom") and dim_side in ("top", "bottom"):
        my = (y1 + y2) / 2
        path_x = [x1, x1, x2, x2]
        path_y = [y1, my, my, y2]
    else:
        path_x = [x1, x2]
        path_y = [y1, y2]

    ax.plot(path_x, path_y, color=COLORS["line"], linewidth=1.8,
            solid_capstyle="round", zorder=1)

    ax.plot(x2, y2, 'o', color=COLORS["line"], markersize=6, zorder=5)
    ax.plot(x1, y1, 'o', color=COLORS["line"], markersize=4,
            markerfacecolor="white", markeredgecolor=COLORS["line"],
            markeredgewidth=1.5, zorder=5)

    lx = (path_x[len(path_x)//2 - 1] + path_x[len(path_x)//2]) / 2
    ly = (path_y[len(path_y)//2 - 1] + path_y[len(path_y)//2]) / 2

    ax.text(lx, ly, label, fontsize=7.5, color=COLORS["line"],
            ha="center", va="center", fontfamily="monospace",
            fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))


# ── schema definitions ──────────────────────────────────────────────
fact_sales = [
    ("PK", "sale_id",        "INTEGER"),
    ("FK", "date_id",        "INTEGER"),
    ("FK", "product_id",     "INTEGER"),
    ("FK", "customer_id",    "INTEGER"),
    ("",   "quantity",       "INTEGER"),
    ("",   "price",          "REAL"),
    ("",   "total_spent",    "REAL"),
    ("",   "payment_method", "TEXT"),
    ("",   "location",       "TEXT"),
]

dim_date = [
    ("PK", "date_id",      "INTEGER"),
    ("",   "full_date",    "DATE"),
    ("",   "day_of_week",  "INTEGER"),
    ("",   "day_name",     "TEXT"),
    ("",   "is_weekend",   "INTEGER"),
    ("",   "month",        "INTEGER"),
    ("",   "month_name",   "TEXT"),
    ("",   "quarter",      "INTEGER"),
    ("",   "year",         "INTEGER"),
    ("",   "fiscal_year",  "INTEGER"),
]

dim_product = [
    ("PK", "product_id",   "INTEGER"),
    ("",   "product_name", "TEXT"),
    ("",   "category",     "TEXT"),
]

dim_customer = [
    ("PK", "customer_id",         "INTEGER"),
    ("",   "customer_name",       "TEXT"),
    ("",   "total_transactions",  "INTEGER"),
    ("",   "total_spent",         "REAL"),
    ("",   "avg_basket_size",     "REAL"),
    ("",   "preferred_category",  "TEXT"),
    ("",   "preferred_location",  "TEXT"),
]


def main():
    fig, ax = plt.subplots(1, 1, figsize=(18, 10), dpi=180)
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_xlim(-1, 17)
    ax.set_ylim(-8.5, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")

    TW_FACT = 4.6
    TW_DIM_DATE = 4.2
    TW_DIM_PROD = 4.2
    TW_DIM_CUST = 4.2

    # ── position tables in a star layout ───────────────────────────
    # Fact table: center
    fact_x, fact_y = 5.8, 1.5
    fact_box = draw_table(ax, fact_x, fact_y, TW_FACT,
                          "FactSales  (Fact Table)", fact_sales,
                          COLORS["fact_header"], COLORS["fact_body"])

    # DimDate: left of fact
    date_x, date_y = 0.0, 1.2
    date_box = draw_table(ax, date_x, date_y, TW_DIM_DATE,
                          "DimDate", dim_date,
                          COLORS["dim_date_h"], COLORS["dim_date_b"])

    # DimProduct: right of fact, upper
    prod_x, prod_y = 12.0, 1.2
    prod_box = draw_table(ax, prod_x, prod_y, TW_DIM_PROD,
                          "DimProduct", dim_product,
                          COLORS["dim_prod_h"], COLORS["dim_prod_b"])

    # DimCustomer: right of fact, lower
    cust_x, cust_y = 12.0, -1.5
    cust_box = draw_table(ax, cust_x, cust_y, TW_DIM_CUST,
                          "DimCustomer", dim_customer,
                          COLORS["dim_cust_h"], COLORS["dim_cust_b"])

    # ── draw FK connections ────────────────────────────────────────
    draw_connection(ax, fact_box, date_box, "left", "right", "date_id")
    draw_connection(ax, fact_box, prod_box, "right", "left", "product_id")
    draw_connection(ax, fact_box, cust_box, "right", "left", "customer_id")

    # ── title ──────────────────────────────────────────────────────
    ax.text(
        8, -7.6,
        "Star Schema  —  Retail Sales Data Warehouse",
        fontsize=15, fontweight="bold", color=COLORS["text_dark"],
        ha="center", va="center", fontfamily="sans-serif",
    )
    ax.text(
        8, -8.1,
        "FactSales references three dimension tables via foreign keys",
        fontsize=9, color="#7F8C8D", ha="center", va="center",
        fontfamily="sans-serif", style="italic",
    )

    plt.tight_layout(pad=0.5)

    out_path = os.path.join(os.path.dirname(__file__), "star_schema.png")
    fig.savefig(out_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
