# AI Tool Usage Disclosure

In accordance with the DSA 210 course policy on AI tool use, this document discloses how AI was used in this project.

## Tool Used
**Claude (Anthropic)** — accessed via claude.ai

## What I Did Myself

- Selected the project topic based on personal context (family-owned plastic injection factory in Osmaniye supplying yogurt producers).
- Wrote the original project proposal.
- Provided the raw monthly sales data (3 years, by week) from the factory.
- Decided which external variables to include and why (temperature for demand seasonality, Brent oil for raw material cost proxy, USD/TRY for FX exposure on imported feedstock).
- Specified that the factory is in Osmaniye and that customers are nationwide, which informed the population-weighted Turkey-average temperature design.
- Wrote the scripts that claude helped me while writing 
- Ran every script notebook on my own machine and verified outputs.
- Reviewed every observation and conclusion in the notebooks against my own intuition from the business.

## What Claude Helped With

### 1. `collect_data.py`
Claude helped me to the wrote the scripts that:
- Fetches daily weather for 10 Turkish cities from Open-Meteo's historical API
- Fetches Brent crude (`BZ=F`) and USD/TRY (`TRY=X`) from Yahoo Finance via `yfinance`
- Aggregates everything to ISO weeks (Monday–Sunday)
- Computes a population-weighted Turkey-average temperature


### 2. `01_eda.ipynb`
Claude drafted the EDA notebook structure and helped to write code: data loading, time-series plots, year-over-year comparison, monthly/seasonal boxplots, correlation heatmap, distribution and Q-Q plots, and the temperature-vs-sales scatter plots. I reviewed each plot's interpretation against my domain understanding before accepting it.

### 3. `02_hypothesis_tests.ipynb`
Claude helped the choice of non-parametric tests (justified by Shapiro-Wilk normality rejection), Mann-Whitney U for season comparisons, Spearman correlation for temperature/oil/FX relationships, Kruskal-Wallis with Bonferroni-corrected post-hoc comparisons, and the first-difference analysis to address spurious correlation in USD/TRY.

### 4. Project planning
Claude helped lay out the timeline against the course deadlines and recommended what to prioritize before each milestone.

## Sample Prompts Used

- "Veri toplama scriptini yazmama yardım et nereden başlamalıyım; fabrika Osmaniye'de, satışlar tüm Türkiye'ye, hava durumu Türkiye geneli ağırlıklı ortalama olsun."
- "örnek EDA notebooku hazırla ve tek tek neler yapacağımı açıkla — zaman serisi, mevsimsellik, sıcaklık-satış scatter, korelasyon heatmap'i ile."
- "hangi hipotez testlerini nasıl kullanmalıyım, örnek hipotez testleri notebook'u hazırla ve bana sebebini ve açıklamalarını yaz — yaz vs kış, sıcaklık-satış, mevsimler arası fark, petrol fiyatı ve USD/TRY için."
- "Proposalım yeterli mi, eksik var mı?"

## Verification Process

For every code cell Claude generated, I:
1. Ran it on my own machine and confirmed the output matched expectations.
2. Read through it to understand what each step does (especially: why non-parametric tests, why first differences for USD/TRY, why population-weighted temperature).
3. Compared the generated interpretations to my own domain knowledge of the dairy/plastics business before accepting them in the notebook.

