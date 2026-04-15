"""Generate Phase 2 page visuals (cards, slicers, charts) for the 6 new pages."""
import os
import json
import uuid

BASE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(BASE, "Report.Report", "definition", "pages")

VISUAL_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"


def write_visual(page, name, payload):
    p = os.path.join(PAGES, page, "visuals", name)
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def year_slicer(page, slicer_name):
    return {
        "$schema": VISUAL_SCHEMA,
        "name": slicer_name,
        "position": {"x": 20, "y": 14, "z": 9, "height": 56, "width": 200, "tabOrder": 9},
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [{
                            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Date"}}, "Property": "Year"}},
                            "queryRef": "Dim_Date.Year",
                            "nativeQueryRef": "Year",
                            "active": True
                        }]
                    }
                }
            },
            "objects": {"data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}}}]},
            "drillFilterOtherVisuals": True
        },
        "filterConfig": {
            "filters": [{
                "name": uuid.uuid4().hex[:20],
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Date"}}, "Property": "Year"}},
                "type": "Categorical",
                "filter": {
                    "Version": 2,
                    "From": [{"Name": "d", "Entity": "Dim_Date", "Type": 0}],
                    "Where": [{
                        "Condition": {
                            "In": {
                                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Year"}}],
                                "Values": [[{"Literal": {"Value": "2026L"}}]]
                            }
                        }
                    }]
                }
            }]
        }
    }


def card(name, x, y, w, h, measure_name, tab_order):
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": x, "y": y, "z": tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [{
                            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": measure_name}},
                            "queryRef": f"_Measures.{measure_name}",
                            "nativeQueryRef": measure_name
                        }]
                    }
                }
            },
            "drillFilterOtherVisuals": True
        }
    }


def column_chart(name, x, y, w, h, measure, category_table, category_col, tab_order):
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": x, "y": y, "z": tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "columnChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [{
                        "field": {"Column": {"Expression": {"SourceRef": {"Entity": category_table}}, "Property": category_col}},
                        "queryRef": f"{category_table}.{category_col}",
                        "nativeQueryRef": category_col,
                        "active": True
                    }]},
                    "Y": {"projections": [{
                        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": measure}},
                        "queryRef": f"_Measures.{measure}",
                        "nativeQueryRef": measure
                    }]}
                }
            },
            "drillFilterOtherVisuals": True
        }
    }


def line_chart(name, x, y, w, h, measure, category_table, category_col, tab_order):
    payload = column_chart(name, x, y, w, h, measure, category_table, category_col, tab_order)
    payload["visual"]["visualType"] = "lineChart"
    return payload


def bar_chart(name, x, y, w, h, measure, category_table, category_col, tab_order):
    payload = column_chart(name, x, y, w, h, measure, category_table, category_col, tab_order)
    payload["visual"]["visualType"] = "barChart"
    return payload


def donut_chart(name, x, y, w, h, measure, category_table, category_col, tab_order):
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": x, "y": y, "z": tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "donutChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [{
                        "field": {"Column": {"Expression": {"SourceRef": {"Entity": category_table}}, "Property": category_col}},
                        "queryRef": f"{category_table}.{category_col}",
                        "nativeQueryRef": category_col,
                        "active": True
                    }]},
                    "Y": {"projections": [{
                        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": measure}},
                        "queryRef": f"_Measures.{measure}",
                        "nativeQueryRef": measure
                    }]}
                }
            },
            "drillFilterOtherVisuals": True
        }
    }


def matrix(name, x, y, w, h, row_table, row_col, measures, tab_order):
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": x, "y": y, "z": tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "pivotTable",
            "query": {
                "queryState": {
                    "Rows": {"projections": [{
                        "field": {"Column": {"Expression": {"SourceRef": {"Entity": row_table}}, "Property": row_col}},
                        "queryRef": f"{row_table}.{row_col}",
                        "nativeQueryRef": row_col,
                        "active": True
                    }]},
                    "Values": {"projections": [
                        {
                            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": m}},
                            "queryRef": f"_Measures.{m}",
                            "nativeQueryRef": m
                        } for m in measures
                    ]}
                }
            },
            "drillFilterOtherVisuals": True
        }
    }


# ============================================================
# Page 3: Sales, Marketing & Channels
# ============================================================
def gen_sales_channels():
    write_visual("sales_channels", "year_slicer_sc", year_slicer("sales_channels", "year_slicer_sc"))
    # KPI cards row at y=80
    write_visual("sales_channels", "card_total_rev", card("card_total_rev", 20, 80, 200, 100, "Reservation Net Revenue", 1))
    write_visual("sales_channels", "card_direct", card("card_direct", 230, 80, 200, 100, "Direct Booking %", 2))
    write_visual("sales_channels", "card_ota", card("card_ota", 440, 80, 200, 100, "OTA Mix %", 3))
    write_visual("sales_channels", "card_lead", card("card_lead", 650, 80, 200, 100, "Avg Lead Time", 4))
    write_visual("sales_channels", "card_los", card("card_los", 860, 80, 200, 100, "Avg Length of Stay", 5))
    write_visual("sales_channels", "card_cancel", card("card_cancel", 1070, 80, 190, 100, "Cancellation Rate", 6))
    # Charts
    write_visual("sales_channels", "rev_by_channel_p3", bar_chart("rev_by_channel_p3", 20, 195, 620, 250, "Reservation Net Revenue", "Dim_Channel", "ChannelName", 7))
    write_visual("sales_channels", "rev_by_segment_p3", donut_chart("rev_by_segment_p3", 650, 195, 610, 250, "Reservation Gross Revenue", "Dim_Segment", "SegmentName", 8))
    write_visual("sales_channels", "channel_matrix", matrix("channel_matrix", 20, 460, 1240, 240, "Dim_Channel", "ChannelName", ["Total Reservations","Reservation Net Revenue","Direct Booking %","Avg Lead Time"], 9))


# ============================================================
# Page 4: Operations & Guest Experience
# ============================================================
def gen_operations():
    write_visual("operations", "year_slicer_op", year_slicer("operations", "year_slicer_op"))
    write_visual("operations", "card_score", card("card_score", 20, 80, 200, 100, "Avg Review Score", 1))
    write_visual("operations", "card_nps", card("card_nps", 230, 80, 200, 100, "NPS Score", 2))
    write_visual("operations", "card_clean", card("card_clean", 440, 80, 200, 100, "Avg Cleanliness", 3))
    write_visual("operations", "card_service", card("card_service", 650, 80, 200, 100, "Avg Service Score", 4))
    write_visual("operations", "card_complaints", card("card_complaints", 860, 80, 200, 100, "Complaint Count", 5))
    write_visual("operations", "card_response", card("card_response", 1070, 80, 190, 100, "Response Rate", 6))
    write_visual("operations", "score_by_month", line_chart("score_by_month", 20, 195, 620, 250, "Avg Review Score", "Dim_Date", "MonthName", 7))
    write_visual("operations", "score_by_platform", bar_chart("score_by_platform", 650, 195, 610, 250, "Avg Review Score", "Fact_GuestFeedback", "Platform", 8))
    write_visual("operations", "complaints_pareto", column_chart("complaints_pareto", 20, 460, 620, 240, "Complaint Count", "Fact_GuestFeedback", "ComplaintCategory", 9))
    write_visual("operations", "feedback_matrix", matrix("feedback_matrix", 650, 460, 610, 240, "Fact_GuestFeedback", "Platform", ["Avg Review Score","NPS Score","Complaint Count","Response Rate"], 10))


# ============================================================
# Page 7: Procurement & Inventory
# ============================================================
def gen_procurement():
    write_visual("procurement", "year_slicer_proc", year_slicer("procurement", "year_slicer_proc"))
    write_visual("procurement", "card_spend", card("card_spend", 20, 80, 240, 100, "Total Spend", 1))
    write_visual("procurement", "card_variance", card("card_variance", 270, 80, 240, 100, "Price Variance", 2))
    write_visual("procurement", "card_otif", card("card_otif", 520, 80, 240, 100, "OTIF %", 3))
    write_visual("procurement", "card_emergency", card("card_emergency", 770, 80, 240, 100, "Emergency Purchase %", 4))
    write_visual("procurement", "card_maverick", card("card_maverick", 1020, 80, 240, 100, "Maverick Spend %", 5))
    write_visual("procurement", "spend_by_cat", donut_chart("spend_by_cat", 20, 195, 620, 250, "Total Spend", "Dim_ProcurementCategory", "CategoryName", 6))
    write_visual("procurement", "spend_by_supplier", bar_chart("spend_by_supplier", 650, 195, 610, 250, "Total Spend", "Dim_Supplier", "SupplierName", 7))
    write_visual("procurement", "spend_trend", line_chart("spend_trend", 20, 460, 620, 240, "Total Spend", "Dim_Date", "MonthName", 8))
    write_visual("procurement", "supplier_matrix", matrix("supplier_matrix", 650, 460, 610, 240, "Dim_Supplier", "SupplierName", ["Total Spend","Price Variance","OTIF %"], 9))


# ============================================================
# Page 8: Workforce & HR
# ============================================================
def gen_workforce():
    write_visual("workforce", "year_slicer_hr", year_slicer("workforce", "year_slicer_hr"))
    write_visual("workforce", "card_headcount", card("card_headcount", 20, 80, 200, 100, "Headcount", 1))
    write_visual("workforce", "card_labor", card("card_labor", 230, 80, 200, 100, "Total Labor Cost", 2))
    write_visual("workforce", "card_labor_pct", card("card_labor_pct", 440, 80, 200, 100, "Labor Cost % Revenue", 3))
    write_visual("workforce", "card_overtime", card("card_overtime", 650, 80, 200, 100, "Overtime %", 4))
    write_visual("workforce", "card_turnover", card("card_turnover", 860, 80, 200, 100, "Turnover Rate", 5))
    write_visual("workforce", "card_revemp", card("card_revemp", 1070, 80, 190, 100, "Revenue per Employee", 6))
    write_visual("workforce", "labor_trend", line_chart("labor_trend", 20, 195, 620, 250, "Total Labor Cost", "Dim_Date", "MonthName", 7))
    write_visual("workforce", "headcount_dept", bar_chart("headcount_dept", 650, 195, 610, 250, "Headcount", "Dim_Department", "DepartmentName", 8))
    write_visual("workforce", "ot_by_dept", column_chart("ot_by_dept", 20, 460, 620, 240, "Overtime Hours", "Dim_Department", "DepartmentName", 9))
    write_visual("workforce", "labor_matrix", matrix("labor_matrix", 650, 460, 610, 240, "Dim_Department", "DepartmentName", ["Headcount","Total Labor Cost","Overtime %","Turnover"], 10))


# ============================================================
# Page 9: Energy & Sustainability
# ============================================================
def gen_sustainability():
    write_visual("sustainability", "year_slicer_su", year_slicer("sustainability", "year_slicer_su"))
    write_visual("sustainability", "card_energy_cost", card("card_energy_cost", 20, 80, 200, 100, "Total Energy Cost", 1))
    write_visual("sustainability", "card_kwh", card("card_kwh", 230, 80, 200, 100, "Total Energy kWh", 2))
    write_visual("sustainability", "card_kwh_per", card("card_kwh_per", 440, 80, 200, 100, "kWh per Occupied Room", 3))
    write_visual("sustainability", "card_water", card("card_water", 650, 80, 200, 100, "Water per Occupied Room", 4))
    write_visual("sustainability", "card_carbon", card("card_carbon", 860, 80, 200, 100, "Total Carbon kgCO2e", 5))
    write_visual("sustainability", "card_anomaly", card("card_anomaly", 1070, 80, 190, 100, "Anomaly Count", 6))
    write_visual("sustainability", "energy_trend", line_chart("energy_trend", 20, 195, 620, 250, "Total Energy kWh", "Dim_Date", "MonthName", 7))
    write_visual("sustainability", "carbon_trend", line_chart("carbon_trend", 650, 195, 610, 250, "Total Carbon kgCO2e", "Dim_Date", "MonthName", 8))
    write_visual("sustainability", "cost_breakdown", column_chart("cost_breakdown", 20, 460, 620, 240, "Total Energy Cost", "Dim_Date", "MonthName", 9))
    write_visual("sustainability", "kwh_per_room_trend", line_chart("kwh_per_room_trend", 650, 460, 610, 240, "kWh per Occupied Room", "Dim_Date", "MonthName", 10))


# ============================================================
# Page 10: Portfolio & Forecast
# ============================================================
def gen_portfolio():
    write_visual("portfolio", "year_slicer_pf", year_slicer("portfolio", "year_slicer_pf"))
    write_visual("portfolio", "card_revpar", card("card_revpar", 20, 80, 200, 100, "RevPAR", 1))
    write_visual("portfolio", "card_goppar", card("card_goppar", 230, 80, 200, 100, "GOPPAR", 2))
    write_visual("portfolio", "card_occ", card("card_occ", 440, 80, 200, 100, "Occupancy %", 3))
    write_visual("portfolio", "card_gop", card("card_gop", 650, 80, 200, 100, "GOP", 4))
    write_visual("portfolio", "card_ebitda_p", card("card_ebitda_p", 860, 80, 200, 100, "EBITDA", 5))
    write_visual("portfolio", "card_npm", card("card_npm", 1070, 80, 190, 100, "Net Profit Margin %", 6))
    write_visual("portfolio", "rev_trend", line_chart("rev_trend", 20, 195, 620, 250, "Total Revenue", "Dim_Date", "MonthName", 7))
    write_visual("portfolio", "ebitda_trend", line_chart("ebitda_trend", 650, 195, 610, 250, "EBITDA Margin %", "Dim_Date", "MonthName", 8))
    write_visual("portfolio", "property_matrix", matrix("property_matrix", 20, 460, 1240, 240, "Dim_Property", "PropertyName", ["Total Revenue","RevPAR","GOPPAR","Occupancy %","Net Profit Margin %"], 9))


if __name__ == "__main__":
    gen_sales_channels()
    gen_operations()
    gen_procurement()
    gen_workforce()
    gen_sustainability()
    gen_portfolio()
    print("Done generating Phase 2 visuals")
