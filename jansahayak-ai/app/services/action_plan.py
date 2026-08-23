class ActionPlanGenerator:

    def generate(
        self,
        scheme: dict,
        eligibility: dict,
        documents: dict
    ) -> list[dict]:

        return [

            {
                "step": 1,
                "title": "Confirm eligibility",
                "description": (
                    "Review the official eligibility "
                    "criteria and resolve any missing "
                    "information."
                )
            },

            {
                "step": 2,
                "title": "Prepare documents",
                "description": (
                    "Collect the required documents "
                    "listed for the scheme."
                )
            },

            {
                "step": 3,
                "title": "Apply through the official channel",
                "description": (
                    "Use the official application "
                    "method listed by the scheme."
                )
            },

            {
                "step": 4,
                "title": "Keep proof",
                "description": (
                    "Save your application number, "
                    "receipt or acknowledgement."
                )
            },

            {
                "step": 5,
                "title": "Follow up",
                "description": (
                    "If the application is delayed, "
                    "use the official contact or "
                    "grievance mechanism."
                )
            }

        ]