class GenerativeLandscape:
    def __init__(self, lifetime_budget=0.20, decay_rate=0.995, horizon=200, history_window=20, persistence_threshold=0.6):
        self.dimensions = {dim: {'current': 1.0, 'irreversible_cum': 0.0, 'reversible_rolling': 0.0} for dim in ['volume', 'interaction', 'optionality']}
        self.lifetime_budget = lifetime_budget
        self.decay_rate = decay_rate
        self.horizon = horizon
        self.history_window = history_window
        self.persistence_threshold = persistence_threshold
        self.loss_history = []

    def evaluate_action(self, deltas, irreversible=False):
        assert len(deltas) == 3
        results = {dim: 'OK' for dim in ['volume', 'interaction', 'optionality']}
        max_severity = None

        for dim, delta in deltas.items():
            loss = max(0, -delta) if irreversible else 0
            self.dimensions[dim]['irreversible_cum'] += loss
            if self.dimensions[dim]['irreversible_cum'] > self.lifetime_budget:
                results[dim] = 'CUMULATIVE_COLLAPSE'
                max_severity = 'CUMULATIVE_COLLAPSE'

            self.dimensions[dim]['reversible_rolling'] = (
                self.dimensions[dim]['reversible_rolling'] * self.decay_rate + (max(0, -delta) if not irreversible else 0)
            )
            self.dimensions[dim]['current'] = max(0.01, self.dimensions[dim]['current'] + delta)

            if irreversible and delta < -0.05:
                if results.get(dim) != 'CUMULATIVE_COLLAPSE':
                    results[dim] = 'PER_DIMENSION_VETO'
                if max_severity != 'CUMULATIVE_COLLAPSE':
                    max_severity = 'PER_DIMENSION_VETO'

        current_rate = sum(max(0, -d) for d in deltas.values()) / len(deltas)
        self.loss_history.append(current_rate)
        if len(self.loss_history) > self.history_window:
            self.loss_history.pop(0)

        if len(self.loss_history) >= 1:
            weights = [self.decay_rate ** i for i in range(len(self.loss_history))][::-1]
            norm = sum(weights) or 1.0
            weighted_persistence = sum(w * (1 if r > 0.01 else 0) for w, r in zip(weights, self.loss_history)) / norm
            avg_rate = sum(w * r for w, r in zip(weights, self.loss_history)) / norm

            if irreversible and max((-d for d in deltas.values()), default=0) > 0.10:
                if max_severity != 'CUMULATIVE_COLLAPSE':
                    max_severity = 'PER_DIMENSION_VETO'

            confidence = min(1.0, len(self.loss_history) / 8.0)
            effective_threshold = self.persistence_threshold / max(confidence, 0.01)
            if weighted_persistence > effective_threshold:
                projected_total = avg_rate * self.horizon * confidence
                if projected_total > self.lifetime_budget * 0.8:
                    if max_severity not in ('CUMULATIVE_COLLAPSE', 'PER_DIMENSION_VETO'):
                        max_severity = 'TRAJECTORY_COLLAPSE'

        priority = {'CUMULATIVE_COLLAPSE': 3, 'PER_DIMENSION_VETO': 2, 'TRAJECTORY_COLLAPSE': 1}
        verdict = max_severity if max_severity in priority else 'APPROVED'
        return verdict, results   # diagnostic return
