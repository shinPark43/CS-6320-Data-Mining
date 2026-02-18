# Mining Report: Market Basket Analysis

## Overview

This report presents the results of Market Basket Analysis (Association Rule Mining) performed on the cleaned Retail Store Sales data warehouse. The analysis identifies products and product categories that are frequently purchased together, and examines how these associations vary across months.

**Dataset Summary:**
- Total sales records: 11,362 (after cleaning)
- Total transaction baskets: 10,257 (grouped by CustomerID + Date + Location)
- Baskets with 2+ unique products: 1,032 (~10% of all baskets)
- Date range: January 2022 -- January 2025 (37 months)
- Products: 200 unique items across 8 categories

> **Note on Date Range:** The assignment specifies data from January 2022 through December 2025 (48 months). However, the Kaggle dataset version used for this analysis (`Retail Store Sales -- 2022-2025` by Ahsan Raza) only contains transaction records through January 2025, covering 37 months rather than the full 48. This limitation is inherent to the dataset and does not affect the validity of the analysis methodology. All 37 available months are analyzed individually in the monthly association section below.

**Methodology:**
- The Apriori algorithm was used to find frequent itemsets and generate association rules
- Analysis was performed at both the **product level** and **category level**
- Metrics: Support, Confidence, and Lift
- Monthly analysis was conducted separately for each of the 37 available months

---

## Why Support Values Are Low

The support values throughout this analysis are notably low (0.0002--0.0045). This is not a flaw in the methodology but a direct consequence of the dataset's characteristics:

**1. 90% of baskets contain only a single item.**
Only 1,032 out of 10,257 baskets have 2 or more unique products. Since associations can only be discovered from multi-item baskets, the theoretical maximum support for any pair is capped at roughly 1,032 / 10,257 ≈ 10%. No pair can ever exceed this ceiling regardless of how dominant it is.

**2. High product diversity spreads co-occurrences thin.**
Among the 1,032 multi-item baskets, items are distributed across 200 unique products, yielding C(200, 2) = 19,900 possible product pairs. The total number of pair occurrences in the data is only ~1,168 (967 two-item baskets × 1 pair + 63 three-item baskets × 3 pairs + 2 four-item baskets × 6 pairs). On average, any specific product pair appears roughly 1,168 / 19,900 ≈ 0.06 times -- most pairs never co-occur at all.

**3. The dataset was not originally designed for co-purchase analysis.**
Each row in the original Kaggle dataset uses TransactionID as a row-level identifier rather than a true transaction grouping. Baskets were reconstructed by grouping on (CustomerID, Date, Location) per the assignment instructions, but the underlying data was not generated with multi-item shopping baskets in mind. For comparison, a typical supermarket dataset has an average basket size of 10--30 items and 95%+ multi-item baskets, producing support values in the 1--5% range.

**Implication for thresholds:** To accommodate this sparsity, very low minimum support thresholds were used (0.0001 for product-level, 0.001 for category-level). Despite the low absolute support values, the discovered rules exhibit high **lift** values (up to 19.35), confirming that the co-occurrences -- while rare -- are far more frequent than random chance would predict.

---

## Top 5 Product Associations

The following product-level associations were identified using the Apriori algorithm with a minimum support of 0.0001. The low support threshold reflects the sparse nature of the data (most baskets contain only one item).

| Rank | Antecedent     | Consequent     | Support | Confidence | Lift   |
|------|----------------|----------------|---------|------------|--------|
| 1    | Item_9_Milk    | Item_11_Milk   | 0.0002  | 0.2000     | 19.353 |
| 2    | Item_10_Bev    | Item_11_Food   | 0.0002  | 0.0870     | 11.892 |
| 3    | Item_22_But    | Item_19_Pat    | 0.0003  | 0.0300     | 11.835 |
| 4    | Item_1_Fur     | Item_18_Milk   | 0.0002  | 0.0339     | 7.559  |
| 5    | Item_21_Bev    | Item_7_Bev     | 0.0002  | 0.0465     | 6.626  |

**Interpretation:**
1. **Item_9_Milk + Item_11_Milk** (Lift=19.35): The strongest association -- customers who buy one milk product are ~19 times more likely to also buy another milk product in the same transaction. This reflects cross-purchasing within the dairy category.
2. **Item_10_Bev + Item_11_Food** (Lift=11.89): A beverage-food pairing, suggesting customers who buy a specific beverage often pair it with a specific food item.
3. **Item_22_But + Item_19_Pat** (Lift=11.84): Cross-category association between Butchers and Patisserie items.
4. **Item_1_Fur + Item_18_Milk** (Lift=7.56): An unexpected cross-category pairing between a furniture item and a milk product.
5. **Item_21_Bev + Item_7_Bev** (Lift=6.63): Intra-category association -- customers purchasing multiple beverage items together.

---

## Top 5 Category Associations

At the category level, the following associations were found:

| Rank | Antecedent                               | Consequent                               | Support | Confidence | Lift  |
|------|------------------------------------------|------------------------------------------|---------|------------|-------|
| 1    | Food                                     | Electric Household Essentials            | 0.0045  | 0.0327     | 0.236 |
| 2    | Beverages                                | Butchers                                 | 0.0042  | 0.0306     | 0.224 |
| 3    | Milk Products                            | Beverages                                | 0.0042  | 0.0306     | 0.223 |
| 4    | Butchers                                 | Furniture                                | 0.0041  | 0.0300     | 0.213 |
| 5    | Furniture                                | Computers And Electric Accessories       | 0.0040  | 0.0284     | 0.211 |

> **Important: These are anti-correlations, not positive co-purchasing patterns.**
>
> All category-level lift values are well below 1.0 (ranging from 0.211 to 0.236). A lift value less than 1.0 means these category pairs co-occur **less frequently** than would be expected by random chance alone. In other words, purchasing from one category actually makes a customer **less likely** to purchase from the paired category in the same basket -- the opposite of a positive co-purchasing relationship.
>
> **Why this happens:** Approximately 90% of all transaction baskets in this dataset contain items from only a single category. This overwhelming dominance of single-category baskets means that any cross-category co-occurrence is inherently rare, driving all lift values below 1.0. No positive (lift > 1.0) category associations exist in this data.
>
> **How to interpret:** While these pairs should not be promoted as "frequently bought together" recommendations, the **relative ranking** among the anti-correlations is still informative. The pair with lift closest to 1.0 (Food + EHE at 0.236) exhibits the least negative association -- meaning it is the category combination that comes closest to random co-occurrence. These relative differences can guide inventory placement and cross-category promotional strategies.

---

## Monthly Analysis: Do Associations Persist Across Months?

The association analysis was repeated for each month individually to determine whether the same patterns appear consistently or are seasonal. Both **category-level** and **product-level** monthly analyses were conducted.

### Category-Level Monthly Consistency

#### Most Consistent Associations (appear in most months)

| Category Pair                              | Months Present | % of Months | Avg Support | Avg Lift |
|--------------------------------------------|---------------|-------------|-------------|----------|
| Beverages + Butchers                       | 13/37         | 35%         | 0.0083      | 0.419    |
| Electric Household Essentials + Food       | 13/37         | 35%         | 0.0103      | 0.516    |
| Butchers + Furniture                       | 13/37         | 35%         | 0.0090      | 0.468    |
| Beverages + Milk Products                  | 12/37         | 32%         | 0.0085      | 0.450    |
| Butchers + Electric Household Essentials   | 12/37         | 32%         | 0.0079      | 0.418    |

#### Least Consistent (Seasonal/Sporadic) Associations

| Category Pair                                       | Months Present | % of Months | Avg Support | Avg Lift |
|-----------------------------------------------------|---------------|-------------|-------------|----------|
| Computers And Electric Accessories + Milk Products   | 6/37          | 16%         | 0.0097      | 0.492    |
| Food + Patisserie                                    | 4/37          | 11%         | 0.0093      | 0.470    |

### Product-Level Monthly Analysis

The assignment specifically asks: *"Do you see the same association between products in different months?"*

Product-level monthly analysis was also performed, tracking the top 5 overall product pairs across each month individually. Due to the extreme sparsity of the data -- only ~10% of baskets contain 2+ products, spread across 200 unique items and 37 months -- product-level monthly rules are significantly harder to detect than category-level ones.

**Key observation:** The top 5 product pairs from the aggregated analysis each appear in only 2--3 out of 37 months (5--8%):

| Product Pair | Months Present | Months |
|---|---|---|
| Item\_11\_Milk + Item\_9\_Milk | 2/37 (5%) | 2024-03, 2024-12 |
| Item\_10\_Bev + Item\_11\_Food | 2/37 (5%) | 2022-02, 2022-08 |
| Item\_19\_Pat + Item\_22\_But | 3/37 (8%) | 2023-02, 2023-03, 2023-12 |
| Item\_18\_Milk + Item\_1\_Fur | 2/37 (5%) | 2023-06, 2023-10 |
| Item\_21\_Bev + Item\_7\_Bev | 2/37 (5%) | 2022-10, 2023-04 |

Even though *some* product-level rules are detected in all 37 months, any *specific* product pair is far too rare to track consistently. Each of these pairs co-occurs in only 2--3 baskets across the entire dataset; when split into monthly slices, most months have zero co-occurrences for any given pair.

This confirms that **category-level analysis is significantly more reliable for detecting monthly trends** in this dataset. With only 8 categories (vs. 200 products), category-level co-occurrences are much more frequent, enabling meaningful month-by-month comparison.

### Key Findings

1. **No universally persistent association**: Even the most consistent category pair (Beverages + Butchers) only appears in 35% of months. This reflects the inherent sparsity of multi-item baskets.

2. **Relative stability of top pairs**: The top 3 category pairs (Beverages+Butchers, EHE+Food, Butchers+Furniture) are the most stable across time, suggesting these co-purchasing patterns are not seasonal but rather structural to the customer base.

3. **Product-level associations are too sparse for monthly tracking**: The top product pairs from the overall analysis typically co-occur in only 2--3 baskets total. When divided across 37 months, most product pairs cannot meet even the lowest support threshold in any individual month. This is a fundamental limitation of the dataset's sparsity, not the methodology.

4. **Seasonal/sporadic pairs**: Food + Patisserie (4 months) and Computers + Milk Products (6 months) are the most sporadic category pairs, appearing in fewer than 20% of months. These may reflect seasonal shopping behaviors or promotional events.

5. **Monthly lift variation**: The heatmap visualization shows that when category associations do appear in a given month, their lift values tend to be relatively consistent (0.3--0.5 range), suggesting the strength of association does not fluctuate wildly even when it does occur.

---

## Visualizations

The following visualizations are included in `report/visualizations/`:

1. **top10_category_associations.png** -- Bar chart of top 10 category pairs by lift
2. **top10_product_associations.png** -- Bar chart of top 10 product pairs by lift
3. **support_vs_confidence.png** -- Scatter plot showing the relationship between support, confidence, and lift for category-level rules
4. **monthly_lift_heatmap.png** -- Heatmap showing which category associations appear in which months, colored by lift value

Supporting data files are in `report/data/`:
- `top5_associations.csv` -- Top 5 product association rules
- `category_associations.csv` -- All category-level association rules
- `monthly_consistency.csv` -- Monthly presence counts for each category pair
