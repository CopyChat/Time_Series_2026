# Energy time-series reduction: topic, keywords and reference list

Prepared 2026-10-11 for the Teams call with Matti Koivisto (DTU Wind and Energy Systems), Monday 12 October 2026, 9:00 CEST.

## 1. Source: e-mail thread "Next visit to DTU Wind"

| Date | From | Content relevant to the topic |
|---|---|---|
| 2026-09-29 | Chao Tang | Asks for background on "the energy timeseries study you have proposed" before the visit (10 Nov 2026 – 5 Feb 2027). |
| 2026-09-29 | Matti Koivisto | Does not remember the details; asks whether the focus is time-series data analysis and what the objective would be. |
| 2026-09-30 | Chao Tang | Restates the topic: a short project (a few months) on time-series analysis, bias correction, principal component analysis and machine learning (keywords of CNU section 61). Concrete idea discussed earlier: reducing the size of energy/electricity time series, e.g. aggregation into representative periods or compression by principal component analysis, for model training and validation. |
| 2026-10-05 | Matti Koivisto | "Yes, the methods and topics you mention are indeed interesting for us." Proposes a 30-min online meeting. |
| 2026-10-08 | Matti Koivisto | Teams invitation for Mon 12 Oct 2026, 9:00 CEST. |

**Status of the topic:** the thread contains no written proposal from Matti. The topic below is Chao's restatement, which Matti accepted as interesting. The objective is still open and is the point to settle in the call.

**Working topic:** reduce long, high-resolution energy time series (wind, solar, demand, prices; hourly, multi-decade) to a small representative set while keeping what matters for the model that uses them (energy system optimisation, machine-learning training and validation).

## 2. Keywords and definitions

| Keyword | Definition |
|---|---|
| Time-series aggregation (TSA) | Methods that replace the full input time series of an energy system model (for example 8760 hourly steps per year × several decades) with fewer time steps, keeping the main statistical information. |
| Representative periods (typical days or weeks) | A small set of periods (days or weeks), each with a weight equal to the number of original periods it stands for. Model operation is solved only on these periods. |
| Clustering (k-means, k-medoids, hierarchical, k-shape) | Unsupervised machine learning that groups similar periods. The representative is either the cluster centroid (an average, not a real day) or the medoid (a real day from the data). |
| Principal component analysis (PCA) / empirical orthogonal functions (EOF) | Linear transform that projects the data onto orthogonal directions ordered by explained variance. Keeping the first k components compresses the data. |
| Autoencoder | Neural network trained to reproduce its input through a low-dimensional bottleneck layer. It is a nonlinear alternative to PCA for dimensionality reduction. |
| Chronology and seasonal storage | Many TSA schemes break the time order of the series. Models with long-term (seasonal) storage need TSA formulations that link representative periods across the year. |
| Extreme or peak periods | Days with low wind, low solar output or peak demand. Clustering averages them out, so they are often added explicitly. |
| A priori vs a posteriori aggregation | An a priori scheme uses only the input time series. An a posteriori scheme also uses model outputs (dispatch, storage) to choose the periods. |
| Inter-annual variability | Year-to-year differences in wind and solar output. Results from one weather year may not hold over several decades. |
| Bias correction / validation | Adjusting simulated wind or solar series (reanalysis, climate models) to match observed generation, and testing them against measurements. |
| Surrogate / emulator model | A fast machine-learning model trained on outputs of an expensive simulation model. Its training set can be selected with TSA or sampling. |
| CorRES | Correlations in Renewable Energy Sources: the DTU Wind tool that simulates wind and solar generation and forecast-error time series (Koivisto et al., 2018/2019). |

Compression by principal component analysis, in plain notation:

```
  X  (n periods × p features, e.g. n = 365 days, p = 24 h × variables), centred column-wise

  X  ≈  Z_k · W_kᵀ          W_k = first k eigenvectors of the covariance matrix  C = Xᵀ X / (n − 1)
                            Z_k = X · W_k      (n × k scores, k ≪ p)

                       λ_1 + … + λ_k
  explained variance = ─────────────     (λ_i = eigenvalues of C, sorted in decreasing order)
                       λ_1 + … + λ_p
```

Weighted representative periods (output of the clustering step):

```
  total annual quantity  ≈  Σ_c  w_c · Σ_t x_c(t)        w_c = number of original days in cluster c
                                                          Σ_c w_c = 365
```

## 3. Reference list (25 papers)

**How the list was checked**
- Metadata: every entry was resolved by DOI on OpenAlex. The BibTeX was then fetched from doi.org (Crossref/DataCite) and checked with `verify_bib.py`: 25/25 VERIFIED (report: `all_refs_25_verify_report.md`).
- Read scope: abstract only for all papers, except items 8 and 17 (abstract not accessed, title only). No full text was read, so no specific number beyond what the abstract states is cited here.
- Main findings in the table are quoted or closely paraphrased from each abstract.
- PDF: 13 PDFs downloaded (12 open-access by script, 1 publisher version downloaded manually: item 6). arXiv or repository copies are preprints or accepted manuscripts, not the publisher version. The other 12 are behind publisher paywalls or blocked scripted download.
- Zotero: all 25 are in collection `Projects/Time_Series_2026` (imported 2026-10-15). The keyword search of 2026-10-11 missed 4 papers already in the library (#19, #21, #22, #23, found by DOI on 2026-10-15); Zotero holds full PDFs of #19, #21 and #22, so 16 of 25 now have a PDF.

### A. Time-series aggregation: reviews and method comparisons

| # | Reference | Research topic | Main finding (abstract) | PDF |
|---|---|---|---|---|
| 1 | Hoffmann, Kotzur, Stolten, Robinius (2020). A review on time series aggregation methods for energy system models. *Energies* 13(3), 641. doi:10.3390/en13030641 · cited 225 | Review of TSA methods in 130 publications | "The future of TSA is clearly feature-based including clustering and other machine learning techniques"; growing focus on bounding the TSA-induced error of the optimisation result. | ✓ (MDPI) |
| 2 | Teichgraeber, Brandt (2022). Time-series aggregation for the optimization of energy systems: goals, challenges, approaches, and opportunities. *Renew. Sustain. Energy Rev.* 157, 111984. doi:10.1016/j.rser.2021.111984 · cited 160 | Review and best practices | Recommends: (1) measure performance on the optimisation outcome, validated on the full time series; (2) tune the method to the problem and data; (3) aggregate wind data with extra care; (4) bound the objective error; (5) add real extreme days. | – |
| 3 | Kotzur, Markewitz, Robinius, Stolten (2018). Impact of different time series aggregation methods on optimal energy system design. *Renew. Energy* 117, 474–487. doi:10.1016/j.renene.2017.10.017 · cited 371 | Comparison of aggregation methods across energy system types | Averaged values underestimate system cost compared with representative periods taken from the original series. The method itself (e.g. k-means) "plays a minor role"; systems with more renewables need more typical periods. | ✓ (arXiv preprint) |
| 4 | Kotzur, Markewitz, Robinius, Stolten (2018). Time series aggregation for energy system design: modeling seasonal storage. *Appl. Energy* 213, 123–135. doi:10.1016/j.apenergy.2018.01.023 · cited 303 | Linking typical periods for seasonal storage | Independent typical periods cannot exchange energy, so seasonal storage is not represented. The paper proposes a formulation that links them. | ✓ (arXiv preprint) |
| 5 | Teichgraeber, Brandt (2019). Clustering methods to find representative periods for the optimization of energy systems: an initial framework and comparison. *Appl. Energy* 239, 1283–1293. doi:10.1016/j.apenergy.2019.02.012 · cited 258 | k-means, k-medoids, hierarchical, DBA and k-shape clustering compared | Centroid methods represent operation more predictably but bias the objective. k-shape helps for intra-day problems (battery). A better clustering score does not imply a better objective value. | – |
| 6 | Pfenninger (2017). Dealing with multiple decades of hourly wind and PV time series in energy models. *Appl. Energy* 197, 1–13. doi:10.1016/j.apenergy.2017.03.051 · cited 369 | Downsampling vs clustering vs heuristics; Great Britain, 25 years | "No one-size-fits-all approach" to time-step reduction. Strong inter-annual variability means results based on one or a few years are likely unreliable. | ✓ (publisher version, downloaded manually) |
| 7 | Poncelet, Höschle, Delarue, Virag, D'haeseleer (2017). Selecting representative days for capturing the implications of integrating intermittent renewables in generation expansion planning problems. *IEEE Trans. Power Syst.* 32(3), 1936–1948. doi:10.1109/TPWRS.2016.2596803 · cited 342 | Metrics of representativeness; optimisation-based day selection | The optimisation-based selection is more accurate than literature approaches at equal model cost, but is computationally costly to run. | ✓ (KU Leuven repository) |
| 8 | Nahmmacher, Schmid, Hirth, Knopf (2016). Carpe diem: a novel approach to select representative days for long-term power system modeling. *Energy* 112, 430–442. doi:10.1016/j.energy.2016.06.081 · cited 288 | Representative day selection (title only) | Abstract not accessed: no finding stated. | – |
| 9 | Scott, Carvalho, Botterud, Silva (2019). Clustering representative days for power systems generation expansion planning: capturing the effects of variable renewables and energy storage. *Appl. Energy* 253, 113603. doi:10.1016/j.apenergy.2019.113603 · cited 128 | Adjusting clustering output (net demand level, shape, peak) | The weighting method reduces the cost error of representative-day expansion models by 61% on average (error of the representative-day model relative to the full model, stated in the abstract). | – |
| 10 | Hoffmann, Kotzur, Stolten (2022). The Pareto-optimal temporal aggregation of energy system models. *Appl. Energy* 315, 119029. doi:10.1016/j.apenergy.2022.119029 · cited 106 | Trade-off between number of typical days and within-day resolution; distribution-preserving representation | Improves on state-of-the-art clustering in a building model and a European carbon-neutral scenario (hundreds of runs). | ✓ (arXiv preprint) |
| 11 | Kotzur et al. (2021). A modeler's guide to handle complexity in energy systems optimization. *Adv. Appl. Energy* 4, 100063. doi:10.1016/j.adapen.2021.100063 · cited 201 | Review of complexity-reduction methods (aggregation, decomposition) | Gives a guide for modellers who hit computational limits. Many drivers of complexity can be avoided by model design. | ✓ (arXiv preprint) |
| 12 | Gonzato, Bruninx, Delarue (2021). Long term storage in generation expansion planning models with a reduced temporal scope. *Appl. Energy* 298, 117168. doi:10.1016/j.apenergy.2021.117168 · cited 81 | TSA and model formulations for long-term storage | Approximating the time series well does not imply approximating the planning solution well. Choosing hours vs days matters more than the TSA method. Long-term storage investment can be off by more than a factor of 2. | ✓ (working paper) |

### B. Climate-scale samples and machine learning / dimensionality reduction

| # | Reference | Research topic | Main finding (abstract) | PDF |
|---|---|---|---|---|
| 13 | Hilbers, Brayshaw, Gandy (2019). Importance subsampling: improving power system planning under climate-based uncertainty. *Appl. Energy* 251, 113114. doi:10.1016/j.apenergy.2019.04.110 · cited 59 | Subsampling 36 years of UK hourly data | Single years or representative days give significant design errors and capacity shortages. Importance subsampling gives accurate designs at much lower cost. | ✓ (arXiv preprint) |
| 14 | Hilbers, Brayshaw, Gandy (2023). Reducing climate risk in energy system planning: a posteriori time series aggregation for models with storage. *Appl. Energy* 334, 120624. doi:10.1016/j.apenergy.2022.120624 · cited 29 | Aggregation that uses model operational variables and keeps chronology | Lower error on the input series does not in general give more accurate model outputs. A posteriori schemes adapt to the system and handle storage. | ✓ (arXiv preprint) |
| 15 | Barbar, Mallapragada (2022). Representative period selection for power system planning using autoencoder-based dimensionality reduction. arXiv:2204.13608 (preprint, not peer reviewed). doi:10.48550/arXiv.2204.13608 · cited 3 | Autoencoder before clustering; extra features from simplified model runs | Dimensionality reduction improves clustering and allows model-output features. Error vs the full capacity expansion model is lower across networks and scenarios. | ✓ (arXiv) |
| 16 | Bogensperger, Fabel, Ferstl (2022). Accelerating energy-economic simulation models via machine learning-based emulation and time series aggregation. *Energies* 15(3), 1239. doi:10.3390/en15031239 · cited 6 | TSA and sampling to build training sets for ML emulators | k-means cluster sampling and adaptive sampling work best for small sample sizes. | ✓ (MDPI) |
| 17 | Ahlborn (2020). Principal component analysis of West European wind power generation. *Eur. Phys. J. Plus* 135(7). doi:10.1140/epjp/s13360-020-00585-4 · cited 5 | PCA of wind power (title only) | Abstract not accessed: no finding stated. | – |
| 18 | Grams, Beerli, Pfenninger, Staffell, Wernli (2017). Balancing Europe's wind-power output through spatial deployment informed by weather regimes. *Nat. Clim. Change* 7(8), 557–562. doi:10.1038/nclimate3338 · cited 419 | Weather regimes as drivers of multi-day wind variability | Mean European wind generation ranges from 22 to 44 GW across regimes (current fleet, as stated in the abstract). Regime-aware siting (e.g. the Balkans instead of the North Sea) nearly removes these output differences. | – |

### C. DTU / Koivisto group: simulated series, validation, bias correction, surrogates

| # | Reference | Research topic | Main finding (abstract) | PDF |
|---|---|---|---|---|
| 19 | Koivisto, Das, Guo, Sørensen, Nuño, Cutululis, Maule (2019, online 2018). Using time series simulation tools for assessing the effects of variable renewable energy generation on power and energy systems. *WIREs Energy Environ.* 8(3), e329. doi:10.1002/wene.329 · cited 90 | CorRES simulation tool | CorRES combines meteorological time series and stochastic simulation to produce consistent wind/solar generation and forecast-error series down to minute resolution. Three case studies. | – |
| 20 | Omoyele, Hoffmann, Koivisto, Larrañeta, Weinand, Linßen, Stolten (2024). Increasing the resolution of solar and wind time series for energy system modeling: a review. *Renew. Sustain. Energy Rev.* 189, 113792. doi:10.1016/j.rser.2023.113792 · cited 61 | Temporal downscaling of irradiance and wind speed (the reverse direction of TSA) | Stochastic and non-dimensional methods dominate for solar. For wind, reanalysis combined with stochastic fluctuations beats interpolation. | – |
| 21 | Murcia, Koivisto, Luzia, Olsen, Hahmann, Sørensen, Als (2022). Validation of European-scale simulated wind speed and wind generation time series. *Appl. Energy* 305, 117794. doi:10.1016/j.apenergy.2021.117794 · cited 107 | Validation of ERA5, NEWA and EIWR for simulating wind generation (32 masts, 12 countries, 2015–2018) | Ranks the datasets by distributions, daily patterns, autocorrelation and spatial correlation, with optional scaling to the Global Wind Atlas. | – (OA at publisher, scripted download blocked) |
| 22 | Luzia, Koivisto, Hahmann (2023). Validating EURO-CORDEX climate simulations for modelling European wind power generation. *Renew. Energy* 217, 118989. doi:10.1016/j.renene.2023.118989 · cited 19 | Validation and bias adjustment of 7 regional climate models | With Global Wind Atlas adjustment, EURO-CORDEX matches or beats ERA5 for temporal dependence and distributions, but spatial correlations are exaggerated. | – |
| 23 | Dalton, Bekker, Koivisto (2021). Classified atmospheric states as operating scenarios in probabilistic power flow analysis for networks with high levels of wind power. *Energy Rep.* 7, 3775–3784. doi:10.1016/j.egyr.2021.06.060 · cited 9 | Clustering generation data by classified atmospheric states (11 wind farms, South Africa) | Operating scenarios clustered by atmospheric state reduce simulation uncertainty in probabilistic power flow compared with an unclustered base state. | ✓ (DTU Orbit) |
| 24 | Staffell, Pfenninger (2016). Using bias-corrected reanalysis to simulate current and future wind power output. *Energy* 114, 1224–1239. doi:10.1016/j.energy.2016.08.068 · cited 1507 | Bias correction of MERRA/MERRA-2 wind power, 23 countries | MERRA overestimates output by 50% in north-west Europe and underestimates it by 30% in the Mediterranean. After national calibration, hourly national output reaches R² > 0.95. | – (OA at publisher, scripted download blocked) |
| 25 | Quick, Murcia Leon, Kanellas, Yamujala, Das, Koivisto (2024). Surrogate-based modeling and sensitivity analysis of future European electricity spot market prices. *Electr. Power Syst. Res.* 234, 110675. doi:10.1016/j.epsr.2024.110675 · cited 10 | Multi-output support vector regression as surrogate of price time series | Solar and wind costs drive electricity prices. Natural gas costs drive peak prices and prices far in the future. | – |

Citation counts: OpenAlex, 2026-10-11.

## 4. Points to raise in the call

The items below are proposals by the author of this note, not findings from the papers.

- **Objective.** Matti asked (29 Sep) for a possible objective. One option: "Which reduction of multi-decade CorRES wind/solar/demand series (clustering, PCA, autoencoder) keeps the outcomes of a DTU energy system model, such as Balmorel, within a target error?" This follows the evaluation practice of #2, #12 and #14: judge the reduction by the model outcome, not by the input error.
- **Model training and validation.** Use TSA or sampling (#16) to choose the training and validation periods for a machine-learning surrogate, similar to #25.
- **Bias correction link.** Corrected series (#21, #22, #24) are the input to reduction. Check whether bias correction changes which periods are selected.
- **Questions for Matti.** Which model would consume the reduced series? Is there a target data set (CorRES European runs, EURO-CORDEX)? Is the output a paper, a tool, or an input to an ongoing DTU project?

## 5. Files

- PDFs and per-paper metadata: Zotero collection `Projects/Time_Series_2026`. PDFs attached for items 1, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 19, 21, 22, 23; the other 9 are tagged `pdf:missing`. Finder view: `~/ctang.Science/Zotero_library/views/by_collection/Projects/Time_Series_2026/`
- `references/all_refs_25.bib`: all 25 entries merged, unique keys
- `references/all_refs_25_verify_report.md`: `verify_bib.py` report (25/25 VERIFIED, run 2026-10-11 on the Downloads copy)
