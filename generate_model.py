"""Generate TMDL semantic model files for The Grand Azure hotel dashboard."""
import os
import uuid
import random
import math

random.seed(42)  # Deterministic data

BASE = os.path.dirname(os.path.abspath(__file__))
SM_DEF = os.path.join(BASE, "Report.SemanticModel", "definition")
TABLES_DIR = os.path.join(SM_DEF, "tables")
os.makedirs(TABLES_DIR, exist_ok=True)

def guid():
    return str(uuid.uuid4())

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {os.path.relpath(path, BASE)}")

# ============================================================
# 1. Dim_Date
# ============================================================
def gen_dim_date():
    content = f"""table Dim_Date
\tlineageTag: {guid()}

\tcolumn DateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DateID

\tcolumn Date
\t\tdataType: dateTime
\t\tformatString: Short Date
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Date

\tcolumn Year
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Year

\tcolumn Quarter
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Quarter

\tcolumn Month
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Month

\tcolumn MonthName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: MonthName

\tcolumn DayOfWeek
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DayOfWeek

\tcolumn DayName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DayName

\tcolumn IsWeekend
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsWeekend

\tcolumn Season
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Season

\tcolumn FiscalYear
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: FiscalYear

\tcolumn FiscalQuarter
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: FiscalQuarter

\tcolumn WeekOfYear
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: WeekOfYear

\tpartition Dim_Date = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    StartDate = #date(2025, 1, 1),
\t\t\t    EndDate = #date(2026, 12, 31),
\t\t\t    Duration = Duration.Days(EndDate - StartDate) + 1,
\t\t\t    DateList = List.Dates(StartDate, Duration, #duration(1, 0, 0, 0)),
\t\t\t    ToTable = Table.FromList(DateList, Splitter.SplitByNothing(), {{"Date"}}),
\t\t\t    ChangedType = Table.TransformColumnTypes(ToTable, {{{{"Date", type date}}}}),
\t\t\t    AddDateID = Table.AddColumn(ChangedType, "DateID", each Number.From(Date.Year([Date])) * 10000 + Number.From(Date.Month([Date])) * 100 + Number.From(Date.Day([Date])), Int64.Type),
\t\t\t    AddYear = Table.AddColumn(AddDateID, "Year", each Date.Year([Date]), Int64.Type),
\t\t\t    AddQuarter = Table.AddColumn(AddYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
\t\t\t    AddMonth = Table.AddColumn(AddQuarter, "Month", each Date.Month([Date]), Int64.Type),
\t\t\t    AddMonthName = Table.AddColumn(AddMonth, "MonthName", each Date.MonthName([Date]), type text),
\t\t\t    AddDOW = Table.AddColumn(AddMonthName, "DayOfWeek", each Date.DayOfWeek([Date], Day.Sunday) + 1, Int64.Type),
\t\t\t    AddDayName = Table.AddColumn(AddDOW, "DayName", each Date.DayOfWeekName([Date]), type text),
\t\t\t    AddIsWeekend = Table.AddColumn(AddDayName, "IsWeekend", each Date.DayOfWeek([Date], Day.Sunday) = 0 or Date.DayOfWeek([Date], Day.Sunday) = 6, type logical),
\t\t\t    AddSeason = Table.AddColumn(AddIsWeekend, "Season", each if List.Contains({{6,7,8}}, Date.Month([Date])) then "High" else if List.Contains({{4,5,9,10}}, Date.Month([Date])) then "Shoulder" else "Low", type text),
\t\t\t    AddFY = Table.AddColumn(AddSeason, "FiscalYear", each Date.Year([Date]), Int64.Type),
\t\t\t    AddFQ = Table.AddColumn(AddFY, "FiscalQuarter", each Date.QuarterOfYear([Date]), Int64.Type),
\t\t\t    AddWOY = Table.AddColumn(AddFQ, "WeekOfYear", each Date.WeekOfYear([Date]), Int64.Type)
\t\t\tin
\t\t\t    AddWOY
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Date.tmdl"), content)

# ============================================================
# 2. Dim_Property
# ============================================================
def gen_dim_property():
    content = f"""table Dim_Property
\tlineageTag: {guid()}

\tcolumn PropertyID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyID

\tcolumn PropertyName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyName

\tcolumn PropertyType
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyType

\tcolumn StarRating
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: StarRating

\tcolumn City
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: City

\tcolumn Country
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Country

\tcolumn TotalRooms
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: TotalRooms

\tcolumn CurrencyCode
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: CurrencyCode

\tcolumn IsActive
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsActive

\tpartition Dim_Property = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [PropertyID = Int64.Type, PropertyName = text, PropertyType = text, StarRating = Int64.Type, City = text, Country = text, TotalRooms = Int64.Type, CurrencyCode = text, IsActive = logical],
\t\t\t        {{
\t\t\t            {{1, "The Grand Azure", "Mid-Scale Hotel", 4, "Tel Aviv", "IL", 200, "USD", true}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Property.tmdl"), content)

# ============================================================
# 3. Dim_Channel
# ============================================================
def gen_dim_channel():
    content = f"""table Dim_Channel
\tlineageTag: {guid()}

\tcolumn ChannelID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ChannelID

\tcolumn ChannelName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ChannelName

\tcolumn ChannelType
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ChannelType

\tcolumn CommissionRate
\t\tdataType: double
\t\tformatString: 0.00%
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: CommissionRate

\tcolumn IsDirect
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsDirect

\tpartition Dim_Channel = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [ChannelID = Int64.Type, ChannelName = text, ChannelType = text, CommissionRate = number, IsDirect = logical],
\t\t\t        {{
\t\t\t            {{1, "Direct Website", "Direct", 0.0, true}},
\t\t\t            {{2, "Booking.com", "OTA", 0.15, false}},
\t\t\t            {{3, "Expedia", "OTA", 0.18, false}},
\t\t\t            {{4, "Corporate Direct", "Corporate", 0.05, true}},
\t\t\t            {{5, "GDS (Amadeus/Sabre)", "GDS", 0.10, false}},
\t\t\t            {{6, "Walk-in / Phone", "Direct", 0.0, true}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Channel.tmdl"), content)

# ============================================================
# 4. Dim_Department
# ============================================================
def gen_dim_department():
    content = f"""table Dim_Department
\tlineageTag: {guid()}

\tcolumn DepartmentID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DepartmentID

\tcolumn DepartmentName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DepartmentName

\tcolumn USALICategory
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: USALICategory

\tcolumn IsRevenueDept
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsRevenueDept

\tpartition Dim_Department = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [DepartmentID = Int64.Type, DepartmentName = text, USALICategory = text, IsRevenueDept = logical],
\t\t\t        {{
\t\t\t            {{1, "Rooms", "Revenue", true}},
\t\t\t            {{2, "Food & Beverage", "Revenue", true}},
\t\t\t            {{3, "Spa & Wellness", "Revenue", true}},
\t\t\t            {{4, "Other Revenue", "Revenue", true}},
\t\t\t            {{5, "Housekeeping", "Departmental", false}},
\t\t\t            {{6, "Maintenance", "Departmental", false}},
\t\t\t            {{7, "Admin & General", "Undistributed", false}},
\t\t\t            {{8, "Sales & Marketing", "Undistributed", false}},
\t\t\t            {{9, "Human Resources", "Undistributed", false}},
\t\t\t            {{10, "Finance", "Undistributed", false}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Department.tmdl"), content)

# ============================================================
# 5. Dim_Account (GL accounts - USALI mapped)
# ============================================================
def gen_dim_account():
    content = f"""table Dim_Account
\tlineageTag: {guid()}

\tcolumn AccountID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: AccountID

\tcolumn GLCode
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: GLCode

\tcolumn AccountName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: AccountName

\tcolumn AccountType
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: AccountType

\tcolumn USALILine
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: USALILine

\tcolumn ExpenseCategory
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ExpenseCategory

\tcolumn IsPayroll
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsPayroll

\tpartition Dim_Account = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [AccountID = Int64.Type, GLCode = text, AccountName = text, AccountType = text, USALILine = text, ExpenseCategory = text, IsPayroll = logical],
\t\t\t        {{
\t\t\t            {{1, "4010", "Room Revenue", "Revenue", "Rooms Revenue", null, false}},
\t\t\t            {{2, "4020", "F&B Revenue", "Revenue", "F&B Revenue", null, false}},
\t\t\t            {{3, "4030", "Spa Revenue", "Revenue", "Other Revenue", null, false}},
\t\t\t            {{4, "4040", "Other Operating Revenue", "Revenue", "Other Revenue", null, false}},
\t\t\t            {{5, "5010", "Rooms Payroll", "Expense", "Rooms Expense", "Payroll", true}},
\t\t\t            {{6, "5020", "F&B Payroll", "Expense", "F&B Expense", "Payroll", true}},
\t\t\t            {{7, "5030", "F&B Cost of Sales", "Expense", "F&B Expense", "COGS", false}},
\t\t\t            {{8, "5040", "Housekeeping Expense", "Expense", "Rooms Expense", "Operations", false}},
\t\t\t            {{9, "5050", "Maintenance & Repairs", "Expense", "Property Operations", "Maintenance", false}},
\t\t\t            {{10, "5060", "Utilities - Energy", "Expense", "Property Operations", "Energy", false}},
\t\t\t            {{11, "5070", "Utilities - Water", "Expense", "Property Operations", "Energy", false}},
\t\t\t            {{12, "6010", "Admin & General Payroll", "Expense", "Undistributed - A&G", "Payroll", true}},
\t\t\t            {{13, "6020", "Sales & Marketing", "Expense", "Undistributed - S&M", "Marketing", false}},
\t\t\t            {{14, "6030", "IT & Technology", "Expense", "Undistributed - A&G", "Admin", false}},
\t\t\t            {{15, "6040", "Insurance", "Expense", "Fixed Charges", "Admin", false}},
\t\t\t            {{16, "6050", "Property Tax", "Expense", "Fixed Charges", "Admin", false}},
\t\t\t            {{17, "6060", "Management Fees", "Expense", "Management Fees", "Admin", false}},
\t\t\t            {{18, "6070", "HR & Training", "Expense", "Undistributed - HR", "Payroll", true}},
\t\t\t            {{19, "7010", "Depreciation", "Expense", "Depreciation", "Depreciation", false}},
\t\t\t            {{20, "7020", "Interest Expense", "Expense", "Interest", "Finance", false}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Account.tmdl"), content)

# ============================================================
# 6. Dim_Segment
# ============================================================
def gen_dim_segment():
    content = f"""table Dim_Segment
\tlineageTag: {guid()}

\tcolumn SegmentID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: SegmentID

\tcolumn SegmentName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: SegmentName

\tpartition Dim_Segment = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [SegmentID = Int64.Type, SegmentName = text],
\t\t\t        {{
\t\t\t            {{1, "Leisure"}},
\t\t\t            {{2, "Corporate"}},
\t\t\t            {{3, "Group"}},
\t\t\t            {{4, "Government"}},
\t\t\t            {{5, "Loyalty"}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Segment.tmdl"), content)

# ============================================================
# 7. Dim_Outlet
# ============================================================
def gen_dim_outlet():
    content = f"""table Dim_Outlet
\tlineageTag: {guid()}

\tcolumn OutletID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: OutletID

\tcolumn OutletName
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: OutletName

\tcolumn OutletType
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: OutletType

\tpartition Dim_Outlet = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [OutletID = Int64.Type, OutletName = text, OutletType = text],
\t\t\t        {{
\t\t\t            {{1, "Room Revenue", "Rooms"}},
\t\t\t            {{2, "Azure Restaurant", "F&B"}},
\t\t\t            {{3, "Lobby Bar", "F&B"}},
\t\t\t            {{4, "Serenity Spa", "Spa"}},
\t\t\t            {{5, "Parking & Other", "Other"}}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Outlet.tmdl"), content)

# ============================================================
# 8. Dim_Guest (simplified, ~30 guests)
# ============================================================
def gen_dim_guest():
    nationalities = ["US","GB","DE","FR","IL","IL","IL","IT","ES","NL","JP","AU","CA","BR","IL"]
    segments = ["Leisure","Corporate","Leisure","Group","Leisure","Corporate","Loyalty","Leisure","Corporate","Leisure","Leisure","Loyalty","Corporate","Leisure","Leisure"]
    tiers = ["null","Gold","null","null","Silver","Platinum","Gold","null","Silver","null","null","Gold","null","null","Bronze"]

    rows = []
    for i in range(1, 31):
        nat = nationalities[(i-1) % len(nationalities)]
        seg = segments[(i-1) % len(segments)]
        tier = tiers[(i-1) % len(tiers)]
        visits = random.randint(1, 8)
        ltv = round(visits * random.uniform(400, 1200), 2)
        tier_val = f'"{tier}"' if tier != "null" else "null"
        rows.append(f'\t\t\t            {{{i}, "{nat}", "{seg}", {tier_val}, {visits}, {ltv}}}')

    rows_str = ",\n".join(rows)

    content = f"""table Dim_Guest
\tlineageTag: {guid()}

\tcolumn GuestID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: GuestID

\tcolumn NationalityCode
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: NationalityCode

\tcolumn Segment
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Segment

\tcolumn LoyaltyTier
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: LoyaltyTier

\tcolumn VisitCount
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: VisitCount

\tcolumn TotalLifetimeRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: TotalLifetimeRevenue

\tpartition Dim_Guest = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [GuestID = Int64.Type, NationalityCode = text, Segment = text, LoyaltyTier = text, VisitCount = Int64.Type, TotalLifetimeRevenue = number],
\t\t\t        {{
{rows_str}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Dim_Guest.tmdl"), content)

# ============================================================
# 9. Fact_Reservations (~100 rows per year)
# ============================================================
def gen_fact_reservations():
    channels = [1,2,3,4,5,6]
    channel_weights = [0.20, 0.30, 0.15, 0.15, 0.10, 0.10]
    segments = [1,2,3,4,5]
    seg_weights = [0.35, 0.25, 0.20, 0.05, 0.15]
    statuses = ["Checked-Out","Checked-Out","Checked-Out","Checked-Out","Cancelled","No-Show"]

    rows = []
    rid = 0
    for year in [2025, 2026]:
        for i in range(100):
            rid += 1
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            # Seasonality: higher ADR in summer
            season_mult = 1.0
            if month in [6,7,8]: season_mult = 1.25
            elif month in [4,5,9,10]: season_mult = 1.10
            elif month in [12,1,2]: season_mult = 0.90

            arrival_id = year * 10000 + month * 100 + day
            room_nights = random.choices([1,2,3,4,5,7], weights=[0.15,0.30,0.25,0.15,0.10,0.05])[0]
            dep_month = month
            dep_day = min(day + room_nights, 28)
            dep_id = year * 10000 + dep_month * 100 + dep_day

            book_lead = random.randint(1, 90)
            book_day = max(1, day - book_lead % 28)
            book_month = max(1, month - book_lead // 28)
            book_id = year * 10000 + book_month * 100 + book_day

            channel_id = random.choices(channels, weights=channel_weights)[0]
            segment_id = random.choices(segments, weights=seg_weights)[0]
            guest_id = random.randint(1, 30)

            adults = random.choices([1,2,3], weights=[0.3,0.6,0.1])[0]
            children = random.choices([0,0,0,1,2], weights=[0.5,0.2,0.1,0.1,0.1])[0]

            base_adr = random.uniform(180, 320) * season_mult
            # Year-over-year growth ~5%
            if year == 2026:
                base_adr *= 1.05

            gross_rev = round(base_adr * room_nights, 2)
            comm_rates = {1:0.0, 2:0.15, 3:0.18, 4:0.05, 5:0.10, 6:0.0}
            commission = round(gross_rev * comm_rates[channel_id], 2)
            discount = round(gross_rev * random.uniform(0, 0.08), 2)
            net_rev = round(gross_rev - commission - discount, 2)
            upsell = round(random.uniform(0, 80) * room_nights, 2) if random.random() > 0.4 else 0

            status = random.choice(statuses)
            cancel_id = "null"
            if status == "Cancelled":
                cancel_id = str(arrival_id - random.randint(1, 10))

            lead_time = book_lead
            loyalty = random.choice(["null",'"Bronze"','"Silver"','"Gold"','"Platinum"',"null","null"])

            row = f'\t\t\t            {{{rid}, 1, {guest_id}, {channel_id}, {segment_id}, {arrival_id}, {dep_id}, {book_id}, {room_nights}, {adults}, {children}, {gross_rev}, {net_rev}, {commission}, {discount}, {upsell}, "{status}", {cancel_id}, {lead_time}, {loyalty}}}'
            rows.append(row)

    rows_str = ",\n".join(rows)

    content = f"""table Fact_Reservations
\tlineageTag: {guid()}

\tcolumn ReservationID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ReservationID

\tcolumn PropertyID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyID

\tcolumn GuestID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: GuestID

\tcolumn ChannelID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ChannelID

\tcolumn SegmentID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: SegmentID

\tcolumn ArrivalDateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ArrivalDateID

\tcolumn DepartureDateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DepartureDateID

\tcolumn BookingDateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BookingDateID

\tcolumn RoomNights
\t\tdataType: int64
\t\tformatString: #,##0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: RoomNights

\tcolumn Adults
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Adults

\tcolumn Children
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Children

\tcolumn GrossRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: GrossRevenue

\tcolumn NetRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: NetRevenue

\tcolumn Commission
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Commission

\tcolumn DiscountAmount
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: DiscountAmount

\tcolumn UpsellRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: UpsellRevenue

\tcolumn Status
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: Status

\tcolumn CancellationDateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: CancellationDateID

\tcolumn LeadTimeDays
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: LeadTimeDays

\tcolumn LoyaltyTier
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: LoyaltyTier

\tpartition Fact_Reservations = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [ReservationID = Int64.Type, PropertyID = Int64.Type, GuestID = Int64.Type, ChannelID = Int64.Type, SegmentID = Int64.Type, ArrivalDateID = Int64.Type, DepartureDateID = Int64.Type, BookingDateID = Int64.Type, RoomNights = Int64.Type, Adults = Int64.Type, Children = Int64.Type, GrossRevenue = number, NetRevenue = number, Commission = number, DiscountAmount = number, UpsellRevenue = number, Status = text, CancellationDateID = Int64.Type, LeadTimeDays = Int64.Type, LoyaltyTier = text],
\t\t\t        {{
{rows_str}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Fact_Reservations.tmdl"), content)

# ============================================================
# 10. Fact_Revenue (~100 rows per year, monthly by outlet)
# ============================================================
def gen_fact_revenue():
    # 12 months x 5 outlets x 2 years = 120 rows per year... let's do monthly by outlet
    outlets = [1,2,3,4,5]
    outlet_base_rev = {1: 350000, 2: 95000, 3: 35000, 4: 15000, 5: 8000}  # monthly base
    season_mult = {1:0.85,2:0.82,3:0.95,4:1.05,5:1.10,6:1.25,7:1.30,8:1.28,9:1.12,10:1.08,11:0.92,12:0.88}

    rows = []
    rid = 0
    for year in [2025, 2026]:
        yoy = 1.0 if year == 2025 else 1.06  # 6% growth
        for month in range(1, 13):
            for oid in outlets:
                rid += 1
                date_id = year * 10000 + month * 100 + 15  # mid-month
                base = outlet_base_rev[oid] * season_mult[month] * yoy
                gross = round(base * random.uniform(0.92, 1.08), 2)
                tax = round(gross * 0.17, 2)  # 17% VAT
                net = round(gross - tax, 2)
                dept_id = oid  # outlets map to departments 1-5 roughly
                if oid == 5: dept_id = 4  # Other Revenue
                covers = random.randint(800, 2500) if oid in [2,3] else "null"
                txns = random.randint(200, 900) if oid in [2,3,4] else "null"

                row = f'\t\t\t            {{{rid}, {date_id}, 1, {oid}, {dept_id}, {gross}, {net}, {tax}, {covers}, {txns}}}'
                rows.append(row)

    rows_str = ",\n".join(rows)

    content = f"""table Fact_Revenue
\tlineageTag: {guid()}

\tcolumn RevenueID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: RevenueID

\tcolumn DateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DateID

\tcolumn PropertyID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyID

\tcolumn OutletID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: OutletID

\tcolumn DepartmentID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DepartmentID

\tcolumn GrossRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: GrossRevenue

\tcolumn NetRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: NetRevenue

\tcolumn TaxAmount
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: TaxAmount

\tcolumn Covers
\t\tdataType: int64
\t\tformatString: #,##0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Covers

\tcolumn Transactions
\t\tdataType: int64
\t\tformatString: #,##0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Transactions

\tpartition Fact_Revenue = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [RevenueID = Int64.Type, DateID = Int64.Type, PropertyID = Int64.Type, OutletID = Int64.Type, DepartmentID = Int64.Type, GrossRevenue = number, NetRevenue = number, TaxAmount = number, Covers = Int64.Type, Transactions = Int64.Type],
\t\t\t        {{
{rows_str}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Fact_Revenue.tmdl"), content)

# ============================================================
# 11. Fact_Expenses (~100 rows per year, monthly by dept/account)
# ============================================================
def gen_fact_expenses():
    # Monthly expenses by account (accounts 5-20)
    expense_accounts = list(range(5, 21))
    account_base = {
        5: 85000, 6: 42000, 7: 28000, 8: 22000, 9: 18000,
        10: 25000, 11: 8000, 12: 35000, 13: 30000, 14: 12000,
        15: 9000, 16: 7000, 17: 20000, 18: 15000, 19: 22000, 20: 18000
    }
    acct_dept = {
        5:1, 6:2, 7:2, 8:5, 9:6, 10:6, 11:6, 12:7, 13:8, 14:7, 15:7, 16:7, 17:7, 18:9, 19:10, 20:10
    }

    rows = []
    eid = 0
    for year in [2025, 2026]:
        yoy = 1.0 if year == 2025 else 1.04  # 4% cost growth
        for month in range(1, 13):
            # Pick ~8 accounts per month to get ~96 rows per year
            selected = random.sample(expense_accounts, 8)
            for acc_id in selected:
                eid += 1
                date_id = year * 10000 + month * 100 + 28
                base = account_base[acc_id] * yoy
                amount = round(base * random.uniform(0.85, 1.15), 2)
                budget = round(base * random.uniform(0.95, 1.05), 2)
                dept_id = acct_dept[acc_id]
                is_capex = "true" if acc_id == 19 else "false"

                row = f'\t\t\t            {{{eid}, {date_id}, 1, {dept_id}, {acc_id}, {amount}, {budget}, {is_capex}}}'
                rows.append(row)

    rows_str = ",\n".join(rows)

    content = f"""table Fact_Expenses
\tlineageTag: {guid()}

\tcolumn ExpenseID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: ExpenseID

\tcolumn DateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DateID

\tcolumn PropertyID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyID

\tcolumn DepartmentID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DepartmentID

\tcolumn AccountID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: AccountID

\tcolumn Amount
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: Amount

\tcolumn BudgetAmount
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: BudgetAmount

\tcolumn IsCapex
\t\tdataType: boolean
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: IsCapex

\tpartition Fact_Expenses = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [ExpenseID = Int64.Type, DateID = Int64.Type, PropertyID = Int64.Type, DepartmentID = Int64.Type, AccountID = Int64.Type, Amount = number, BudgetAmount = number, IsCapex = logical],
\t\t\t        {{
{rows_str}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Fact_Expenses.tmdl"), content)

# ============================================================
# 12. Fact_Budget (24 rows: 12 months x 2 years)
# ============================================================
def gen_fact_budget():
    budget_rev = {1:420000,2:400000,3:470000,4:520000,5:550000,6:620000,7:650000,8:640000,9:560000,10:530000,11:460000,12:440000}

    rows = []
    bid = 0
    for year in [2025, 2026]:
        yoy = 1.0 if year == 2025 else 1.08
        for month in range(1, 13):
            bid += 1
            date_id = year * 10000 + month * 100 + 1
            brev = round(budget_rev[month] * yoy, 2)
            bexp = round(brev * random.uniform(0.58, 0.65), 2)
            bocc = round(random.uniform(0.65, 0.92) * (1.15 if month in [6,7,8] else 1.0) * (0.9 if month in [1,2,12] else 1.0), 4)
            bocc = min(bocc, 0.98)
            badr = round(brev / (200 * 30 * bocc) if bocc > 0 else 0, 2)
            bhead = round(random.uniform(140, 165), 2)

            row = f'\t\t\t            {{{bid}, {date_id}, 1, {brev}, {bexp}, {bocc}, {badr}, {bhead}, {year}, "Original"}}'
            rows.append(row)

    rows_str = ",\n".join(rows)

    content = f"""table Fact_Budget
\tlineageTag: {guid()}

\tcolumn BudgetID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BudgetID

\tcolumn DateID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: DateID

\tcolumn PropertyID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: PropertyID

\tcolumn BudgetRevenue
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: BudgetRevenue

\tcolumn BudgetExpense
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: sum
\t\tsourceColumn: BudgetExpense

\tcolumn BudgetOccupancy
\t\tdataType: double
\t\tformatString: 0.00%
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BudgetOccupancy

\tcolumn BudgetADR
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BudgetADR

\tcolumn BudgetHeadcount
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BudgetHeadcount

\tcolumn FiscalYear
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: FiscalYear

\tcolumn BudgetVersion
\t\tdataType: string
\t\tlineageTag: {guid()}
\t\tsummarizeBy: none
\t\tsourceColumn: BudgetVersion

\tpartition Fact_Budget = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(
\t\t\t        type table [BudgetID = Int64.Type, DateID = Int64.Type, PropertyID = Int64.Type, BudgetRevenue = number, BudgetExpense = number, BudgetOccupancy = number, BudgetADR = number, BudgetHeadcount = number, FiscalYear = Int64.Type, BudgetVersion = text],
\t\t\t        {{
{rows_str}
\t\t\t        }}
\t\t\t    )
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "Fact_Budget.tmdl"), content)

# ============================================================
# 13. _Measures table (Phase 1 DAX measures)
# ============================================================
def gen_measures():
    g = guid  # shorthand
    content = f"""table _Measures
\tlineageTag: {g()}

\tmeasure 'Total Revenue' = SUM(Fact_Revenue[GrossRevenue])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Revenue

\tmeasure 'Net Revenue' = SUM(Fact_Revenue[NetRevenue])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Revenue

\tmeasure 'Rooms Revenue' = CALCULATE(SUM(Fact_Revenue[GrossRevenue]), Dim_Outlet[OutletType] = "Rooms")
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Revenue

\tmeasure 'F&B Revenue' = CALCULATE(SUM(Fact_Revenue[GrossRevenue]), Dim_Outlet[OutletType] = "F&B")
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Revenue

\tmeasure 'Occupied Room Nights' = CALCULATE(SUM(Fact_Reservations[RoomNights]), Fact_Reservations[Status] <> "Cancelled", Fact_Reservations[Status] <> "No-Show")
\t\tlineageTag: {g()}
\t\tformatString: #,##0
\t\tdisplayFolder: Occupancy

\tmeasure 'Available Room Nights' =
\t\tVAR DaysInPeriod = COUNTROWS(Dim_Date)
\t\tVAR TotalRooms = SUM(Dim_Property[TotalRooms])
\t\tRETURN DaysInPeriod * TotalRooms
\t\tlineageTag: {g()}
\t\tformatString: #,##0
\t\tdisplayFolder: Occupancy

\tmeasure 'Occupancy %' = DIVIDE([Occupied Room Nights], [Available Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Occupancy

\tmeasure ADR = DIVIDE([Rooms Revenue], [Occupied Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Revenue

\tmeasure RevPAR = DIVIDE([Rooms Revenue], [Available Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Revenue

\tmeasure TRevPAR = DIVIDE([Total Revenue], [Available Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Revenue

\tmeasure 'Net ADR' =
\t\tVAR NetRoomsRev = CALCULATE(SUM(Fact_Revenue[NetRevenue]), Dim_Outlet[OutletType] = "Rooms")
\t\tRETURN DIVIDE(NetRoomsRev, [Occupied Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Revenue

\tmeasure 'Total Expenses' = SUM(Fact_Expenses[Amount])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'Gross Profit' = [Total Revenue] - [Total Expenses]
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure GOP =
\t\tVAR DeptExpenses = CALCULATE(SUM(Fact_Expenses[Amount]), Dim_Department[USALICategory] IN {{"Revenue", "Departmental"}})
\t\tRETURN [Total Revenue] - DeptExpenses
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'GOP Margin %' = DIVIDE([GOP], [Total Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Profitability

\tmeasure EBITDA =
\t\tVAR AllExpExDepr = CALCULATE(SUM(Fact_Expenses[Amount]), Dim_Account[ExpenseCategory] <> "Depreciation", Dim_Account[ExpenseCategory] <> "Finance")
\t\tRETURN [Total Revenue] - AllExpExDepr
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'EBITDA Margin %' = DIVIDE([EBITDA], [Total Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Profitability

\tmeasure GOPPAR = DIVIDE([GOP], [Available Room Nights])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Profitability

\tmeasure 'Payroll Cost' = CALCULATE(SUM(Fact_Expenses[Amount]), Dim_Account[IsPayroll] = TRUE())
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'Payroll %' = DIVIDE([Payroll Cost], [Total Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Profitability

\tmeasure 'Net Profit' = [Total Revenue] - [Total Expenses]
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'Net Profit Margin %' = DIVIDE([Net Profit], [Total Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Profitability

\tmeasure 'Budget Revenue' = SUM(Fact_Budget[BudgetRevenue])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Budget

\tmeasure 'Budget Expense' = SUM(Fact_Budget[BudgetExpense])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Budget

\tmeasure 'Budget Variance $' = [Total Revenue] - [Budget Revenue]
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Budget

\tmeasure 'Budget Variance %' = DIVIDE([Budget Variance $], [Budget Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Budget

\tmeasure 'Budget Occupancy' = AVERAGE(Fact_Budget[BudgetOccupancy])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Budget

\tmeasure 'Budget ADR' = AVERAGE(Fact_Budget[BudgetADR])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Budget

\tmeasure 'Revenue LY' = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Time Intelligence

\tmeasure 'Revenue vs LY %' = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Time Intelligence

\tmeasure 'RevPAR LY' = CALCULATE([RevPAR], SAMEPERIODLASTYEAR(Dim_Date[Date]))
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Time Intelligence

\tmeasure 'Occupancy LY' = CALCULATE([Occupancy %], SAMEPERIODLASTYEAR(Dim_Date[Date]))
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Time Intelligence

\tmeasure 'ADR LY' = CALCULATE([ADR], SAMEPERIODLASTYEAR(Dim_Date[Date]))
\t\tlineageTag: {g()}
\t\tformatString: $#,##0.00
\t\tdisplayFolder: Time Intelligence

\tmeasure 'Total Reservations' = COUNTROWS(Fact_Reservations)
\t\tlineageTag: {g()}
\t\tformatString: #,##0
\t\tdisplayFolder: Bookings

\tmeasure 'Cancellation Rate' =
\t\tVAR Cancelled = CALCULATE(COUNTROWS(Fact_Reservations), Fact_Reservations[Status] = "Cancelled")
\t\tRETURN DIVIDE(Cancelled, [Total Reservations])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Bookings

\tmeasure 'No-Show Rate' =
\t\tVAR NoShows = CALCULATE(COUNTROWS(Fact_Reservations), Fact_Reservations[Status] = "No-Show")
\t\tRETURN DIVIDE(NoShows, [Total Reservations])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Bookings

\tmeasure 'Avg Lead Time' = AVERAGE(Fact_Reservations[LeadTimeDays])
\t\tlineageTag: {g()}
\t\tformatString: #,##0
\t\tdisplayFolder: Bookings

\tmeasure 'Avg Length of Stay' = AVERAGE(Fact_Reservations[RoomNights])
\t\tlineageTag: {g()}
\t\tformatString: #,##0.0
\t\tdisplayFolder: Bookings

\tmeasure 'Direct Booking %' =
\t\tVAR DirectBookings = CALCULATE(COUNTROWS(Fact_Reservations), Dim_Channel[IsDirect] = TRUE())
\t\tRETURN DIVIDE(DirectBookings, [Total Reservations])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Channels

\tmeasure 'OTA Commission Total' = SUM(Fact_Reservations[Commission])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Channels

\tmeasure 'Upsell Revenue' = SUM(Fact_Reservations[UpsellRevenue])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Revenue

\tmeasure 'Revenue per Channel' = DIVIDE(SUM(Fact_Reservations[NetRevenue]), DISTINCTCOUNT(Fact_Reservations[ChannelID]))
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Channels

\tmeasure 'Expense Variance $' = SUM(Fact_Expenses[Amount]) - SUM(Fact_Expenses[BudgetAmount])
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Budget

\tmeasure 'Expense Variance %' = DIVIDE([Expense Variance $], SUM(Fact_Expenses[BudgetAmount]))
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Budget

\tmeasure 'Energy Cost' = CALCULATE(SUM(Fact_Expenses[Amount]), Dim_Account[ExpenseCategory] = "Energy")
\t\tlineageTag: {g()}
\t\tformatString: $#,##0
\t\tdisplayFolder: Profitability

\tmeasure 'Energy Cost %' = DIVIDE([Energy Cost], [Total Revenue])
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Profitability

\tmeasure 'Repeat Guest Rate' =
\t\tVAR RepeatGuests = CALCULATE(DISTINCTCOUNT(Fact_Reservations[GuestID]), FILTER(VALUES(Dim_Guest[GuestID]), CALCULATE(COUNTROWS(Fact_Reservations)) > 1))
\t\tVAR TotalGuests = DISTINCTCOUNT(Fact_Reservations[GuestID])
\t\tRETURN DIVIDE(RepeatGuests, TotalGuests)
\t\tlineageTag: {g()}
\t\tformatString: 0.0%
\t\tdisplayFolder: Guest

\tpartition _Measures = m
\t\tmode: import
\t\tsource
\t\t\tlet
\t\t\t    Source = #table(type table {{}}, {{{{}}}})
\t\t\tin
\t\t\t    Source
"""
    write_file(os.path.join(TABLES_DIR, "_Measures.tmdl"), content)

# ============================================================
# 14. model.tmdl (updated with refs and relationships)
# ============================================================
def gen_model():
    g = guid
    content = f"""model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-IL
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBI_ProTooling = ["DevMode"]

ref cultureInfo en-US

ref table Dim_Date
ref table Dim_Property
ref table Dim_Channel
ref table Dim_Department
ref table Dim_Account
ref table Dim_Segment
ref table Dim_Outlet
ref table Dim_Guest
ref table Fact_Reservations
ref table Fact_Revenue
ref table Fact_Expenses
ref table Fact_Budget
ref table _Measures

relationship {g()}
\tfromColumn: Fact_Reservations.ArrivalDateID
\ttoColumn: Dim_Date.DateID

relationship {g()}
\tfromColumn: Fact_Reservations.PropertyID
\ttoColumn: Dim_Property.PropertyID

relationship {g()}
\tfromColumn: Fact_Reservations.ChannelID
\ttoColumn: Dim_Channel.ChannelID

relationship {g()}
\tfromColumn: Fact_Reservations.SegmentID
\ttoColumn: Dim_Segment.SegmentID

relationship {g()}
\tfromColumn: Fact_Reservations.GuestID
\ttoColumn: Dim_Guest.GuestID

relationship {g()}
\tfromColumn: Fact_Revenue.DateID
\ttoColumn: Dim_Date.DateID

relationship {g()}
\tfromColumn: Fact_Revenue.PropertyID
\ttoColumn: Dim_Property.PropertyID

relationship {g()}
\tfromColumn: Fact_Revenue.OutletID
\ttoColumn: Dim_Outlet.OutletID

relationship {g()}
\tfromColumn: Fact_Revenue.DepartmentID
\ttoColumn: Dim_Department.DepartmentID

relationship {g()}
\tfromColumn: Fact_Expenses.DateID
\ttoColumn: Dim_Date.DateID

relationship {g()}
\tfromColumn: Fact_Expenses.PropertyID
\ttoColumn: Dim_Property.PropertyID

relationship {g()}
\tfromColumn: Fact_Expenses.DepartmentID
\ttoColumn: Dim_Department.DepartmentID

relationship {g()}
\tfromColumn: Fact_Expenses.AccountID
\ttoColumn: Dim_Account.AccountID

relationship {g()}
\tfromColumn: Fact_Budget.DateID
\ttoColumn: Dim_Date.DateID

relationship {g()}
\tfromColumn: Fact_Budget.PropertyID
\ttoColumn: Dim_Property.PropertyID
"""
    write_file(os.path.join(SM_DEF, "model.tmdl"), content)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Generating DEEPLY Hospitality Dashboard - Semantic Model...")
    print()

    gen_dim_date()
    gen_dim_property()
    gen_dim_channel()
    gen_dim_department()
    gen_dim_account()
    gen_dim_segment()
    gen_dim_outlet()
    gen_dim_guest()
    gen_fact_reservations()
    gen_fact_revenue()
    gen_fact_expenses()
    gen_fact_budget()
    gen_measures()
    gen_model()

    print()
    print("Done! Generated 14 files.")
    print(f"Tables: {len(os.listdir(TABLES_DIR))} TMDL files")
