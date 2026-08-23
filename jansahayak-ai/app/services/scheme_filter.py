class SchemeFilter:

    def filter_by_state(
        self,
        schemes: list[dict],
        state: str | None = None
    ) -> list[dict]:

        if not state:
            return schemes

        state = state.strip().lower()

        filtered = []

        for scheme in schemes:

            states = [
                str(s).lower().strip()
                for s in scheme.get(
                    "states",
                    []
                )
            ]

            # Central / All-India schemes
            if "all" in states:
                filtered.append(scheme)
                continue

            # State-specific scheme
            if state in states:
                filtered.append(scheme)

        return filtered

    def filter_verified(
        self,
        schemes: list[dict]
    ) -> list[dict]:

        return [
            scheme
            for scheme in schemes
            if scheme.get(
                "verification_status"
            ) == "verified"
        ]