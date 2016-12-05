def update(elo0, elo1, actual_outcome0, actual_outcome1,
           k_factor=16, magnification_interval=400, magnification_factor=10):
    relative_elo0 = pow(magnification_factor, elo0 / magnification_interval)
    relative_elo1 = pow(magnification_factor, elo1 / magnification_interval)

    elo_normalization_constant = relative_elo0 + relative_elo1

    expected_outcome_ratio0 = relative_elo0 / elo_normalization_constant
    expected_outcome_ratio1 = relative_elo1 / elo_normalization_constant

    total_score = actual_outcome0 + actual_outcome1

    expected_outcome0 = total_score * expected_outcome_ratio0
    expected_outcome1 = total_score * expected_outcome_ratio1

    updated_elo0 = elo0 + k_factor * (actual_outcome0 - expected_outcome0)
    updated_elo1 = elo1 + k_factor * (actual_outcome1 - expected_outcome1)

    return updated_elo0, updated_elo1
