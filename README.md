# EAF Slag Utilization Decision Tool

## Overview

Electric Arc Furnace (EAF) slag is a major by-product of steelmaking. Traditionally treated as waste, EAF slag can often be recycled into valuable applications such as construction materials and cement additives.

This application evaluates **potential recycling routes for EAF slag** based on slag chemistry, environmental considerations, and available infrastructure.

The tool provides **recommendations for sustainable slag utilization**.

---

## Problem Description

EAF slag is produced during refining reactions in steelmaking when impurities react with fluxes such as lime.

Typical slag generation rates:

100–150 kg per ton of steel.

If not properly managed, slag disposal can create:

- environmental challenges
- landfill costs
- loss of valuable materials

However, slag can often be reused in industrial applications.

This tool helps determine the **most suitable recycling pathway**.

---

## Metallurgical Background

EAF slag consists primarily of oxide phases.

Typical composition:

| Component | Typical Range |
|--------|--------|
| CaO | 25 – 45 % |
| SiO₂ | 10 – 25 % |
| FeO | 10 – 30 % |
| MgO | 5 – 10 % |

Key parameters influencing slag utilization include:

### Basicity

Basicity is defined as:

Basicity = CaO / SiO₂

This ratio affects slag reactivity and suitability for construction applications.

### Free CaO

Free CaO can cause **volume expansion** due to hydration reactions:

CaO + H₂O → Ca(OH)₂

Slag with high free CaO must undergo **aging or stabilization** before reuse.

### Trace Metals

Trace elements such as:

- Chromium
- Lead
- Zinc

must be evaluated to ensure compliance with environmental regulations.

---

## Methodology

The application uses a **rule-based decision system**.

Users provide inputs including:

- FeO content
- Basicity ratio
- Free CaO risk
- Trace metal levels
- Available industrial outlets

The tool evaluates these inputs and ranks potential utilization routes.

---

## Recycling Routes

### Road Construction

EAF slag can be used as:

- road base material
- asphalt aggregate
- railway ballast

Advantages include high mechanical strength and durability.

### Cement Applications

Slag may be used as a component in cement or construction materials if its chemical composition is suitable.

### Metal Recovery

Metallic iron can be recovered from slag through crushing and magnetic separation.

### Landfill

Landfill is considered the **least desirable option** and is recommended only when recycling is not feasible.

---

## Results

The tool provides:

- Recommended slag utilization route
- Alternative options
- Explanation of the decision logic
- Environmental screening summary

---

## Code Structure

The application includes:

1. Input interface for slag properties
2. Environmental screening logic
3. Recycling route scoring system
4. Result visualization

The interface is implemented using **Streamlit**.

##References

-  Electric arc furnace slag as natural aggregate replacement in concrete production. Saveria Monosi, Maria Letizia Ruello*, Daniela Sani.
- The potential of industrial waste: Electric arc furnace slag (EAF) as recycled road construction materials. Patimapon Sukmak a, Gampanart Sukmak a, Pre DeSilva b, Suksun Horpibulsuk.
- A critical analysis of electric arc furnace (EAF) slag for sustainable geopolymer concrete production. Kamal Kishore , M. Neaz Sheikh , Muhammad N.S. Hadi
- Heavy metal recovery from electric arc furnace steel slag by using hydrochloric acid leaching. Lim Jin Wei1, 2 , Ong Teng Haan1, Thomas Choong Shean Yaw2, Luqman Chuah
- Verordnung über Anforderungen an den Einbau von mineralischen Ersatzbaustoffen in technische Bauwerke (Ersatzbaustoffverordnung - ErsatzbaustoffV)
- Verordnung über Deponien und Langzeitlager  (Deponieverordnung – DepV) Vom 27. April 2009, BGBl. I S. 900
- Directive 2008/98/EC of the European Parliament and of the Council of 19 November 2008 on waste and repealing certain Directives.https://eurlex.europa.eu/eli/dir/2008/98/oj

