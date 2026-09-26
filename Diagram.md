```mermaid
flowchart TD
    %% Source Data
    subgraph RawData ["1. Raw Data Input"]
        RAW["KNBS Report Workbooks<br/>(118 Excel Tables across 9 Chapters)"]
    end

    %% Processing Pipeline
    subgraph Pipeline ["2. Data Processing Pipeline"]
        SRC_C["src/counties.py<br/>• 47-County Reference List<br/>• Name Normalization"]
        SRC_P["src/parser.py<br/>• Forward-fills merged cells<br/>• Strips footnotes & blank rows<br/>• Handles multi-column layouts"]
        
        parse_county["parse_county_table()"]
        parse_simple["parse_simple_table()"]

        RAW --> SRC_P
        SRC_C -. Reference .-> SRC_P
        SRC_P -->|72 County Tables| parse_county
        SRC_P -->|46 National/Reference Tables| parse_simple
    end

    %% Processed Outputs & Quality Control
    subgraph ProcessedData ["3. Processed Data Layer"]
        QC["qc_log.json<br/>(Parser Diagnostics & Match Rates)"]
        TBL_C["data/processed/tables/<br/>(72 Tidy County CSVs)"]
        TBL_N["data/processed/tables_national/<br/>(46 Tidy Reference CSVs)"]
        EST_FIN["chapter7_ESTIMATED_housing_finance.csv<br/>(Modeled Finance Estimate)"]
        
        parse_county --> TBL_C
        parse_simple --> TBL_N
        SRC_P --> QC
    end

    %% Master Aggregation & Indexing
    subgraph MasterTable ["4. Aggregation & Composite Index"]
        M_INDICATORS["master_county_indicators.csv<br/>(47 Counties × 11 Headline Indicators)"]
        
        INDEX["Housing Affordability & Quality Index (0–100)<br/>• 35% Quality<br/>• 20% Water<br/>• 20% Sanitation<br/>• 25% Affordability"]

        TBL_C --> M_INDICATORS
        EST_FIN --> M_INDICATORS
        M_INDICATORS --> INDEX
    end

    %% Analysis & Deliverables
    subgraph Deliverables ["5. Analysis & Deliverables"]
        NB["notebooks/01_khs_housing_analysis.ipynb<br/>• Analysis Walkthrough<br/>• Executed Outputs"]
        CHARTS["images/<br/>• 6 Visualization Charts"]
        REPORT["reports/KHS_2024_Policy_Brief.docx<br/>• 13-Page Non-Technical Brief"]

        INDEX --> NB
        NB --> CHARTS
        NB --> REPORT
    end

    %% Styling
    style Pipeline fill:#e1f5fe,stroke:#0288d1,stroke-width:1px
    style ProcessedData fill:#fff3e0,stroke:#f57c00,stroke-width:1px
    style MasterTable fill:#e8f5e9,stroke:#388e3c,stroke-width:1px
    style Deliverables fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px
