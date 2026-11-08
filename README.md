# Peel Region: Population Density vs. Household Income

## Question
Does population density predict median after-tax household income across Peel Region census tracts, and do the results show spatial patterns?

## Data
2021 Census data for 272 census tracts (Region of Peel Census Information Hub). Density recomputed in a projected CRS (UTM 17N) because Web Mercator inflates area at this latitude.

## Method
- Global Moran's I (inverse-distance weights) on income and density
- OLS regression of income on density
- Moran's I on the regression residuals, and maps of income and residuals

## Results
- Income is spatially clustered (Moran's I = 0.19, p < 0.001); density clusters weakly (0.073)
- Denser tracts have lower income: about $2,750 less per additional 1,000 people/km² (R² = 0.081)
- Residuals are clustered (Moran's I = 0.209), so the regression's assumptions are violated

## Limitations
- Density explains only ~8% of income variation
- Clustered residuals mean the p-value is likely too optimistic; spatial lag/error models are a natural next step
- Tracts vary hugely in size (large rural tracts in Caledon vs. small urban ones)
