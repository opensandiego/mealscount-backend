django_config = {'secret_key': 6609241238288064823}  # change it in the <your_state>.py or prod.py

model_version_info = {
    "version": "2.0",
    "model_variant": "v2",
    "isp_width_default": 2.0,
    "isp_width_bundle": [0.01, 2.0, 6.25, 12.5, 22.5],

}

us_regions = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY"]


funding_rules = {
    "min_cep_thold_pct": 0.40, # lowest poverty percentage to get any reimbursement
    "max_cep_thold_pct": 0.625,  # poverty percentage to get reimbursed at 100%
    "performance_based_cash_assistance_per_lunch": 0.06,  # healthy lunch 6 cent ... thing.
    "monthly_lunches": 21.64,    # how many lunches on average per month does a student eat
    "monthly_breakfasts": 21.64, # how many breakfasts on average per month does a student eat
    "cep_rates": [{
        "region": "default",
        "nslp_lunch_free_rate": 3.23,
        "nslp_lunch_paid_rate": 0.31,
        "sbp_bkfst_free_rate": 1.75,
        "sbp_bkfst_paid_rate": 0.30}, {
        "region": "AK",
        "nslp_lunch_free_rate": 5.24,
        "nslp_lunch_paid_rate": 0.50,
        "sbp_bkfst_free_rate": 2.79,
        "sbp_bkfst_paid_rate": 0.45}, {
        "region": "HI",
        "nslp_lunch_free_rate": 3.78,
        "nslp_lunch_paid_rate": 0.36,
        "sbp_bkfst_free_rate": 2.03,
        "sbp_bkfst_paid_rate": 0.34}, {
        "region": "PR",
        "nslp_lunch_free_rate": 3.78,
        "nslp_lunch_paid_rate": 0.36,
        "sbp_bkfst_free_rate": 2.03,
        "sbp_bkfst_paid_rate": 0.34}
    ]
}

